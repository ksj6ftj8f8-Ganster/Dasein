# 🗺️ MAPA COMPLETO DEL ECOSISTEMA DASEIN

## 1. ESTRUCTURA JERÁRQUICA GENERAL

```
DASEIN (Raíz del Ecosistema)
│
├─ 🔴 LIGHTRAG SYSTEM (Core RAG Framework)
│  ├─ lightrag/ (paquete principal)
│  ├─ lightrag_source/ (submodule remoto)
│  ├─ lightrag-api/ (FastAPI wrapper)
│  ├─ lightrag_webui/ (React + TypeScript)
│  └─ examples/ (casos de uso)
│
├─ 🟢 RENODE ENTITY SYSTEM (Hardware Simulation)
│  ├─ renode_entity/
│  │  ├─ src/monje_virtual.c (kernel module)
│  │  ├─ rpi4.resc (platform spec)
│  │  ├─ renode_script.py (orchestrator)
│  │  ├─ scripts/ (build, test, deploy)
│  │  └─ reports/ (output files)
│  └─ Dockerfile.renode (containerization)
│
├─ 🔵 REM SYSTEM (Multimodal Experience Recording)
│  ├─ REm/ (carpeta activa)
│  │  ├─ remforge_ultra_formato_optimo.py (core)
│  │  ├─ remforge_lite.py (versión ligera)
│  │  ├─ remforge.js (frontend)
│  │  ├─ remforge_dashboard.html (UI)
│  │  ├─ rems_formato_optimo.json (schema)
│  │  └─ demo_files/ (ejemplos)
│  └─ Entity2/Entity2-main/REm/ (copia)
│
├─ 🟡 ECLOSION SYSTEM (Event Processing)
│  ├─ Entity-copilot-deploy-ec-losion-v042/
│  │  ├─ bin/ (generador_eventos.py, mensajero_silencioso.py, monje_pasivo.py)
│  │  ├─ docs/ (INSTALLATION.md, QUICKSTART.md)
│  │  ├─ systemd/ (service descriptors)
│  │  └─ setup_eclosion.sh (deployment)
│  └─ Propósito: Procesamiento de eventos asincrónico
│
├─ 🟣 DOCUMENTATION LAYER
│  ├─ docs/ (oficial)
│  │  ├─ Algorithm.md (LightRAG algorithm)
│  │  ├─ DockerDeployment.md (Docker guide)
│  │  ├─ OfflineDeployment.md (offline setup)
│  │  ├─ FrontendBuildGuide.md (React build)
│  │  ├─ UV_LOCK_GUIDE.md (dependency management)
│  │  └─ LightRAG_concurrent_explain.md (concurrency model)
│  └─ Archivos generados (análisis, diagramas)
│
├─ 📦 INFRASTRUCTURE
│  ├─ docker-compose.yml (orchestración completa)
│  ├─ Dockerfile (LightRAG)
│  ├─ Dockerfile.lite (versión ligera)
│  ├─ k8s-deploy/ (Kubernetes)
│  │  ├─ databases/
│  │  │  ├─ 00-config.sh
│  │  │  ├─ 01-prepare.sh
│  │  │  ├─ 02-install-database.sh
│  │  │  └─ 03-uninstall-database.sh
│  │  └─ deployment manifests
│  ├─ lightrag.service.example (systemd)
│  └─ docker-build-push.sh (CI/CD helper)
│
├─ ⚙️ CONFIGURATION FILES
│  ├─ pyproject.toml (Python package config)
│  ├─ setup.py (setup script)
│  ├─ config.ini.example (app config template)
│  ├─ env.example (environment variables)
│  ├─ env.ollama-binding-options.example
│  ├─ requirements-offline*.txt (dependencies)
│  └─ MANIFEST.in (distribution manifest)
│
├─ 📚 KNOWLEDGE BASE
│  ├─ inputs/ (datos crudos para ingesta)
│  ├─ rag_storage/ (almacenamiento persistente)
│  ├─ temp/ (archivos temporales)
│  └─ data/ (volúmenes Docker)
│
├─ 📋 PROJECT MANAGEMENT
│  ├─ README.md (English)
│  ├─ README-zh.md (Chinese)
│  ├─ LICENSE (MIT/Apache)
│  ├─ SECURITY.md (security guidelines)
│  ├─ paging.md (doc organization)
│  ├─ AGENTS.md (guidelines for this AI)
│  └─ Entity2/ (archived experiments)
│
└─ 🎯 ASSETS
   ├─ assets/ (logos, images)
   └─ Example visualizations
```

---

## 2. MAPEO DE COMPONENTES Y RESPONSABILIDADES

| Componente | Directorio | Responsabilidad Principal | Entrada | Salida | Lenguaje |
|:-----------|:-----------|:------------------------|:--------|:-------|:---------|
| **LightRAG Core** | `lightrag/` | Orquestación RAG | Texto/Docs | Embeddings + Grafos | Python |
| **Query Engine** | `lightrag/` | Búsqueda semántica | Pregunta | Top-k Resultados | Python |
| **Entity Extractor** | `lightrag/` | NER + Linking | Texto | Entidades | Python |
| **Relation Builder** | `lightrag/` | RE (Relational Extract) | Texto | Relaciones | Python |
| **Renode Simulator** | `renode_entity/` | Simulación hardware | `.resc` script | CSV measurements | C + Python |
| **Monje Virtual** | `renode_entity/src/` | Kernel module | CPU events | 72D vectors | C |
| **Side-Channel Analyzer** | `renode_entity/` | CPA/TVLA analysis | measurements | vulnerability scores | Python |
| **REMForge Ultra** | `REm/` | Multimodal conversion | Imágenes/Audio/Texto | REM JSON | Python |
| **REMForge Dashboard** | `REm/` | Visualización interactiva | REM JSON | HTML dashboard | JavaScript + HTML |
| **FastAPI Server** | `lightrag-api/` | HTTP wrapper | HTTP request | JSON response | Python |
| **React WebUI** | `lightrag_webui/` | User interface | Browser events | HTML/JS | TypeScript + React |
| **Eclosion Events** | `Entity-copilot-deploy-ec-losion-v042/` | Event processing | System events | Triggers/Actions | Python |
| **N8N Workflows** | Docker service | Workflow orchestration | HTTP webhooks | Actions | JavaScript |
| **Neo4j Store** | Docker container | Graph database | Cypher queries | Graph results | CQL |
| **Milvus Store** | Docker container | Vector database | FAISS/IVF searches | Similar vectors | C++ |
| **MongoDB Store** | Docker container | Document database | JSON documents | Query results | JavaScript |
| **Redis Cache** | Docker container | Caché + PubSub | Key-value ops | Cached values | C |

---

## 3. FLUJOS DE INTEGRACIÓN

### 3.1 Flujo: Ingesta desde Renode → LightRAG → Consulta

```
┌──────────────────────────────────────────────────────────────┐
│ SIMULACIÓN                                                   │
├──────────────────────────────────────────────────────────────┤
│ renode_script.py inicia simulación                          │
│  ├─ carga rpi4.resc                                         │
│  ├─ ejecuta monje_virtual.ko                                │
│  └─ genera measurements_*.csv (1000+ filas)                │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ ANÁLISIS LATERAL                                             │
├──────────────────────────────────────────────────────────────┤
│ side_channel_analyzer.py procesa CSV                        │
│  ├─ CPA correlation: ≈ 0.97                                 │
│  ├─ TVLA p-value: ≈ 0.0003                                  │
│  └─ Genera analysis_results.json                            │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ INGESTA A LIGHTRAG                                           │
├──────────────────────────────────────────────────────────────┤
│ RenodeAdapter.ingest_from_csv()                            │
│  ├─ Parsea CSV                                              │
│  ├─ Crea entidades: Instruction, Pattern, Vulnerability    │
│  ├─ Inserta en Neo4j                                        │
│  │  └─ Nodos: [Instruction, EnergyPattern, Vulnerability]  │
│  │  └─ Relaciones: CORRELATES_WITH, TRIGGERS, LEAKS_INFO  │
│  ├─ Genera embeddings → Milvus                             │
│  │  └─ instruction_embeddings collection                    │
│  ├─ Persiste documento → MongoDB                           │
│  │  └─ measurements collection                              │
│  └─ Cachea en Redis                                         │
│     └─ measurement:batch_id → JSON (TTL: 24h)              │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ CONSULTA                                                     │
├──────────────────────────────────────────────────────────────┤
│ Usuario: "¿Qué instrucciones filtran energía?"             │
│                                                              │
│ LightRAG Query Engine:                                     │
│  ├─ Embed query con LLM → 384D vector                      │
│  ├─ Búsqueda en Milvus (top-10)                            │
│  ├─ Traversa Neo4j (pattern → instruction)                │
│  ├─ Recupera context de MongoDB                            │
│  ├─ Llama LLM con contexto                                 │
│  └─ Devuelve: Instrucciones + correlaciones de energía     │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ RESPUESTA AL USUARIO                                         │
├──────────────────────────────────────────────────────────────┤
│ {                                                            │
│   "answer": "Las siguientes instrucciones...",            │
│   "evidence": [instruction_ids],                          │
│   "confidence": 0.92,                                      │
│   "sources": ["measurements_batch_1", "neo4j_traversal"]  │
│ }                                                           │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Flujo: Ingesta Multimodal desde REMForge

```
INPUT: Imagen/Audio/Texto
         ▼
REMForge.forge_from_file()
  ├─ Detección automática de tipo
  ├─ Extracción de características
  │  ├─ CLIP embeddings (imágenes)
  │  ├─ Wav2Vec2 (audio)
  │  ├─ DeBERTa (texto)
  │  └─ Whisper (speech-to-text)
  ├─ Análisis fenomenológico
  │  ├─ Qualia detection
  │  ├─ Intentionality mapping
  │  ├─ Temporal structure analysis
  │  ├─ Affective valence
  │  └─ Spatial horizon
  └─ Genera REM JSON

REM JSON (salida)
  {
    "metadata": {
      "source": "image.png",
      "type": "IMAGE",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    "qualia": {
      "visual": ["bright", "vibrant", "complex"],
      "color_diversity": 0.85,
      "texture_complexity": 0.72,
      "dominant_colors": ["red", "blue"]
    },
    "intentionality": {
      "primary_mode": "SEEING_AS_OBJECT",
      "directedness": "FOCUSED"
    },
    "temporal_structure": {
      "duration": 0.0,
      "change_rate": 0.0,
      "rhythm": "STATIC"
    },
    "affective": {
      "valence": 0.65,
      "arousal": 0.58,
      "dominance": 0.72,
      "emotions": ["joy", "interest"]
    }
  }

         ▼
REMDashboard.visualize(rem_json)
  ├─ Gráfico de distribución modal
  ├─ Timeline de evolución temporal
  ├─ Mapa de affective space
  ├─ Análisis de qualia
  └─ Export a HTML interactive dashboard
```

### 3.3 Flujo: N8N Orchestration

```
┌─────────────────────────────────┐
│ N8N Workflow Webhook            │
│ POST /n8n/lightrag-trigger      │
└────────────┬────────────────────┘
             │
             ▼
   ┌─────────────────────────┐
   │ Parse webhook payload   │
   │ (instruction_id, params)│
   └────────┬────────────────┘
            │
            ▼
   ┌─────────────────────────────────────┐
   │ HTTP Call to LightRAG API           │
   │ POST /api/lightrag/query            │
   │ {                                   │
   │   "query": "Analyze instruction X"  │
   │ }                                   │
   └────────┬────────────────────────────┘
            │
            ▼
   ┌──────────────────────────────────────┐
   │ Process Response                     │
   │ - Extract answer                     │
   │ - Format for notification           │
   │ - Store in MongoDB                  │
   └────────┬───────────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ Send Notification            │
   │ (Slack/Email/Dashboard)      │
   └──────────────────────────────┘
```

---

## 4. MAPPING DE PUERTOS Y SERVICIOS

| Servicio | Puerto | Protocolo | Descripción |
|:---------|:-------|:----------|:-----------|
| LightRAG API | 9621 | HTTP | REST endpoint |
| Neo4j HTTP | 7474 | HTTP | Web UI |
| Neo4j Bolt | 7687 | Bolt | Client protocol |
| Milvus | 19530 | gRPC | Vector search |
| MongoDB | 27017 | BSON | Document store |
| Redis | 6379 | RESP | Cache + PubSub |
| N8N Editor | 5678 | HTTP | Workflow UI |
| Grafana | 3000 | HTTP | Dashboard |
| Renode Debugger | 9119 | TCP | Debug protocol (optional) |

---

## 5. CICLO DE VIDA DE UN ANÁLISIS COMPLETO

```
T=0s    ┌─────────────────────────────────────────────┐
        │ Usuario solicita análisis en Dashboard      │
        │ Input: "Analizar instrucción X"             │
        └────────┬────────────────────────────────────┘
                 │
T=0.1s  ┌────────▼────────────────────────────────────┐
        │ LightRAG Query Engine procesa query         │
        │ ├─ Embedding generation (0.05s)            │
        │ ├─ Milvus similarity search (0.02s)         │
        │ └─ Neo4j traversal (0.03s)                  │
        └────────┬────────────────────────────────────┘
                 │
T=0.2s  ┌────────▼────────────────────────────────────┐
        │ Recupera contexto desde MongoDB             │
        │ ├─ Query documents (0.05s)                  │
        │ └─ Aggregate data (0.02s)                   │
        └────────┬────────────────────────────────────┘
                 │
T=0.3s  ┌────────▼────────────────────────────────────┐
        │ LLM inference con contexto                  │
        │ ├─ Build prompt (0.01s)                     │
        │ ├─ API call a OpenAI/Ollama (0.3-5.0s)    │
        │ └─ Parse response (0.02s)                   │
        └────────┬────────────────────────────────────┘
                 │
T=5.3s  ┌────────▼────────────────────────────────────┐
        │ Cachea resultado en Redis                   │
        │ └─ Set with TTL 24h (0.01s)                │
        └────────┬────────────────────────────────────┘
                 │
T=5.4s  ┌────────▼────────────────────────────────────┐
        │ Devuelve respuesta a usuario                │
        │ {                                           │
        │   "answer": "La instrucción...",          │
        │   "processing_time": "5.4s",              │
        │   "source": "rag+llm",                     │
        │   "confidence": 0.92                       │
        │ }                                           │
        └────────────────────────────────────────────┘
```

---

## 6. MATRIZ DE DEPENDENCIAS

```
REMForge
  ├─ Depends on: torch, transformers, PIL, numpy
  └─ Optional: moviepy (para video)

LightRAG Core
  ├─ Depends on: neo4j, milvus-py, pymongo, redis-py
  ├─ Depends on: openai, ollama (LLM providers)
  └─ Depends on: httpx, uvicorn (async)

Renode Entity
  ├─ Depends on: renode (v1.14.0)
  ├─ Depends on: linux-headers-generic (kernel module)
  ├─ Depends on: scipy, numpy (análisis)
  └─ Depends on: python-can (para instrumentación)

Eclosion Events
  ├─ Depends on: asyncio, aiohttp
  └─ Depends on: pydantic (schemas)

FastAPI Server
  ├─ Depends on: fastapi, uvicorn, pydantic
  ├─ Depends on: LightRAG core
  └─ Depends on: all storage backends

React WebUI
  ├─ Depends on: React 19, TypeScript, Vite
  ├─ Depends on: Tailwind CSS, Chart.js
  └─ Depends on: axios (HTTP client)
```

---

## 7. CHECKLIST DE VERIFICACIÓN DEL SISTEMA

**Pre-deployment:**
- [ ] Neo4j accessible via bolt://localhost:7687
- [ ] Milvus health check passes (port 19530)
- [ ] MongoDB initialized with indexes
- [ ] Redis running and connectable
- [ ] LightRAG API responds to `/health`
- [ ] Renode binary available in container

**Post-deployment:**
- [ ] All 6 containers running (docker ps)
- [ ] No critical logs in any container
- [ ] Query latency < 5s (median)
- [ ] Cache hit rate > 30% (after warmup)
- [ ] Renode simulation completes in < 120s
- [ ] WebUI loads without errors

**Troubleshooting:**
1. Neo4j won't start → Check disk space, increase heap
2. Milvus fails health check → Verify FAISS installation
3. LightRAG queries slow → Check Neo4j index creation
4. Renode simulation times out → Check kernel module load
5. Cache hit rate low → Increase Redis memory or TTL

---

Este mapa proporciona una visión 360° del ecosistema Dasein y cómo interactúan todos sus componentes.
