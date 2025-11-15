# 🎨 ESQUELETOS Y DIAGRAMAS VISUALES - ECOSISTEMA DASEIN

## 1. SKELETON COMPLETO (Vista Lateral)

```
Windows Host (WSL2)
│
├─ File System
│  └─ /workspaces/Dasein/
│     ├─ lightrag/              ← Core RAG framework
│     ├─ renode_entity/         ← Hardware simulation
│     │  ├─ src/monje_virtual.c ← Kernel module source
│     │  ├─ rpi4.resc           ← Platform description
│     │  ├─ renode_script.py    ← Orchestrator
│     │  └─ reports/            ← Output files (mounted)
│     ├─ lightrag_source/       ← LightRAG submodule
│     ├─ examples/              ← Use cases
│     └─ docs/                  ← Documentation
│
└─ Docker Daemon
   │
   ├─ Container: lightrag (Port 9621)
   │  ├─ Image: ghcr.io/hkuds/lightrag:latest
   │  ├─ Volume: ./data/rag_storage → /app/data/rag_storage
   │  └─ Depends on: neo4j, milvus, redis
   │
   ├─ Container: neo4j (Port 7687)
   │  ├─ Image: neo4j:5.15-enterprise
   │  ├─ Storage: neo4j_data volume
   │  └─ Network: bridge
   │
   ├─ Container: milvus (Port 19530)
   │  ├─ Image: milvusdb/milvus:v0.19.7
   │  ├─ Storage: milvus_data volume
   │  └─ Health: TCP 9091
   │
   ├─ Container: redis (Port 6379)
   │  ├─ Image: redis:7-alpine
   │  ├─ Storage: redis_data volume
   │  └─ Health: PING command
   │
   ├─ Container: mongodb (Port 27017)
   │  ├─ Image: mongo:latest
   │  ├─ Storage: mongodb_data volume
   │  └─ Indexes: timestamp, instruction_id
   │
   ├─ Container: renode-simulator (Background)
   │  ├─ Image: dasein-renode-simulator:latest
   │  ├─ Build: Dockerfile.renode
   │  ├─ Volumes: 
   │  │  ├─ ./renode_entity → /app/renode_entity
   │  │  └─ ./renode_entity/reports → /app/renode_entity/reports
   │  ├─ Entrypoint: run_simulation_in_container.sh
   │  └─ Privileged: false (por defecto)
   │
   ├─ Container: n8n (Port 5678)
   │  ├─ Image: n8nio/n8n:latest
   │  └─ Webhooks: reciben eventos de Renode
   │
   └─ Container: grafana (Port 3000)
       ├─ Image: grafana/grafana:latest
       ├─ DataSources: Neo4j, Prometheus
       └─ Dashboards: Métricas de simulación + RAG

Network (bridge): Todos los contenedores comunicados vía DNS interno
```

---

## 2. FLUJO DE DECISIÓN - ¿Qué sistema procesa qué?

```
┌─────────────────────────────────────────────────────────────┐
│ DATO INGRESA AL ECOSISTEMA                                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─ ¿Es de Renode?
             │  ├─ YES: CSV/BIN → RenodeAdapter → LightRAG
             │  └─ NO: ↓
             │
             ├─ ¿Es usuario query?
             │  ├─ YES: HTTP POST → FastAPI → LightRAG Query Engine
             │  └─ NO: ↓
             │
             ├─ ¿Es evento N8N?
             │  ├─ YES: Webhook → N8N Workflow → HTTP to LightRAG
             │  └─ NO: ↓
             │
             ├─ ¿Es para side-channel analysis?
             │  ├─ YES: measurements → CPA/TVLA analyzer → Neo4j
             │  └─ NO: ↓
             │
             └─ ALMACENAR EN:
                ├─ Neo4j       (si es entidad/relación)
                ├─ Milvus      (si es texto/embedding)
                ├─ MongoDB     (si es documento flexible)
                ├─ Redis       (si es caché)
                └─ File System (si es binario/reporte)
```

---

## 3. CICLO DE VIDA DE UNA MEDICIÓN RENODE

```
Step 1: SIMULACIÓN (t=0s)
┌─────────────────────────────────────────┐
│ Renode Simulator arranca                │
│ ├─ carga rpi4.resc                      │
│ ├─ inicia 4 cores ARM virtuales         │
│ ├─ carga Linux kernel (simulado)        │
│ └─ monta monje_virtual.ko               │
└────────┬────────────────────────────────┘
         │
Step 2: MEDICIÓN (t=0-60s, cada 50µs)
┌─────────────────────────────────────────┐
│ monje_virtual.ko sampling                │
│ ├─ HRTIMER dispara cada 50µs            │
│ ├─ Captura: TSC, temperatura, energía   │
│ ├─ Calcula 72 dimensiones               │
│ ├─ Almacena en buffer (max 1000)       │
│ └─ I2C read INA219 (power sensor)      │
└────────┬────────────────────────────────┘
         │ (1000 muestras = 50ms)
Step 3: LECTURA (t=61s)
┌─────────────────────────────────────────┐
│ renode_script.py → cat /dev/monje_virtual
│ └─ Copia buffer a measurements.csv     │
└────────┬────────────────────────────────┘
         │
Step 4: ANÁLISIS (t=62s)
┌─────────────────────────────────────────┐
│ side_channel_extractor.py                │
│ ├─ CPA correlation calculation          │
│ ├─ TVLA p-value calculation             │
│ ├─ Vulnerability classification         │
│ └─ Genera analysis_results.json         │
└────────┬────────────────────────────────┘
         │
Step 5: INGESTA (t=63s)
┌─────────────────────────────────────────┐
│ RenodeAdapter.ingest_from_csv()         │
│ ├─ Parsea CSV                           │
│ ├─ Crea entidades LightRAG              │
│ ├─ Inserta en Neo4j                     │
│ ├─ Genera embeddings en Milvus          │
│ └─ Cachea en Redis                      │
└────────┬────────────────────────────────┘
         │
Step 6: CONSULTA (t=64s+, a demanda)
┌─────────────────────────────────────────┐
│ Usuario consulta:                       │
│ "¿Qué instrucciones son riesgosas?"     │
│                                         │
│ LightRAG Query Engine:                  │
│ ├─ Embed query en Milvus                │
│ ├─ Busca top-k vectores similares       │
│ ├─ Traversa Neo4j (1-3 hops)           │
│ ├─ Recupera contexto de MongoDB         │
│ ├─ Llama LLM con contexto               │
│ └─ Devuelve: respuesta + vulnerabilidades
└─────────────────────────────────────────┘
```

---

## 4. ÁRBOL DE DEPENDENCIAS

```
LightRAG (Núcleo)
│
├─ Adaptadores de Entrada
│  ├─ RenodeAdapter (CSV/BIN)
│  ├─ MongoDBAdapter (documentos)
│  ├─ N8NAdapter (webhooks)
│  └─ FileAdapter (text/PDF)
│
├─ Motores Internos
│  ├─ EntityExtractor (NER)
│  ├─ RelationshipBuilder (RE)
│  ├─ QueryEngine (semantic search)
│  └─ LLMCaller (OpenAI/Ollama)
│
├─ Backends de Almacenamiento
│  ├─ Neo4jStorage (grafo)
│  ├─ MilvusStorage (vectores)
│  ├─ MongoDBStorage (documentos)
│  └─ RedisStorage (caché)
│
└─ Utilidades
   ├─ Logger
   ├─ Chunker (text splitting)
   ├─ TokenCounter
   └─ ConfigManager
```

---

## 5. MATRIZ DE LLAMADAS ENTRE COMPONENTES

```
                   Neo4j   Milvus  MongoDB  Redis  Renode  N8N
LightRAG          [W]      [W]     [W]      [RW]   [R]     [R]
RenodeAdapter     [W]      [W]     [W]      [W]    [R]     [-]
SideChannelExt    [W]      [-]     [W]      [-]    [R]     [-]
N8NWorkflow       [R]      [-]     [RW]     [R]    [-]     [W]
Dashboard         [R]      [-]     [R]      [R]    [-]     [-]
FileSystem        [-]      [-]     [-]      [-]    [RW]    [-]

[R] = Read  [W] = Write  [RW] = Read-Write  [-] = No access
```

---

## 6. TOPOLOGÍA DE DATOS (Esquema Conceptual)

```
NEO4J (Property Graph)
├─ Nodos
│  ├─ Instruction
│  │  ├─ id: string
│  │  ├─ name: string
│  │  ├─ avg_energy: float
│  │  ├─ avg_temperature: float
│  │  └─ sample_count: int
│  │
│  ├─ EnergyPattern
│  │  ├─ pattern_type: string (HIGH/MEDIUM/LOW)
│  │  ├─ correlation: float
│  │  └─ instructions: [string]
│  │
│  └─ SecurityVulnerability
│     ├─ name: string
│     ├─ cpa_value: float
│     ├─ tvla_p_value: float
│     └─ severity: string (CRITICAL/HIGH/MEDIUM/LOW)
│
└─ Relaciones
   ├─ CORRELATES_WITH (weight: correlation coefficient)
   ├─ TRIGGERS (target: pattern)
   ├─ LEAKS_INFORMATION (severity: measured)
   └─ MITIGATED_BY (effectiveness: %)

MILVUS (Vector Search)
├─ Collection: instruction_embeddings
│  ├─ id: int64
│  ├─ instruction_id: varchar
│  ├─ embedding: float_vector[384]  ← de OpenAI/Ollama
│  └─ metadata: json
│
└─ Collection: measurement_embeddings
   ├─ id: int64
   ├─ measurement_id: varchar
   ├─ embedding: float_vector[384]
   └─ metadata: json

MONGODB (Document Store)
├─ measurements collection
│  ├─ _id: ObjectId
│  ├─ timestamp: Date
│  ├─ instruction_id: string
│  ├─ energy: float
│  ├─ temperature: float
│  ├─ dimensions: [float] (72 values)
│  └─ indexed: {timestamp: 1, instruction_id: 1}
│
└─ analysis_results collection
   ├─ _id: ObjectId
   ├─ measurement_batch_id: string
   ├─ cpa_correlation: float
   ├─ tvla_p_value: float
   ├─ timestamp: Date
   └─ indexed: {timestamp: 1}

REDIS (Cache + PubSub)
├─ Keys
│  ├─ query:hash → {result JSON}  [TTL: 1h]
│  ├─ instruction:id → {data JSON} [TTL: 24h]
│  └─ metric:latest → {value}      [TTL: 5m]
│
└─ Channels (PubSub)
   ├─ renode:measurement_complete
   ├─ analysis:vulnerability_detected
   └─ lightrag:query_cached

FILE SYSTEM (reports/)
├─ measurements_*.csv
│  ├─ timestamp, temperature, energy, latency, dim_0...dim_71
│  └─ 1000+ rows (dependiendo de duración)
│
├─ analysis_results_*.json
│  ├─ cpa_correlation, tvla_p_value, sample_count, dimensions
│  └─ determinism, calibration_status
│
└─ report_*.json
   ├─ summary, analysis_results, configuration
   └─ notes, next_steps
```

---

## 7. DEPENDENCIAS DE INICIO (Docker Compose Boot Order)

```
Fase 1: Storage Layer (Paralelo)
┌─────────────────────────────────────────────────────────┐
│ docker-compose up -d neo4j milvus mongodb redis         │
│                                                          │
│ neo4j        [████████████] 30s (health check)          │
│ milvus       [████████████] 15s (health check)          │
│ mongodb      [████████] 10s (health check)              │
│ redis        [████] 5s (health check)                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
         ↓ (todos healthy)
Fase 2: Application Layer
┌─────────────────────────────────────────────────────────┐
│ docker-compose up -d lightrag n8n grafana              │
│                                                          │
│ lightrag     [████████████████] 20s                     │
│ n8n          [████████] 10s                             │
│ grafana      [████] 5s                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
         ↓ (todos ready)
Fase 3: Simulation Layer (Opcional, Background)
┌─────────────────────────────────────────────────────────┐
│ docker-compose up -d renode-simulator                  │
│                                                          │
│ renode-sim   [████████████████████] 60s (ejecución)    │
│              (genera reports + ingesta a LightRAG)      │
│                                                          │
└─────────────────────────────────────────────────────────┘

Total: ~120 segundos hasta sistema completamente operativo
```

---

## 8. PUNTOS DE FALLO Y RECUPERACIÓN

```
Escenario 1: Neo4j se cae
├─ Impacto: ❌ Queries fails, ❌ Graph traversal fails
├─ Recuperación: 
│  ├─ docker restart neo4j
│  ├─ Datos persisten en volumen
│  └─ ~30s para recovery
└─ Prevención: Backup automático nightly

Escenario 2: Milvus se cae
├─ Impacto: ⚠️ Búsqueda vectorial falla, caché en Redis parcial
├─ Recuperación:
│  ├─ docker restart milvus
│  ├─ Reingenerar embeddings desde Neo4j
│  └─ ~15s para recovery
└─ Prevención: Réplica de Milvus (cluster mode)

Escenario 3: Redis se cae
├─ Impacto: ⚠️ Caché vacío, pero datos persisten
├─ Recuperación:
│  ├─ docker restart redis
│  ├─ Caché se reconstruye dinámicamente
│  └─ ~5s para recovery
└─ Prevención: Persistencia RDB/AOF habilitada

Escenario 4: Renode Simulator falla
├─ Impacto: ⚠️ Nueva medición no disponible
├─ Recuperación:
│  ├─ docker restart renode-simulator
│  ├─ Último informe disponible en reports/
│  └─ ~60s para nueva medición
└─ Prevención: Logs auditables en renode_simulation.log

Escenario 5: LightRAG API cae
├─ Impacto: ❌ Usuarios no pueden consultar
├─ Recuperación:
│  ├─ docker restart lightrag
│  ├─ Estado sincronizado desde Neo4j
│  └─ ~20s para recovery
└─ Prevención: Health check endpoint + alertas
```

---

Este conjunto completo de esqueletos y diagramas permite visualizar cada aspecto del ecosistema Dasein, desde la arquitectura física hasta los flujos de datos y escenarios de recuperación.
