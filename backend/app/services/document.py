import os
import uuid
from typing import List, Optional
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from app.core.config import settings
from app.models.document import Document, DocumentStatus
from app.repositories.document import DocumentRepository
from app.repositories.audit import AuditLogRepository

class MockEmbeddingFunction(EmbeddingFunction):
    """Deterministic local mock embedding function for sandboxed testing.
    
    Generates a fixed-dimension vector (3072 floats) matching text-embedding-3-large
    without requiring network requests or model downloads.
    """
    def __init__(self) -> None:
        pass

    def name(self) -> str:
        return "mock"

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            val = float(len(text) % 100) / 100.0
            embeddings.append([val] * 3072)
        return embeddings

class RecursiveCharacterTextSplitter:
    """Custom light splitter mimicking LangChain's RecursiveCharacterTextSplitter interface."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text]
        
        separator = self.separators[-1]
        for s in self.separators:
            if s in text:
                separator = s
                break
        
        splits = text.split(separator)
        chunks = []
        current_chunk = ""
        
        for split in splits:
            if len(current_chunk) + len(split) + (len(separator) if current_chunk else 0) <= self.chunk_size:
                if current_chunk:
                    current_chunk += separator + split
                else:
                    current_chunk = split
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                if len(split) > self.chunk_size:
                    for i in range(0, len(split), self.chunk_size - self.chunk_overlap):
                        chunks.append(split[i:i + self.chunk_size])
                    current_chunk = ""
                else:
                    current_chunk = split
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

class DocumentService:
    """Service layer handling document storage, content parsing, splitting, and vector indexing."""

    def __init__(self, document_repo: DocumentRepository, audit_repo: AuditLogRepository):
        self.document_repo = document_repo
        self.audit_repo = audit_repo
        
        # Ensure directories exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
        
        # Initialize Chroma Client & Collection
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            embedding_function=self._get_embedding_function()
        )

    def _get_embedding_function(self) -> EmbeddingFunction:
        """Resolve embedding function. Uses OpenAI if key is present, else falls back to Mock."""
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "dummy_key_replace_in_env":
            return OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-large"
            )
        return MockEmbeddingFunction()

    def _parse_file(self, file_path: str, content_type: str) -> str:
        """Extract text from file depending on content type (PDF, DOCX, or text/MD)."""
        if "pdf" in content_type:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        elif "word" in content_type or file_path.endswith(".docx"):
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    async def process_document(
        self,
        document_id: uuid.UUID,
        file_path: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Parse, segment, and index document chunks in ChromaDB asynchronously."""
        document = await self.document_repo.update_status(document_id, DocumentStatus.PROCESSING)
        if not document:
            return

        try:
            # 1. Parse content
            text = self._parse_file(file_path, document.content_type)
            if not text.strip():
                raise ValueError("Extracted text is empty")

            # 2. Chunk content
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_text(text)

            # 3. Add to ChromaDB
            ids = [f"{document_id}_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "document_id": str(document_id),
                    "chunk_index": i,
                    "filename": document.filename
                }
                for i in range(len(chunks))
            ]
            self.collection.add(
                ids=ids,
                documents=chunks,
                metadatas=metadatas
            )

            # 4. Mark Complete
            await self.document_repo.update_status(document_id, DocumentStatus.COMPLETED)
            
            await self.audit_repo.create(
                user_id=None,
                action="document_processed",
                ip_address=ip_address,
                user_agent=user_agent,
                payload={"document_id": str(document_id), "filename": document.filename, "chunks_count": len(chunks)}
            )

        except Exception as e:
            error_msg = str(e)[:1000]
            await self.document_repo.update_status(document_id, DocumentStatus.FAILED, error_message=error_msg)
            
            await self.audit_repo.create(
                user_id=None,
                action="document_processing_failed",
                ip_address=ip_address,
                user_agent=user_agent,
                payload={"document_id": str(document_id), "filename": document.filename, "error": error_msg}
            )

    async def delete_document(
        self,
        document_id: uuid.UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        """Remove document file, database metadata, and ChromaDB vector index references."""
        document = await self.document_repo.get_by_id(document_id)
        if not document:
            return False

        # 1. Delete Chroma vectors
        try:
            self.collection.delete(where={"document_id": str(document_id)})
        except Exception:
            pass

        # 2. Remove physical file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}_{document.filename}")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

        # 3. Delete DB record
        success = await self.document_repo.delete(document_id)
        
        if success:
            await self.audit_repo.create(
                user_id=None,
                action="document_deleted",
                ip_address=ip_address,
                user_agent=user_agent,
                payload={"document_id": str(document_id), "filename": document.filename}
            )
            
        return success
