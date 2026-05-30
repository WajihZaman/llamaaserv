# Enterprise Local AI RAG Assistant for Corporate Governance

An enterprise-grade, resource-optimized Retrieval-Augmented Generation (RAG) system engineered to handle corporate reporting workflows, data privacy compliance, and organizational guidance. Designed and fully deployed on traditional, CPU-only cloud infrastructure, this architecture serves local quantized LLMs natively to achieve total compliance with enterprise data privacy mandates, completely eliminating commercial vendor subscription paths (saving \$20k–\$80k/year).

---

### Architectural Scope & Performance Metrics
* **Role:** Backend AI Developer & Knowledge Engineer
* **Target Infrastructure:** Traditional Azure Server (8 vCPUs, 8 GiB RAM, Zero-GPU Compute Footprint)
* **Ingestion Strategy:** Offline Decoupled Embedding Processing (Zero Production Overhead)
* **Knowledge Infrastructure:** Central Unified ChromaDB Vector Database

---

### System Data Flow & Telemetry Tracking Matrix

To maximize production compute cycles, data ingestion is completely decoupled from runtime execution. Document vector embeddings are generated offline on separate developer workstations and shipped directly as pre-compiled data weights. At runtime, the FastAPI app performs zero-overhead semantic searches and tracks usage by `Employee_ID` inside Azure MySQL.

```mermaid
graph TB

    %% =========================================================
    %% 1. PIPELINE NODE DEFINITIONS
    %% =========================================================
    Dev[💻 Local Laptop / RDP Machine <br> Raw Knowledge Base Docs]
    Git[📦 GitHub Repository <br> Pre-Computed Embeddings Storage]
    
    User[👤 Client UI Request <br> basic_auth + Employee_ID]
    FastAPI{⚡ FastAPI Gateway Router}
    
    MySQL_Auth[(🗄️ Azure MySQL <br> Verify Global Credentials)]
    Chroma[(🗃️ Production Chroma DB <br> Reads Pre-Computed Vectors)]
    Llama[🦙 Local Llama-3.2 GGUF <br> CPU Inference Engine]
    MySQL_Log[(📊 Azure MySQL <br> Log Telemetry & Chat Histories)]
    
    Output[📤 Encrypted JSON Response]

    %% =========================================================
    %% 2. PIPELINE INTERACTIONS
    %% =========================================================
    %% Offline Data Pipeline
    Dev -->|A. Run Local Embeddings Model| Git
    Git -->|B. Manually Ship Pre-Compiled Database Artifacts| Chroma

    %% Live Runtime API Pipeline
    User -->|1. Transmit Payload Headers| FastAPI
    FastAPI -->|2. Check Static Credentials| MySQL_Auth
    MySQL_Auth -->|3. Return Session Auth OK| FastAPI
    FastAPI -->|4. Query Pre-Loaded Vectors| Chroma
    Chroma -->|5. Return Context Chunks| FastAPI
    FastAPI -->|6. Run Multi-Threaded Prompt| Llama
    Llama -->|7. Latency Loop: 12-25 Seconds| FastAPI
    FastAPI -->|8. Async Append User History| MySQL_Log
    MySQL_Log -->|9. Construct Response Object| Output
    Output -->|10. Render App UI View| User

    %% =========================================================
    %% 3. REFINED GRAPH ACCENTS
    %% =========================================================
    classDef default fill:#1a1d24,stroke:#4a5568,stroke-width:1px,color:#ffffff;
    style FastAPI fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#ffffff
    style Llama fill:#062040,stroke:#3b82f6,stroke-width:2px,color:#ffffff
    style Chroma fill:#062f21,stroke:#10b981,stroke-width:2px,color:#ffffff
    style MySQL_Auth fill:#272510,stroke:#eab308,stroke-width:2px,color:#ffffff
    style MySQL_Log fill:#272510,stroke:#eab308,stroke-width:2px,color:#ffffff
    style Dev fill:#2d3748,stroke:#cbd5e0,stroke-width:1px,color:#ffffff
    style Git fill:#2d3748,stroke:#cbd5e0,stroke-width:1px,color:#ffffff
```

---

### Key Technical Indicators & Engineering Implementations

* **Offline Decoupled Embedding Ingestion:** Designed a zero-overhead production ingestion strategy. By generating document embeddings locally on isolated RDP/workstation hardware and committing the pre-compiled database files straight to the repository, the production Azure server is completely protected from resource-heavy token embedding calculation loops.
* **Telemetry-Driven Audit Logging:** Engineered an isolated backend tracking mechanism that binds system computation usage, query history, and system exceptions directly to a unique `Employee_ID` string parameter while using a simplified basic authentication access gateway.
* **Traditional Azure Hardware Optimization:** Specifically configured to maximize CPU multi-threading and vector mathematical calculations on baseline virtual hardware configurations without requiring expensive GPU compute instances.
* **Hardened Instruction-Level Execution Tracing:** To guarantee absolute determinism and zero-fault data lineage under strict corporate compliance mandates, the backend implements a granular line-by-line audit framework. By piping static execution state markers directly into MySQL stored procedures after sequential code blocks using async thread pools (`run_in_threadpool`), the application isolates runtime anomalies and benchmarks code performance with microsecond precision directly on the Azure host machine.


---

### Enterprise Repository File System Architecture

```text
├── .env.template          # Global environment variable blueprint
├── Dockerfile             # Code to Deploy the program to Azure Server using Ubuntu Latest
├── requirements.txt       # Unified system Python dependencies
├── main.py                # Primary FastAPI application entry endpoint (Routing Layer)
├── config.py              # Configuration manager and database connections
├── exceptions.py          # Unified system exception handlers and MySQL logging
├── Model                  # Local AI GGUF Model (Llama 3.2) invoked by llama server  
├── bin/                   # Production Ubuntu binary (Unzipped automatically via Dockerfile)
├── bin2/                  # Local Windows binary (Leveraged for isolated desktop testing)
└── central/               # Application core configurations, schemas, and database mappings
    ├── database/vectordb  # PRE-COMPUTED DATA VECTORS (Committed manually via Git)
    ├── db.py              # Central MySql Database Models in SQLAlchemy
    ├── prompts.py         # System prompt for the Local AI model
    └── schema.py          # Pydantic Model for User Queries
└── services/              # Core business processing microservices
    ├── dbops.py           # Store and retrieve chat history from MySQL Database
    ├── rag.py             # Central ChromaDB vectors retrieval, chat history, system prompt to generate response to user query.
    └── security.py        # Basic Useer Authentication executed on every user query
```

---

### Local Quick-Start Directory Execution

#### 1. Clone and Navigate to Infrastructure Workspace
```bash
git clone https://github.com/WajihZaman/local-ai-rag-assistant
cd local-ai-rag-assistant
```

#### 2. Establish Environment File Configuration
```bash
cp .env.template .env
```
