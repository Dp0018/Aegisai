# AegisAI Complete End-to-End Free Deployment Guide

This guide provides step-by-step instructions to deploy the entire AegisAI platform for **100% free** using modern cloud providers:
* **Frontend:** Vercel (Next.js 14)
* **Backend:** Koyeb or Render (FastAPI, Python 3.11, Docker, WebSockets)
* **Database:** Neon (Serverless PostgreSQL)
* **Cache & Token Blacklist:** Upstash (Serverless Redis)
* **Vector Store:** Pinecone (Managed Vector Database)

---

## Table of Contents
1. [Prerequisites & Accounts Needed](#1-prerequisites--accounts-needed)
2. [Step 1: Obtain Free PostgreSQL URL (Neon)](#step-1-obtain-free-postgresql-url-neon)
3. [Step 2: Obtain Free Redis URL (Upstash)](#step-2-obtain-free-redis-url-upstash)
4. [Step 3: Obtain OpenAI & Pinecone API Keys](#step-3-obtain-openai--pinecone-api-keys)
5. [Step 4: Generate Secure JWT Secrets](#step-4-generate-secure-jwt-secrets)
6. [Step 5: Deploy Backend for Free (Koyeb or Render)](#step-5-deploy-backend-for-free-koyeb-or-render)
7. [Step 6: Run Database Migrations (Remote Neon)](#step-6-run-database-migrations-remote-neon)
8. [Step 7: Deploy Frontend to Vercel](#step-7-deploy-frontend-to-vercel)
9. [Step 8: Post-Deployment Verification & Admin Bootstrap](#step-8-post-deployment-verification--admin-bootstrap)
10. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## 1. Prerequisites & Accounts Needed

Create free accounts on the following platforms (no credit card required for standard free tiers):
1. **GitHub:** Repository containing your AegisAI code.
2. **Neon:** [https://neon.tech](https://neon.tech) (Free PostgreSQL storage).
3. **Upstash:** [https://upstash.com](https://upstash.com) (Free serverless Redis).
4. **Pinecone:** [https://pinecone.io](https://pinecone.io) (Free vector database starter tier).
5. **OpenAI:** [https://platform.openai.com](https://platform.openai.com) (API key for embeddings and GPT-4o models).
6. **Koyeb:** [https://koyeb.com](https://koyeb.com) or **Render:** [https://render.com](https://render.com) (Free backend container hosting).
7. **Vercel:** [https://vercel.com](https://vercel.com) (Free Next.js frontend hosting).

---

## Step 1: Obtain Free PostgreSQL URL (Neon)

AegisAI uses asynchronous PostgreSQL via SQLAlchemy 2.0 and `asyncpg`.

1. Go to [https://neon.tech](https://neon.tech) and sign up with GitHub or Google.
2. Click **Create Project**.
   * **Project Name:** `aegisai-db`
   * **Postgres Version:** `16` (default)
   * **Region:** Choose the region closest to where you will deploy your backend (e.g. US East or Frankfurt).
   * Click **Create Project**.
3. On the Neon Dashboard, navigate to **Connection Details**.
4. Select **Connection string** and ensure **Pooled connection** is unchecked (direct connection is recommended for migrations and connection pools).
5. You will see a URI formatted like:
   ```text
   postgresql://alex:AbCdEf123456@ep-cool-cloud-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
6. **IMPORTANT FORMATTING FOR AEGISAI:**
   AegisAI uses `asyncpg` as its database driver. You **must** change the protocol prefix from `postgresql://` to `postgresql+asyncpg://`.
   
   Example formatted URL:
   ```text
   postgresql+asyncpg://alex:AbCdEf123456@ep-cool-cloud-123456.us-east-2.aws.neon.tech/neondb?ssl=require
   ```
7. Save this URL for your `DATABASE_URL` environment variable.

---

## Step 2: Obtain Free Redis URL (Upstash)

AegisAI uses Redis for JWT token blacklisting upon logout and session caching.

1. Go to [https://upstash.com](https://upstash.com) and log in.
2. Under **Redis**, click **Create Database**.
   * **Name:** `aegisai-redis`
   * **Type:** Regional (Single zone, 100% free forever)
   * **Region:** Match your backend region (e.g., US-East-1 or EU-West-1).
   * **TLS:** Checked / Enabled (default).
   * Click **Create**.
3. Scroll down on the database overview page to the **Connect your database** section.
4. Click on the **redis-py** or **Node** tab and look for the connection URL, or click the **copy** button on the `UPSTASH_REDIS_REST_URL` / standard `rediss://` URI.
5. In the **Details** section, locate the standard Redis endpoint:
   ```text
   rediss://default:[YOUR_PASSWORD]@[YOUR_ENDPOINT].upstash.io:6379
   ```
6. Save this string for your `REDIS_URL` environment variable.

---

## Step 3: Obtain OpenAI & Pinecone API Keys

### 3.1 OpenAI API Key
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Click **Create new secret key**.
3. Name it `aegisai-production` and click **Create secret key**.
4. Copy the key starting with `sk-...`.
5. Save this for your `OPENAI_API_KEY` environment variable.

### 3.2 Pinecone Vector Database
1. Go to [https://app.pinecone.io](https://app.pinecone.io) and log in.
2. In the left sidebar, click **API Keys**.
3. Copy your default API key (or click **Create API Key**). Save this for `PINECONE_API_KEY`.
4. Click **Indexes** in the sidebar, then click **Create Index**:
   * **Index Name:** `aegisai-index`
   * **Dimensions:** `3072` (if using OpenAI `text-embedding-3-large`) or `1536` (if using `text-embedding-3-small`). Standard default in AegisAI is `3072`.
   * **Metric:** `cosine`
   * **Capacity Mode:** `Serverless`
   * **Cloud / Region:** `AWS / us-east-1` (free starter tier eligible).
   * Click **Create Index**.
5. Save `aegisai-index` for your `PINECONE_INDEX_NAME` variable.

*(Note: If you do not want to use Pinecone, you can set `VECTOR_DB_PROVIDER=chroma` to use local disk storage).*

---

## Step 4: Generate Secure JWT Secrets

AegisAI requires two high-entropy random secrets to sign and verify user access tokens and refresh tokens.

Run this command in any terminal to generate two unique cryptographically secure secrets:

```bash
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32)); print('JWT_REFRESH_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Example output:
```text
JWT_SECRET_KEY=k9L1p_Xw4Zq8mN2vRt7Yc3De5Fa6Gb1Hj8Ks0Lm4Pq9
JWT_REFRESH_SECRET_KEY=v3B7n9M2x4L1k8P5q0W6z1C8j2F4h7S9t0R3e6G8d1Y
```
Save both values for your backend configuration.

---

## Step 5: Deploy Backend for Free (Koyeb or Render)

Choose either **Koyeb** (Recommended: zero idle sleep) or **Render**.

### Option A: Deploy to Koyeb (Recommended)

1. Sign up or log in at [https://koyeb.com](https://koyeb.com).
2. Click **Create App**.
3. Under **Deployment Method**, select **GitHub**.
4. Select your `aegis-ai` repository.
5. In the configuration panel:
   * **Service Name:** `aegisai-backend`
   * **Root Directory:** Enter `backend`
   * **Builder:** Select **Dockerfile** (Koyeb will auto-detect `backend/Dockerfile`)
   * **Port:** Set to `8000`
   * **Instance Type:** Select **Free (Nano)** (512 MB RAM, 0.1 vCPU)
6. Under **Environment Variables**, click **Add Variable** and input the following keys:

| Variable Name | Value |
| :--- | :--- |
| `APP_NAME` | `AegisAI Enterprise Platform` |
| `DEBUG` | `False` |
| `API_PREFIX` | `/api/v1` |
| `DATABASE_URL` | `postgresql+asyncpg://[user]:[password]@[host]/neondb?ssl=require` |
| `REDIS_URL` | `rediss://default:[password]@[endpoint]:6379` |
| `VECTOR_DB_PROVIDER` | `pinecone` (or `chroma`) |
| `PINECONE_API_KEY` | Your Pinecone API key |
| `PINECONE_INDEX_NAME` | `aegisai-index` |
| `OPENAI_API_KEY` | `sk-...` |
| `JWT_SECRET_KEY` | Your generated JWT secret |
| `JWT_REFRESH_SECRET_KEY` | Your generated JWT refresh secret |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` |

7. Click **Deploy**.
8. Once built and healthy, copy your public backend URL from the Koyeb dashboard:
   ```text
   https://[your-app-name].koyeb.app
   ```
9. Verify by visiting `https://[your-app-name].koyeb.app/health` in your browser. It should return `{"status":"healthy","service":"AegisAI Backend"}`. Interactive Swagger docs will be live at `https://[your-app-name].koyeb.app/docs`.

---

### Option B: Deploy to Render

1. Sign up or log in at [https://render.com](https://render.com).
2. Click **New +** and select **Web Service**.
3. Choose your `aegis-ai` GitHub repository.
4. Set the build details:
   * **Name:** `aegisai-backend`
   * **Region:** Oregon (US West) or Frankfurt (EU)
   * **Branch:** `main`
   * **Root Directory:** `backend`
   * **Runtime:** Select `Docker`
   * **Instance Type:** Select `Free`
5. Under **Environment Variables**, paste all the variables listed in the table above.
6. Click **Create Web Service**.
7. Render will build the container and provide your URL (e.g. `https://aegisai-backend.onrender.com`).

---

## Step 6: Run Database Migrations (Remote Neon)

Now that your Neon PostgreSQL database is created and your backend is deployed, apply the database schema so the tables (`users`, `threads`, `actions`, `documents`, `messages`) exist.

From your local machine in the project root:

```bash
cd backend
DATABASE_URL="postgresql+asyncpg://[YOUR_NEON_USER]:[YOUR_NEON_PASSWORD]@[YOUR_NEON_HOST]/neondb?ssl=require" alembic upgrade head
```

You will see output showing migrations applied successfully:
```text
INFO  [alembic.runtime.migration] Running upgrade  -> 5443e56cc871, create initial schemas
INFO  [alembic.runtime.migration] Running upgrade 5443e56cc871 -> 794570c1769d, create thread and memory tables
INFO  [alembic.runtime.migration] Running upgrade 794570c1769d -> 16a99639e88e, create documents table
```

---

## Step 7: Deploy Frontend to Vercel

With your backend live, deploy the Next.js frontend to Vercel.

1. Go to [https://vercel.com](https://vercel.com) and log in.
2. Click **Add New...** > **Project**.
3. Import your `aegis-ai` GitHub repository.
4. In the project configuration:
   * **Framework Preset:** `Next.js`
   * **Root Directory:** Click **Edit** and select `frontend`
5. Expand the **Environment Variables** accordion and add:

| Key | Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://[your-backend-app].koyeb.app/api/v1` | Public REST API endpoint |
| `NEXT_PUBLIC_WS_URL` | `wss://[your-backend-app].koyeb.app/api/v1` | Public WebSocket endpoint |
| `NEXT_PUBLIC_OBSERVABILITY_URL` | `http://localhost:3100` | Grafana URL (or link to your monitoring) |

6. Click **Deploy**.
7. Vercel will build the frontend and provide your production URL:
   ```text
   https://aegis-ai.vercel.app
   ```
8. **Custom Domain (Optional / Launch Gate):**
   * Go to **Settings** > **Domains** in your Vercel project.
   * Enter your custom domain (e.g. `aegisai.yourdomain.com`).
   * Add the CNAME or A record provided by Vercel into your DNS provider (Cloudflare, Namecheap, GoDaddy).

---

## Step 8: Post-Deployment Verification & Admin Bootstrap

Once both services are live, verify the platform end-to-end:

### 1. Bootstrap the First Administrator Account
1. Open your production frontend URL: `https://[your-app].vercel.app/register`.
2. Enter your details:
   * Full Name: Your Name
   * Email: `admin@aegisai.com`
   * Role: `Administrator (IAM & Uploads)`
   * Password: Choose a secure password (minimum 6 characters)
3. Click **Create Account**.
4. Because the database was clean, AegisAI automatically assigns this first registered identity the **Administrator** role.

### 2. Ingest Enterprise Documents
1. Log in and click **Documents Ingestion** in the sidebar.
2. Drag and drop any corporate policy PDF, DOCX, or Markdown file.
3. Observe the upload progress bar. The backend parses, chunks, and indexes vectors into your Pinecone/Chroma database. Status will transition to **Completed**.

### 3. Verify Agent Chat & Reasoning Telemetry
1. Click **Chat Console** in the sidebar.
2. Click **New Session**.
3. Ask a question relevant to your uploaded document.
4. Watch the right-hand **Reasoning Telemetry** panel update as LangGraph traverses the nodes (`CoordinatorNode` -> `ResearchNode` -> `RespondNode`).

### 4. Verify Human-in-the-Loop Review
1. Send an action-oriented or risky query (e.g., *"Issue a refund of \$50,000 for SLA breach"*).
2. The agent graph pauses execution and presents an **Operator Action Required** review box.
3. Click **Approve & Release** or write revision directives and click **Request Redraft**.

---

## Troubleshooting & FAQs

### 1. `Cannot connect to host fonts.googleapis.com` during Next.js build
If Vercel or an offline environment encounters trouble reaching Google Fonts, Next.js automatically falls back to system fonts. This does not block production execution.

### 2. Backend WebSockets returning 403 or failing to connect
Ensure your `NEXT_PUBLIC_WS_URL` uses the `wss://` protocol in production:
```text
NEXT_PUBLIC_WS_URL=wss://[your-backend-app].koyeb.app/api/v1
```
*(Do not use `ws://` on an HTTPS production domain).*

### 3. Database connection timeout on Neon
Ensure your connection string includes `?ssl=require` at the end:
```text
postgresql+asyncpg://[user]:[password]@[host]/neondb?ssl=require
```

### 4. Kafka errors on Koyeb / Render
AegisAI has a built-in graceful fallback: if Apache Kafka is not present, the backend logs a connection notice and continues operating all REST and WebSocket agent loops without interruption.

