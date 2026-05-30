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

```mermaid
graph TB

    %% =========================================================
    %% 1. PIPELINE NODE DEFINITIONS (High Contrast Styling)
    %% =========================================================
    User[👤 Client UI Request <br> basic_auth + Employee_ID]
    
    FastAPI_Auth{⚡ FastAPI Gateway: Authenticating}
    MySQL_Auth[(🗄️ Azure MySQL <br> Verify Static Credentials)]
    
    FastAPI_RAG{⚡ FastAPI Gateway: Context Retrieval}
    Chroma[(🗃️ Chroma Vector DB <br> Semantic KB Search)]
    
    FastAPI_LLM{⚡ FastAPI Gateway: Model Execution}
    Llama[🦙 Local Llama-3.2 GGUF <br> CPU Inference Engine]
    
    FastAPI_Log{⚡ FastAPI Gateway: Telemetry Ingestion}
    MySQL_Log[(📊 Azure MySQL <br> Log Chat & Exception History)]
    
    Output[📤 Encrypted JSON Response]

    %% =========================================================
    %% 2. LINEAR STEP-BY-STEP DATAFLOW (Eliminates Text Crowding)
    %% =========================================================
    User --> |1. Transmit Payload Headers| FastAPI_Auth
    
    FastAPI_Auth --> |2. Check DB Records| MySQL_Auth
    MySQL_Auth --> |3. Session Authorized OK| FastAPI_RAG
    
    FastAPI_RAG --> |4. Execute Vector Search| Chroma
    Chroma --> |5. Return Context Chunks| FastAPI_LLM
    
    FastAPI_LLM --> |6. Inject Context-Informed Prompt| Llama
    Llama --> |7. Latency Loop: 12-25 Seconds| FastAPI_Log
    
    FastAPI_Log --> |8. Async Append User History| MySQL_Log
    MySQL_Log --> |9. Generate Final Response Object| Output
    
    Output --> |10. Render Completed Stream View| User

    %% =========================================================
    %% 3. REFINED GRAPH ACCENTS (Dark-Mode Harmony)
    %% =========================================================
    classDef default fill:#1a1d24,stroke:#4a5568,stroke-width:1px,color:#ffffff;
    
    style FastAPI_Auth fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#ffffff
    style FastAPI_RAG fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#ffffff
    style FastAPI_LLM fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#ffffff
    style FastAPI_Log fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#ffffff
    
    style Llama fill:#062040,stroke:#3b82f6,stroke-width:2px,color:#ffffff
    style Chroma fill:#062f21,stroke:#10b981,stroke-width:2px,color:#ffffff
    style MySQL_Auth fill:#272510,stroke:#eab308,stroke-width:2px,color:#ffffff
    style MySQL_Log fill:#272510,stroke:#eab308,stroke-width:2px,color:#ffffff
```


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
