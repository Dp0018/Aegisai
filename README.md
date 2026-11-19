# AegisAI Enterprise Agent Platform
### Production-Grade GenAI + RAG + Multi-Agent Enterprise Operations & Telemetry System

---

## 📖 1. Project Overview

**AegisAI** is a production-grade enterprise operations platform designed to simulate how next-generation AI agents function within modern organizations. The platform autonomously reads documents, reasons step-by-step using a stateful multi-agent graph, queries enterprise knowledge bases, streams live telemetry events, and incorporates strict Human-in-the-Loop (HITL) compliance reviews before executing actions (like mock SMTP email dispatches).

---

## 🚀 2. Core Features

### 🔐 Identity & Access Management (IAM)
* **Role-Based Access Control (RBAC):** Supports `Administrator` (Full access, uploa ds, team setup), `Operator` (Reviews drafts, reviews reasoning), and `Viewer` (Read-only access).
* **Token Blacklisting:** JWT token revocation via Redis storage for immediate session terminations upon logout.
* **Bootstrapping:** Automatically bootstraps the first registered user in a clean database as an `Administrator`.

### 👥 Team Management (Admin Portal)
* **Operator Gateway:** Interactive dashboard module visible only to administrators.
* **Inline Creation:** Easily register new operators or viewers without logging out of the administrator session.
* **Identity Audit:** View a complete grid of active coordinate profiles.

### 📚 Knowledge Ingestion & RAG
* **Multi-Format Parsing:** Parses Markdown policies, PDFs, and complex DOCX table matrices.
* **Vector Embeddings:** Chunking and high-dimensional semantic vector generation using OpenAI's `text-embedding-3-large`.
* **Hybrid Database Adapter:** Unified adapter supporting **Pinecone** (production-grade SaaS) and local **ChromaDB** (development-ready).

### 🧠 LangGraph Multi-Agent Brain
* **Stateful Graph Execution:** Custom StateGraph coordinating nodes:
  * `Coordinator Node:` Evaluates user inputs for direct response routing or risk escalation.
  * `Research Node:` Similarity searches matched context chunks (automatic `top_k=5`).
  * `Respond Node:` GPT-4o model generates answers grounded strictly in retrieved context.
  * `Escalation Node:` Auto-detects SLA breaches, billing, or legal risks, pauses graph state, and logs a helpdesk ticket.
* **Human-in-the-Loop Interrupts:** Automatically pauses execution for response drafts, allowing operators to **Approve** or **Reject & Redraft** with custom revision feedback.

### ⚡ Live Event Telemetry
* **Kafka Streaming:** Emits agent thoughts, database queries, and tool actions to a Kafka broker.
* **WebSockets Consolidation:** Streams events from the Kafka consumer directly to the Next.js UI.
* **Visual Console:** Premium glassmorphic side-panel renders live reasoning traces as the AI computes.

### 📊 System Observability
* **Prometheus Integration:** FastAPI metrics instrumentator exposing endpoints (request counts, model latencies, exceptions).
* **Grafana Dashboards:** Pre-configured monitoring charts accessible via port `3100` to track CPU, memory, and query speeds.

---

## 🛠️ 3. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons, TanStack Query |
| **Backend** | FastAPI, Uvicorn, LangGraph, LangChain, PyPDF, Pydantic v2 |
| **Database & Cache** | PostgreSQL (relational storage), Redis (cache & blacklist), SQLAlchemy 2.0, Alembic |
| **Vector Indexing** | Pinecone, ChromaDB, OpenAI Embeddings (`text-embedding-3-large`) |
| **Event Broker** | Apache Kafka, Zookeeper, `aiokafka` |
| **Observability** | Prometheus, Grafana, `prometheus-fastapi-instrumentator` |
| **Containerization** | Docker, Docker Compose |

---

## 🧬 4. System Architecture & Directory Structure

```text
aegisai/
├── backend/                   # FastAPI Backend Application
│   ├── app/
│   │   ├── api/               # API Endpoints (v1)
│   │   ├── core/              # Config, Security, Kafka, Websockets
│   │   ├── db/                # DB Session & Redis Connections
│   │   ├── models/            # SQLAlchemy DB Models
│   │   ├── repositories/      # DB Repositories (Thread, User, Memory)
│   │   ├── schemas/           # Pydantic Schemas
│   │   └── services/          # Agent (LangGraph), Document, RAG, Auth
│   ├── monitoring/            # Prometheus Config Files
│   ├── tests/                 # Pytest Suites (Auth, Agent, Kafka, Metrics)
│   ├── alembic.ini            # Database migration CLI configuration
│   ├── requirements.txt       # Python Dependencies
│   └── Dockerfile             # Container image configuration
│
├── frontend/                  # Next.js Frontend Application
│   ├── src/
│   │   ├── app/               # Page routing & Layout structures
│   │   ├── components/        # Reusable UI (AuthGuard, DashboardLayout)
│   │   ├── features/          # Feature Domains (Auth, Chat, Documents)
│   │   └── lib/               # API Clients & Utilities
│   ├── package.json           # Frontend Dependencies
│   └── Dockerfile             # Multi-stage build container
│
└── docker-compose.yml         # Platform orchestration manifest (Postgres, Redis, Kafka, Grafana)
```

---

## ⚙️ 5. Installation & Setup

### Prerequisites
* Docker & Docker Compose
* Node.js v18+ & `pnpm`
* Python 3.11+ & virtualenv

### 1. Launch Services (Docker)
In the root directory, start the infrastructure services:
```bash
docker-compose up -d
```
*Starts PostgreSQL, Redis, Kafka, Zookeeper, Prometheus, and Grafana.*

### 2. Configure Environment variables
Create a `.env` file in the `backend/` directory:
```env
APP_NAME=AegisAI Control
DEBUG=False
API_PREFIX=/api/v1
DATABASE_URL=postgresql+asyncpg://postgres:secure_password_123@localhost:5432/aegisai_db
REDIS_URL=redis://:redis_password_123@localhost:6379/0
VECTOR_DB_PROVIDER=pinecone # Use chroma or pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=generate_a_random_jwt_key
JWT_REFRESH_SECRET_KEY=generate_another_random_jwt_key
```

### 3. Run Database Migrations
Initialize schemas on your local PostgreSQL database:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. alembic upgrade head
```

### 4. Start backend Server
```bash
uvicorn app.main:app --reload --port 8000
```
* **Endpoints Docs:** `http://localhost:8000/docs`

### 5. Install & Run Frontend
In a new terminal window:
```bash
cd frontend
pnpm install
pnpm run dev
```
* **Frontend UI:** `http://localhost:3000`

---

## 🧪 6. Test Suite
Ensure the backend dependencies and core lifecycles are functional:
```bash
cd backend
PYTHONPATH=. pytest
```
*Includes tests for IAM lifecycle, Blacklisting, LangGraph State loops, Kafka broker streams, and Prometheus metrics endpoints.*

---

## 🧑‍✈️ 7. Verification Workflow

1. **Bootstrap Admin:** Go to `http://localhost:3000/register` and register the first account using the role **`Administrator`**.
2. **Team Setup:** Access **Team Management** in the sidebar, and register a new **`Operator`** account.
3. **Index Knowledge:** Go to **Documents Ingestion**, upload a PDF policy/SLA document, and confirm status becomes `completed`.
4. **Chat & Stream:** Log in as your operator, go to **Chat Console**, ask a question, and observe the live reasoning telemetry traces and documents retrieved.
5. **Human-in-the-Loop Review:** Approve or reject/revise response drafts. Check mock SMTP logs for output.
6. **Observability Check:** Open `http://localhost:3100` (login: `admin` / `admin`) to monitor performance.

---

## 🌐 8. Production & Free Cloud Deployment Guide

AegisAI can be deployed for **100% free** using a decoupled cloud architecture (Vercel for Frontend, Koyeb/Render for Backend, Neon for PostgreSQL, and Upstash for Redis) or self-hosted via Docker Compose.

### Free Cloud Architecture Overview

| Component | Free Cloud Provider | Key Configuration |
| :--- | :--- | :--- |
| **Frontend** | [Vercel](https://vercel.com) | Root: `frontend`, Next.js preset |
| **Backend API** | [Koyeb](https://koyeb.com) or [Render](https://render.com) | Root: `backend`, Docker build, Port: `8000` |
| **Relational Database** | [Neon](https://neon.tech) (0.5GB free) | Serverless PostgreSQL with `asyncpg` |
| **Cache & Token Revocation** | [Upstash Redis](https://upstash.com) (10k cmd/day) | Standard Redis connection URI |
| **Vector Index** | [Pinecone](https://pinecone.io) (100k vectors) | Cloud vector index with `text-embedding-3-large` |

### Step 1: Provision Free Backing Databases

1. **Neon PostgreSQL:**
   * Create a project at [neon.tech](https://neon.tech) named `aegisai_db`.
   * Copy the connection string and change the protocol to `postgresql+asyncpg://`:
     ```text
     postgresql+asyncpg://[user]:[password]@[host]/aegisai_db?ssl=require
     ```
2. **Upstash Redis:**
   * Create a Redis database at [upstash.com](https://upstash.com).
   * Copy the connection string (`rediss://default:[password]@[endpoint]:6379`).

### Step 2: Deploy Backend to Koyeb (Zero Cold Starts) or Render

1. Sign up at [koyeb.com](https://koyeb.com) (or [render.com](https://render.com)).
2. Create a new Web Service and link your GitHub repository.
3. Set build configuration:
   * **Root Directory:** `backend`
   * **Build Type:** `Dockerfile` (uses `backend/Dockerfile`)
   * **Port:** `8000`
4. Add the following Environment Variables in the provider dashboard:
   ```env
   DEBUG=False
   API_PREFIX=/api/v1
   DATABASE_URL=postgresql+asyncpg://[user]:[password]@[host]/aegisai_db?ssl=require
   REDIS_URL=rediss://default:[password]@[endpoint]:6379
   VECTOR_DB_PROVIDER=pinecone
   PINECONE_API_KEY=your_pinecone_key
   PINECONE_INDEX_NAME=aegisai-index
   OPENAI_API_KEY=sk-your-openai-api-key
   JWT_SECRET_KEY=your_secure_random_jwt_key
   JWT_REFRESH_SECRET_KEY=your_secure_random_refresh_key
   ```
5. Deploy the service to obtain your public backend HTTPS URL (e.g. `https://aegisai-backend.koyeb.app`).

### Step 3: Run Remote Migrations

Run database migrations locally against your remote Neon database:
```bash
cd backend
DATABASE_URL="postgresql+asyncpg://[user]:[password]@[host]/aegisai_db?ssl=require" alembic upgrade head
```

### Step 4: Deploy Frontend to Vercel

1. Import your repository on [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Add Environment Variables:
   * `NEXT_PUBLIC_API_URL=https://[your-backend-domain].koyeb.app/api/v1`
   * `NEXT_PUBLIC_WS_URL=wss://[your-backend-domain].koyeb.app/api/v1`
   * `NEXT_PUBLIC_OBSERVABILITY_URL=http://localhost:3100`
4. Deploy the frontend and connect your production custom domain.

---

### Alternative: Self-Contained VPS Deployment (Docker Compose)

For dedicated servers or virtual private servers (DigitalOcean, Hetzner, AWS EC2):

1. Clone the repository and configure `backend/.env`.
2. Start all services using the production compose file:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
3. Run migrations inside the backend container:
   ```bash
   docker exec -it aegisai-backend alembic upgrade head
   ```
4. Set up Caddy or Nginx reverse proxy with automated SSL for your domains.
