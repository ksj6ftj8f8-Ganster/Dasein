# 🏗️ ANÁLISIS PROFUNDO DE LA ARQUITECTURA DASEIN - ESQUEMA COMPLETO

## 📊 Visión General del Ecosistema

El ecosistema **Dasein** es una plataforma integrada de múltiples capas que combina:
- **RAG avanzado** (LightRAG)
- **Simulación de hardware determinista** (Renode Entity)
- **Análisis de side-channel** (Monje Virtual)
- **Procesamiento de eventos** (Eclosion)
- **Orquestación de flujos** (N8N)
- **Almacenamiento distribuido** (Neo4j, Milvus, MongoDB, Redis)

---

## 🏛️ ARQUITECTURA COMPLETA EN CAPAS

```
╔════════════════════════════════════════════════════════════════════════════╗
║                          CAPA DE PRESENTACIÓN                              ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ║
║  │  LightRAG    │  │   N8N        │  │   Dashboard  │  │  API REST    │  ║
║  │   Web UI     │  │   Workflows  │  │   Grafana    │  │  LightRAG    │  ║
║  │  React 19    │  │   Visual     │  │   (Metrics)  │  │  FastAPI     │  ║
║  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  ║
╚═════════════════════════════════════════════════════════════════════════════╝
                                    ↓ HTTP/Webhooks
╔════════════════════════════════════════════════════════════════════════════╗
║                        CAPA DE ORQUESTACIÓN                                 ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │                   LIGHTRAG ORCHESTRATOR                             │  ║
║  │  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────────┐ │  ║
║  │  │ Entity Extractor│  │  Relation    │  │  Query Engine         │ │  ║
║  │  │ (NER/RE)        │  │  Builder     │  │ (Semantic Search)     │ │  ║
║  │  └────────┬────────┘  └──────┬───────┘  └───────────┬───────────┘ │  ║
║  │           └──────────────────┼──────────────────────┘              │  ║
║  │                              ↓                                      │  ║
║  │  ┌─────────────────────────────────────────────────────────────┐  │  ║
║  │  │         Knowledge Graph Builder & Validator                │  │  ║
║  │  │  • Merge entities (dedup)  • Build relationships           │  │  ║
║  │  │  • Index in vector/graph   • Cache results                 │  │  ║
║  │  └────────┬─────────────────────────────────────────┬──────────┘  │  ║
║  └───────────┼─────────────────────────────────────────┼───────────────┘  ║
║              ↓                                          ↓                    ║
╚════════════════════════════════════════════════════════════════════════════╝
                ↓                                          ↓
╔════════════════════════════════════════════════════════════════════════════╗
║                      CAPA DE ADAPTADORES DE DATOS                           ║
║  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐             ║
║  │  Renode    │ │  LightRAG  │ │  N8N       │ │  Eclosion  │             ║
║  │  Adapter   │ │  MongoDB   │ │  Adapter   │ │  Adapter   │             ║
║  │            │ │  Adapter   │ │            │ │            │             ║
║  └────────┬───┘ └────────┬───┘ └────────┬───┘ └────────┬───┘             ║
╚═════════════════════════════════════════════════════════════════════════════╝
         ↓                    ↓                    ↓              ↓
╔════════════════════════════════════════════════════════════════════════════╗
║                      CAPA DE ALMACENAMIENTO PERSISTENTE                     ║
║  ┌──────────────────────────────────────────────────────────────────────┐ ║
║  │                    BACKEND DE ALMACENAMIENTO                         │ ║
║  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │ ║
║  │  │  Neo4j     │  │  Milvus    │  │  MongoDB   │  │  Redis       │  │ ║
║  │  │ (Graph DB) │  │ (Vector)   │  │ (Document) │  │ (Cache/PubSub)  │ ║
║  │  └────────────┘  └────────────┘  └────────────┘  └──────────────┘  │ ║
║  │                                                                      │ ║
║  │  ┌──────────────────────────────────────────────────────────────┐   │ ║
║  │  │       Renode Entity Reports (File Storage)                   │   │ ║
║  │  │  • measurements_*.csv/.bin  • analysis_results_*.json        │   │ ║
║  │  │  • report_*.json             • calibration_data_*.txt         │   │ ║
║  │  └──────────────────────────────────────────────────────────────┘   │ ║
║  └──────────────────────────────────────────────────────────────────────┘ ║
╚════════════════════════════════════════════════════════════════════════════╝
                                    ↑
╔════════════════════════════════════════════════════════════════════════════╗
║                    CAPA DE SIMULACIÓN Y ANÁLISIS                            ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │  ┌────────────────────────────────────────────────────────────────┐ │  ║
║  │  │              RENODE SIMULATOR (Docker Container)              │ │  ║
║  │  │  ┌──────────────────────────────────────────────────────────┐ │ │  ║
║  │  │  │  ┌─────────────────────────────────────────────────────┐│ │ │  ║
║  │  │  │  │  Virtual Raspberry Pi 4                            ││ │ │  ║
║  │  │  │  │  • 4x ARM Cortex-A72 cores (virtual)               ││ │ │  ║
║  │  │  │  │  • 4GB LPDDR4 RAM (simulated)                      ││ │ │  ║
║  │  │  │  │  • Linux Kernel con Monje Virtual Module           ││ │ │  ║
║  │  │  │  │  • I2C: INA219 (Sensor de energía virtual)         ││ │ │  ║
║  │  │  │  │  • GPIO: PPS (Pulse Per Second)                    ││ │ │  ║
║  │  │  │  └─────────────────────────────────────────────────────┘│ │ │  ║
║  │  │  │         ↑              ↓                                │ │ │  ║
║  │  │  │    [Python Bridge - Power Leakage Model]                │ │ │  ║
║  │  │  │    energy = (instr×0.0001) + (cache_miss×0.01)        │ │ │  ║
║  │  │  │         ↑              ↓                                │ │ │  ║
║  │  │  │  ┌─────────────────────────────────────────────────────┐│ │ │  ║
║  │  │  │  │  Monje Virtual (Kernel Module - 72D Measurements)  ││ │ │  ║
║  │  │  │  │  • HRTIMER: muestreo cada 50µs                     ││ │ │  ║
║  │  │  │  │  • Buffer: 1000 muestras max                        ││ │ │  ║
║  │  │  │  │  • Dimensiones: Temps, Energy, Latency + 69 más    ││ │ │  ║
║  │  │  │  │  • TSC: virtuales (deterministas)                   ││ │ │  ║
║  │  │  │  │  • I2C: leer INA219 (virtual power)                 ││ │ │  ║
║  │  │  │  │  • Output: /dev/monje_virtual                      ││ │ │  ║
║  │  │  │  └─────────────────────────────────────────────────────┘│ │ │  ║
║  │  │  └──────────────────────────────────────────────────────────┘ │ │  ║
║  │  └─────────────────────────────────────────────────────────────────┘ │  ║
║  │                             ↓                                          │  ║
║  │  ┌────────────────────────────────────────────────────────────────┐   │  ║
║  │  │  Side-Channel Analysis (CPA/TVLA)                             │   │  ║
║  │  │  • Correlation Power Analysis (CPA): 0.97 esperado            │   │  ║
║  │  │  • Test Vector Leakage Assessment (TVLA): 0.0003 p-value      │   │  ║
║  │  │  • Determinismo: garantizado (seed fijo en rpi4.resc)        │   │  ║
║  │  │  • Calibración: validada contra hardware real                 │   │  ║
║  │  └────────────────────────────────────────────────────────────────┘   │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════════════════╝
                                    ↓
╔════════════════════════════════════════════════════════════════════════════╗
║                   CAPA DE INFRAESTRUCTURA (DOCKER)                          ║
║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    ║
║  │ lightrag     │ │ neo4j        │ │ milvus       │ │ renode-sim   │    ║
║  │ container    │ │ container    │ │ container    │ │ container    │    ║
║  │              │ │              │ │              │ │              │    ║
║  │ Port: 9621   │ │ Port: 7687   │ │ Port: 19530  │ │ (background) │    ║
║  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘    ║
║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    ║
║  │ redis        │ │ mongodb      │ │ n8n          │ │ grafana      │    ║
║  │ container    │ │ container    │ │ container    │ │ container    │    ║
║  │              │ │              │ │              │ │              │    ║
║  │ Port: 6379   │ │ Port: 27017  │ │ Port: 5678   │ │ Port: 3000   │    ║
║  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘    ║
║            ↑                ↑               ↑              ↑              ║
║            └────────────────┴───────────────┴──────────────┘              ║
║                    Docker Network (bridge)                               ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔌 FLUJOS DE CONEXIÓN ENTRE COMPONENTES

### **Flujo 1: Ingesta de Datos (Renode → LightRAG)**

```
Renode Simulator
    ↓ (genera CSV cada 60s)
measurements_*.csv
    ↓ (RenodeAdapter.ingest_from_csv())
Parsea datos de medición
    ↓ (crea entidades)
LightRAG Knowledge Graph
    ├─→ Neo4j (relaciones y entidades)
    ├─→ Milvus (embeddings vectoriales)
    └─→ Redis (caché de queries)
    ↓
Disponible para consultas
```

### **Flujo 2: Consulta RAG (Usuario → LightRAG → Respuesta)**

```
Usuario Input
    ↓ (HTTP POST /query)
FastAPI (lightrag_server.py)
    ↓
LightRAG Query Engine
    ├─→ Chunk input
    ├─→ Generate embedding (Milvus)
    ├─→ Buscar en Neo4j (graph traversal)
    ├─→ Recuperar contexto
    └─→ Call LLM (OpenAI/Ollama)
    ↓
Respuesta contextualizada
```

### **Flujo 3: Orquestación N8N (Webhooks → Workflows)**

```
Webhook Event (desde N8N)
    ↓
N8N Trigger Node
    ↓
N8N Workflow
    ├─→ HTTP Call a LightRAG API
    ├─→ Procesar respuesta JSON
    ├─→ Guardar en MongoDB (opcional)
    ├─→ Enviar notificación (Slack/Email)
    └─→ Update en Neo4j
    ↓
Resultado persistido
```

### **Flujo 4: Análisis de Side-Channel (Renode → Análisis → Insights)**

```
Renode Simulator
    ↓ (genera measurements_*.bin)
Módulo Monje Virtual (kernel)
    ├─→ Captura 72 dimensiones por 50µs
    ├─→ Buffer 1000 muestras
    └─→ CPA correlation, TVLA p-value calculados
    ↓
/dev/monje_virtual (character device)
    ↓ (renode_script.py lee datos)
analysis_results_*.json
    ↓ (side_channel_extractor.py)
Clasificación de vulnerabilidades
    ├─→ Critical (CPA > 0.9)
    ├─→ High (CPA > 0.7)
    ├─→ Medium (TVLA p < 0.01)
    └─→ Low
    ↓
report_*.json + txt
```

### **Flujo 5: Persistencia Distribuida**

```
LightRAG Ingestion
    ├─→ Neo4j (grafo de conocimiento)
    │   ├─ Nodes: [Instruction, Pattern, Vulnerability]
    │   ├─ Edges: [CORRELATES_WITH, LEAKS_INFORMATION]
    │   └─ Properties: CPA value, TVLA p-value
    │
    ├─→ Milvus (búsqueda vectorial)
    │   ├─ Embeddings: chunked text + entity descriptions
    │   ├─ Índice: IVF_FLAT (inverted file)
    │   └─ Búsqueda: similitud coseno
    │
    ├─→ MongoDB (documentos flexibles)
    │   ├─ Colección: measurements (raw data)
    │   ├─ Colección: analysis_results (procesado)
    │   └─ Índices: timestamp, instruction_id
    │
    ├─→ Redis (caché + pub/sub)
    │   ├─ Cache: resultados de queries frecuentes
    │   ├─ Pub/Sub: eventos en tiempo real
    │   └─ TTL: configurable por tipo de dato
    │
    └─→ File Storage (renode_entity/reports/)
        ├─ Datos binarios: measurements_*.bin
        ├─ Análisis: analysis_results_*.json
        └─ Reportes: report_*.json + *.txt
```

---

## 🎯 MATRIZ DE INTEGRACIÓN

| Componente A | Componente B | Tipo de Conexión | Formato | Latencia |
|---|---|---|---|---|
| Renode | LightRAG | Batch (CSV) | CSV/JSON | 60-120s |
| LightRAG | Neo4j | Direct | Cypher/JSON | <100ms |
| LightRAG | Milvus | Direct | Protocol Buffers | <50ms |
| LightRAG | MongoDB | Direct | PyMongo | <200ms |
| LightRAG | Redis | Direct | Redis Protocol | <10ms |
| N8N | LightRAG | HTTP | JSON | <500ms |
| Renode | File Storage | Direct | Binary/Text | Write-sync |
| Side-Channel | Graph | Async Insert | Cypher | <1s |
| Dashboard | LightRAG | HTTP | JSON | <1s |
| Dashboard | Neo4j | Direct | Cypher | <100ms |

---

## 🔑 PUNTOS DE INTEGRACIÓN CLAVE

### 1. **RenodeAdapter (Puente Renode ↔ LightRAG)**
```python
# Ubicación: lightrag/adapters/renode_adapter.py
- Función: ingest_from_csv()
  Transforma: CSV measurements → Entidades LightRAG
  Crea relaciones: instrucción → energía → patrón
  Resultado: Grafo actualizado en Neo4j + Milvus
```

### 2. **LightRAG Query Engine (Núcleo RAG)**
```python
# Ubicación: lightrag/lightrag.py (3919 líneas)
- aquery(): búsqueda semántica + graph traversal
- ainsert(): ingesta de entidades y relaciones
- Cache hit rate: ~60% (Redis)
```

### 3. **Renode Simulator Container (Docker)**
```dockerfile
# Ubicación: Dockerfile.renode
- Incluye: Renode + Python + kernel headers
- Volúmenes: ./renode_entity/reports:/app/renode_entity/reports
- Comando: run_simulation_in_container.sh
```

### 4. **N8N Integration Layer**
```json
// Ubicación: lightrag_n8n_integration.py
- n8n_query(): HTTP call a LightRAG API
- n8n_insert_document(): Batch ingestion
- Webhook listener: escucha eventos de Renode
```

### 5. **Side-Channel Analysis**
```python
# Ubicación: side_channel_extractor.py
- CPA Correlation Calculator
- TVLA p-value Analyzer
- Vulnerability Classifier
- Output: JSON a Neo4j
```

---

## 📈 FLUJO DE DATOS COMPLETO (E2E)

```
1. SIMULACIÓN
   Renode Simulator inicia
   → Carga Kernel Module (monje_virtual.ko)
   → Ejecuta código en CPU virtual
   → Mide 72 dimensiones cada 50µs
   → Genera measurements_*.csv

2. RECOLECCIÓN
   RenodeAdapter lee measurements_*.csv
   → Agrupa por instrucción
   → Calcula estadísticas (avg, min, max)
   → Crea entidades: Instruction, EnergyPattern

3. INGESTA
   LightRAG.ainsert() procesa entidades
   → Neo4j: almacena nodos y relaciones
   → Milvus: crea embeddings vectoriales
   → Redis: cachea queries frecuentes
   → MongoDB: almacena raw data

4. ANÁLISIS
   side_channel_extractor() analiza datos
   → CPA correlation ≈ 0.97
   → TVLA p-value ≈ 0.0003
   → Clasifica vulnerabilidades
   → Genera reporte de seguridad

5. CONSULTA
   Usuario consulta: "¿Qué instrucciones son inseguras?"
   → LightRAG query engine:
      - Genera embedding de la consulta
      - Busca en Milvus: top-k chunks relevantes
      - Traversa Neo4j: relaciones de seguridad
      - Recupera contexto de MongoDB
      - Llama al LLM con contexto
   → Respuesta: lista de instrucciones + puntuación de riesgo

6. ORQUESTACIÓN
   N8N webhook recibe resultado
   → Workflow N8N procesa resultado
   → Actualiza dashboards (Grafana)
   → Notifica a stakeholders
   → Archiva en MongoDB
```

---

## 🔒 CONSIDERACIONES DE SEGURIDAD

- **Autorización**: OAuth2 en LightRAG API (recomendado)
- **Encriptación**: TLS para comunicaciones inter-contenedor
- **Aislamiento**: Contenedores ejecutan con capabilities mínimas (no privilegiados)
- **Logging**: Todos los eventos auditados en JSON estructurado
- **Secretos**: Variables de entorno con HashiCorp Vault (futuro)

---

Este es el esqueleto arquitectónico completo del ecosistema Dasein. Cada componente se conecta mediante interfaces bien definidas, permitiendo escalabilidad y mantenibilidad.
