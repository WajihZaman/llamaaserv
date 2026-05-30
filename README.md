# 🤖 Enterprise Local AI RAG Assistant for Corporate Governance

An enterprise-grade, resource-optimized Retrieval-Augmented Generation (RAG) system engineered to handle corporate reporting workflows, data privacy compliance, and organizational guidance. Designed and fully deployed on traditional, CPU-only cloud infrastructure, this architecture serves local quantized LLMs natively to achieve total compliance with enterprise data privacy mandates, completely eliminating commercial vendor subscription paths (saving \$20k–\$80k/year).

---

### 📐 Architectural Scope & System Parameters
* **Role:** Backend AI Developer & Knowledge Engineer
* **Target Infrastructure:** Traditional Azure Server (8 vCPUs, 8 GiB RAM, Zero-GPU Compute Footprint)
* **Performance Metrics:** 12-25 seconds response latency loop under pure CPU execution.
* **Knowledge Infrastructure:** Unified central knowledge base served via ChromaDB to all authorized personnel.

---

### 🗺️ System Data Flow & Telemetry Tracking Matrix

The application leverages a lightweight Basic Authentication schema paired with a dedicated transactional tracking pipeline. To protect network overhead, a shared corporate credential grants access to the gateway, while a mandatory `Employee_ID` payload is injected into every request header to securely audit system usage, exception traces, and chat session histories inside an Azure MySQL instance.

graph TB
    %% Core Nodes Defining the Layers
    User[👤 Client / UI Request Payload]
    Auth[🔑 Basic Auth & Employee_ID Validation]
    MySQL_Auth[(🗄️ Azure MySQL: Validate Credentials)]
    FastAPI[⚡ FastAPI Gateway Router Core]
    Chroma[(🗃️ Chroma Vector DB: Document Retrieval)]
    Llama[🦙 Localized Llama-3.2 GGUF Engine]
    MySQL_Log[(📊 Azure MySQL: Log Telemetry & Chat History)]
    Output[📤 Encrypted JSON Response Stream]

    %% Grouping Components Visually to Prevent Crowding
    subgraph Gateway & Verification Layer
        User -->|1. Transmit Auth Headers| Auth
        Auth -->|2. Check Static Credentials| MySQL_Auth
        MySQL_Auth -->|3. Initialize Session Handshake| FastAPI
    end

    subgraph Knowledge Retrieval Layer
        FastAPI -->|4. Request Semantic Context chunks| Chroma
        Chroma -->|5. Return Relevant KB Text Blocks| FastAPI
    end

    subgraph CPU Inference Processing Layer
        FastAPI -->|6. Inject Context-Augmented Prompt| Llama
        Llama -->|7. Multi-threaded CPU Inference Loop: 12-25s| FastAPI
    end

    subgraph Transactional Persistence Layer
        FastAPI -->|8. Append Async Chat History String| MySQL_Log
        MySQL_Log -->|9. Route Structured Generation Payload| Output
        Output -->|10. Render Interface Response| User
    end

    %% Apply visual polish to key data pathways
    style FastAPI fill:#f9f,stroke:#333,stroke-width:2px
    style Llama fill:#bbf,stroke:#333,stroke-width:1px
    style Chroma fill:#bfb,stroke:#333,stroke-width:1px
    style MySQL_Auth fill:#ffb,stroke:#333,stroke-width:1px
    style MySQL_Log fill:#ffb,stroke:#333,stroke-width:1px

---

### 🚀 Key Technical Indicators & Engineering Implementations

* **Telemetry-Driven Audit Logging:** Engineered an isolated backend tracking mechanism that binds system computation usage, query history, and system exceptions directly to a unique `Employee_ID` string parameter while using a simplified basic authentication access gateway.
* **Unified Vector Ingestion Framework:** Maintained a centralized document index database layout within ChromaDB, utilizing its native embedding layer to serve uniform, context-rich documentation arrays to all querying endpoints.
* **Traditional Azure Hardware Optimization:** Specifically configured to maximize CPU multi-threading and vector mathematical calculations on baseline virtual hardware configurations without requiring expensive GPU compute instances.
* **Stateful MySQL Chat Records:** Utilizes an integrated database topology to log isolated system telemetry, process historical user chat states, and register application exception tracing streams safely.

---

### 📂 Enterprise Repository File System Architecture

```text
├── .env.template          # Global environment variable blueprint
├── Dockerfile             # Global environment variable blueprint
├── requirements.txt       # Unified system Python dependencies
├── main.py                # Primary FastAPI application entry endpoint (Routing Layer)
├── config.py              # Configuration manager and database connections
├── exceptions.py          # Unified system exception handlers and MySQL logging
├── bin                    # Unified system exception handlers and MySQL logging
├── bin2                   # Unified system exception handlers and MySQL logging
└── central/               # Core business processing microservices
    ├── database/vectordb  # Basic Authentication parsing & Employee_ID verification
    ├── db.py              # Central ChromaDB retrieval, indexing, and embedding loops
    ├── prompts.py         # Central ChromaDB retrieval, indexing, and embedding loops
    └── schema.py          # Quantized Llama 3.2 token parsing streaming logic
└── services/              # Core business processing microservices
    ├── dbops.py           # Basic Authentication parsing & Employee_ID verification
    ├── rag.py             # Central ChromaDB retrieval, indexing, and embedding loops
    └── security.py        # Quantized Llama 3.2 token parsing streaming logic
```

---

### 🚀 Local Quick-Start Directory Execution

#### 1. Clone and Navigate to Infrastructure Workspace
```bash
git clone https://github.com
cd local-ai-rag-assistant
```

#### 2. Establish Environment File Configuration
```bash
cp .env.template .env
```
*Open `.env` and populate your secure Azure system credentials.*

#### 3. Execute Environment Compilation via Docker Compose
```bash
docker-compose up --build -d
```
