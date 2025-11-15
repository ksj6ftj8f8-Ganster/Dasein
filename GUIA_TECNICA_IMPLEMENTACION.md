# 🛠️ GUÍA TÉCNICA DE IMPLEMENTACIÓN - RENODE + LIGHTRAG
**Documento:** Guía Step-by-Step | **Versión:** 1.0 | **Audiencia:** Equipo Técnico

---

## 📋 ÍNDICE

1. [Quick Start (15 min)](#quick-start)
2. [Arquitectura Detallada](#arquitectura)
3. [Implementación Step-by-Step](#implementación)
4. [Testing & Validation](#testing)
5. [Troubleshooting](#troubleshooting)
6. [Performance Tuning](#performance)

---

## 🚀 QUICK START (15 min)

### Prerequisitos
```bash
# Ambiente
- Linux 5.15+ (para kernel module)
- Python 3.9+
- Docker & Docker Compose
- Renode simulator

# Paquetes
- gcc, make, linux-headers
- python-dev
- curl, jq
```

### Instalación Rápida

```bash
# 1. Clonar y preparar
cd /workspaces/Dasein
python3 -m venv venv
source venv/bin/activate
pip install -e ".[api]"

# 2. Compilar kernel module
cd renode_entity/scripts
./build.sh
sudo insmod ../src/monje_virtual.ko

# 3. Iniciar LightRAG
lightrag-server --host 0.0.0.0 --port 8000

# 4. Ejecutar Renode
cd renode_entity
python3 renode_script.py --duration 10 --output reports/

# 5. Crear adaptador y ingestar
python3 /workspaces/Dasein/lightrag/adapters/renode_adapter.py

# 6. Consultar
curl http://localhost:8000/query \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Cuál es la instrucción con máximo consumo de energía?"}'
```

**Resultado esperado:** JSON con respuesta contextualizada del grafo

---

## 🏗️ ARQUITECTURA DETALLADA

### Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  Python Scripts | REST API | Web UI                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│               ORCHESTRATION LAYER (LightRAG)                │
│  • Entity Extraction  • Relation Building                   │
│  • Query Processing   • Response Generation                 │
└────────┬──────────────────┬──────────────────┬──────────────┘
         │                  │                  │
    ┌────▼──────┐   ┌──────▼────┐   ┌────────▼──────┐
    │ Vector DB │   │ Graph DB  │   │  Cache Layer  │
    │ (Milvus)  │   │ (Neo4j)   │   │ (Redis)       │
    │           │   │           │   │               │
    └───────────┘   └───────────┘   └───────────────┘

┌─────────────────────────────────────────────────────────────┐
│            DATA INGESTION LAYER (Renode Adapter)            │
│  CSV Parser | Entity Creator | Relationship Builder         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         SIMULATION LAYER (Renode Entity)                    │
│  • Kernel Module (monje_virtual.ko)                         │
│  • CPU Emulation (4x Cortex-A72)                            │
│  • Power Leakage Model (Python Bridge)                      │
│  • Measurement Buffer (72 dimensions)                       │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
Renode Simulation (50µs sampling)
        ↓
Kernel Module (captura en buffer)
        ↓
Aplicación usuario (lee /dev/monje_virtual)
        ↓
CSV File (measurements.csv)
        ↓
Renode Adapter
        ├─ Parse CSV
        ├─ Extract entities
        ├─ Build relationships
        └─ Calculate statistics
        ↓
LightRAG Ingestion
        ├─ Create nodes
        ├─ Store vectors
        ├─ Index graph
        └─ Cache results
        ↓
Knowledge Graph (queryable)
```

---

## 🔧 IMPLEMENTACIÓN STEP-BY-STEP

### Step 1: Crear Adaptador Renode

**Archivo:** `/workspaces/Dasein/lightrag/adapters/renode_adapter.py`

```python
#!/usr/bin/env python3
"""Adaptador para Renode Entity → LightRAG"""

import asyncio
import csv
from pathlib import Path
from typing import Dict, List
import logging
from lightrag import LightRAG

logger = logging.getLogger(__name__)

class RenodeAdapter:
    """Convierte datos Renode en entidades LightRAG"""
    
    def __init__(self, lightrag_instance: LightRAG):
        self.rag = lightrag_instance
        self.measurements = []
        
    async def ingest_from_csv(self, csv_path: Path) -> Dict:
        """Ingestar mediciones desde CSV generado por Renode"""
        
        logger.info(f"Ingesting measurements from {csv_path}")
        
        # Leer CSV
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.measurements.append(row)
        
        # Agrupar por instrucción
        by_instr = {}
        for m in self.measurements:
            instr_id = m.get('instruction_id', 'unknown')
            if instr_id not in by_instr:
                by_instr[instr_id] = []
            by_instr[instr_id].append(m)
        
        # Ingestar entidades
        stats = await self._ingest_entities(by_instr)
        
        # Ingestar relaciones
        await self._ingest_relationships(by_instr)
        
        logger.info(f"Ingestion completed: {stats}")
        return stats
    
    async def _ingest_entities(self, by_instr: Dict) -> Dict:
        """Crear entidades de instrucción"""
        stats = {
            'entities': 0,
            'total_samples': sum(len(v) for v in by_instr.values())
        }
        
        for instr_id, samples in by_instr.items():
            # Calcular estadísticas
            energies = [float(s.get('energy', 0)) for s in samples]
            temps = [float(s.get('temperature', 0)) for s in samples]
            latencies = [float(s.get('latency', 0)) for s in samples]
            
            avg_energy = sum(energies) / len(energies) if energies else 0
            avg_temp = sum(temps) / len(temps) if temps else 0
            max_latency = max(latencies) if latencies else 0
            
            # Crear documento para LightRAG
            doc_text = f"""
            Instruction ID: {instr_id}
            Type: Assembly Instruction
            Total Executions: {len(samples)}
            Average Energy Consumption: {avg_energy:.6f} Joules
            Average Temperature: {avg_temp:.2f} Celsius
            Maximum Latency: {max_latency:.3f} microseconds
            Energy Range: {min(energies):.6f} to {max(energies):.6f} Joules
            Statistical Deviation in Energy: {self._std_dev(energies):.6f}
            """
            
            # Ingestar en LightRAG
            await self.rag.ainsert(doc_text)
            stats['entities'] += 1
        
        return stats
    
    async def _ingest_relationships(self, by_instr: Dict):
        """Crear relaciones entre instrucciones correlacionadas"""
        
        instructions = list(by_instr.keys())
        
        for i, instr1 in enumerate(instructions):
            for instr2 in instructions[i+1:]:
                # Calcular correlación
                corr = self._calculate_correlation(by_instr[instr1], by_instr[instr2])
                
                if corr > 0.7:  # Umbral de correlación significativa
                    rel_text = f"""
                    {instr1} instruction is highly correlated with {instr2} instruction.
                    Correlation Coefficient: {corr:.3f}
                    This suggests both instructions share similar energy consumption patterns.
                    Potential security implication: Side-channel analysis may correlate execution.
                    """
                    
                    await self.rag.ainsert(rel_text)
    
    def _calculate_correlation(self, samples1: List, samples2: List) -> float:
        """Calcular correlación entre dos series de mediciones"""
        import numpy as np
        
        try:
            energy1 = np.array([float(s.get('energy', 0)) for s in samples1[:100]])
            energy2 = np.array([float(s.get('energy', 0)) for s in samples2[:100]])
            
            if len(energy1) == 0 or len(energy2) == 0:
                return 0.0
            
            # Normalizar
            energy1 = (energy1 - energy1.mean()) / (energy1.std() + 1e-10)
            energy2 = (energy2 - energy2.mean()) / (energy2.std() + 1e-10)
            
            return float(np.corrcoef(energy1, energy2)[0, 1])
        except:
            return 0.0
    
    def _std_dev(self, values: List[float]) -> float:
        """Calcular desviación estándar"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

async def main():
    """Función principal"""
    
    # Inicializar LightRAG
    rag = LightRAG(
        working_dir="./rag_storage/renode_measurements",
        llm_model_name="gpt-4-mini"  # O tu modelo preferido
    )
    
    # Crear adaptador
    adapter = RenodeAdapter(rag)
    
    # Ingestar datos
    csv_file = Path("./renode_entity/reports/measurements.csv")
    
    if csv_file.exists():
        stats = await adapter.ingest_from_csv(csv_file)
        print(f"✅ Ingestion complete!")
        print(f"   Entities created: {stats['entities']}")
        print(f"   Total samples processed: {stats['total_samples']}")
    else:
        print(f"❌ File not found: {csv_file}")
        print(f"   Run Renode first: python3 renode_script.py")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

### Step 2: Configurar Docker Compose

**Archivo:** `/workspaces/Dasein/docker-compose-renode.yml`

```yaml
version: '3.8'

services:
  # Neo4j para grafo de conocimiento
  neo4j:
    image: neo4j:5.15-enterprise
    environment:
      NEO4J_AUTH: neo4j/your-secure-password
      NEO4J_PLUGINS: '["graph-data-science"]'
    ports:
      - "7687:7687"
      - "7474:7474"
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "your-secure-password", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Milvus para búsqueda vectorial
  milvus:
    image: milvusdb/milvus:v0.19.7
    environment:
      COMMON_STORAGETYPE: local
    ports:
      - "19530:19530"
      - "9091:9091"
    volumes:
      - milvus_data:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis para caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # LightRAG API
  lightrag-api:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      LIGHTRAG_NEO4J_URL: "neo4j://neo4j:your-secure-password@neo4j:7687"
      LIGHTRAG_MILVUS_URL: "http://milvus:19530"
      LIGHTRAG_REDIS_URL: "redis://redis:6379"
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      neo4j:
        condition: service_healthy
      milvus:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./rag_storage:/app/rag_storage
    command: lightrag-server --host 0.0.0.0 --port 8000

volumes:
  neo4j_data:
  milvus_data:
  redis_data:
```

**Lanzar servicios:**
```bash
docker-compose -f docker-compose-renode.yml up -d

# Verificar estado
docker-compose -f docker-compose-renode.yml ps

# Ver logs
docker-compose -f docker-compose-renode.yml logs -f lightrag-api
```

### Step 3: Pipeline de Ingesta

**Archivo:** `/workspaces/Dasein/scripts/run_pipeline.sh`

```bash
#!/bin/bash
set -e

echo "🚀 Iniciando pipeline Renode → LightRAG"

# Configuración
RENODE_DURATION=60  # segundos
OUTPUT_DIR="./renode_entity/reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Ejecutar simulación Renode
echo "📊 Paso 1: Ejecutando simulación Renode..."
cd renode_entity
python3 renode_script.py --duration $RENODE_DURATION --output $OUTPUT_DIR

# Esperar a que terminen las mediciones
LATEST_CSV=$(ls -t $OUTPUT_DIR/measurements_*.csv | head -1)
echo "✅ Mediciones generadas: $LATEST_CSV"

# 2. Ejecutar adaptador
echo "🔄 Paso 2: Convirtiendo datos para LightRAG..."
cd ..
python3 lightrag/adapters/renode_adapter.py --input "$LATEST_CSV"

# 3. Ejecutar análisis de seguridad
echo "🔐 Paso 3: Analizando patrones de seguridad..."
python3 lightrag/security_patterns/side_channel_extractor.py \
  --input "$OUTPUT_DIR/measurements.json" \
  --output "$OUTPUT_DIR/security_report_${TIMESTAMP}.json"

# 4. Generar reporte
echo "📋 Paso 4: Generando reporte final..."
curl -s http://localhost:8000/query \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarize the security vulnerabilities found in the measurements"
  }' | jq . > "$OUTPUT_DIR/summary_${TIMESTAMP}.json"

echo "✅ Pipeline completado!"
echo "📁 Reportes en: $OUTPUT_DIR"
```

**Ejecutar:**
```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

---

## ✅ TESTING & VALIDATION

### Unit Tests

**Archivo:** `/workspaces/Dasein/tests/test_renode_adapter.py`

```python
#!/usr/bin/env python3
"""Tests para RenodeAdapter"""

import pytest
from pathlib import Path
import tempfile
import csv
from lightrag.adapters.renode_adapter import RenodeAdapter

@pytest.fixture
def sample_csv():
    """Crear CSV de muestra para tests"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'temperature', 'energy', 'latency', 
            'instruction_id', 'dim_0', 'dim_1'
        ])
        writer.writeheader()
        
        # Escribir datos de ejemplo
        for i in range(100):
            writer.writerow({
                'timestamp': '0.001000',
                'temperature': '23.5',
                'energy': '0.000100',
                'latency': '0.005',
                'instruction_id': 'MUL' if i < 50 else 'ADD',
                'dim_0': str(i),
                'dim_1': str(i * 2)
            })
        
        return Path(f.name)

@pytest.mark.asyncio
async def test_ingest_from_csv(sample_csv):
    """Test ingesta de CSV"""
    from unittest.mock import MagicMock, AsyncMock
    
    # Mock LightRAG
    mock_rag = MagicMock()
    mock_rag.ainsert = AsyncMock()
    
    adapter = RenodeAdapter(mock_rag)
    stats = await adapter.ingest_from_csv(sample_csv)
    
    # Verificaciones
    assert stats['entities'] == 2  # MUL, ADD
    assert stats['total_samples'] == 100
    assert mock_rag.ainsert.call_count > 0

@pytest.mark.asyncio
async def test_correlation_calculation(sample_csv):
    """Test cálculo de correlación"""
    mock_rag = MagicMock()
    adapter = RenodeAdapter(mock_rag)
    
    samples1 = [{'energy': '0.0001'}, {'energy': '0.0002'}, {'energy': '0.0001'}]
    samples2 = [{'energy': '0.0001'}, {'energy': '0.0002'}, {'energy': '0.0001'}]
    
    corr = adapter._calculate_correlation(samples1, samples2)
    
    # Correlación perfecta
    assert corr > 0.95

def test_std_dev():
    """Test desviación estándar"""
    mock_rag = MagicMock()
    adapter = RenodeAdapter(mock_rag)
    
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    std = adapter._std_dev(values)
    
    # Verificar aproximadamente correcto
    assert 1.4 < std < 1.5

# Ejecutar tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Ejecutar tests:**
```bash
python -m pytest tests/test_renode_adapter.py -v
```

### Integration Tests

```python
@pytest.mark.integration
async def test_end_to_end_pipeline():
    """Test completo del pipeline"""
    
    # 1. Generar datos Renode
    # 2. Ingestar en LightRAG
    # 3. Ejecutar queries
    # 4. Validar resultados
    
    pass
```

---

## 🔍 TROUBLESHOOTING

### Problema: "Permission denied" al cargar kernel module

```bash
# Solución
sudo insmod renode_entity/src/monje_virtual.ko

# Verificar
lsmod | grep monje_virtual

# Si falla, verificar dependencias
make -C renode_entity/src
```

### Problema: Neo4j no inicia

```bash
# Ver logs
docker logs dasein-neo4j-1

# Verificar puerto
netstat -tlnp | grep 7687

# Reiniciar
docker-compose restart neo4j
```

### Problema: Milvus connection timeout

```bash
# Ver estado
docker exec dasein-milvus-1 curl http://localhost:9091/healthz

# Reiniciar si necesario
docker-compose restart milvus
```

### Problema: CSV no generado por Renode

```bash
# Verificar script
python3 renode_entity/renode_script.py --help

# Ejecutar con verbose
python3 renode_entity/renode_script.py --duration 10 --verbose

# Verificar permisos de escritura
touch renode_entity/reports/test.txt
rm renode_entity/reports/test.txt
```

---

## ⚡ PERFORMANCE TUNING

### Optimizaciones LightRAG

```python
# 1. Tuning de chunk size
rag = LightRAG(
    working_dir="./rag_storage",
    chunk_size=512,  # Reducir si hay OOM
    overlap=128,      # 25% overlap
    max_token_size=4000,
    cache_size=1000,  # Aumentar si hay RAM
)

# 2. Parámetros de búsqueda
result = await rag.aquery(
    query="...",
    top_k=10,        # Resultados a retornar
    threshold=0.7,   # Umbral de relevancia
    timeout=30       # segundos
)
```

### Optimizaciones de Base de Datos

```bash
# Neo4j: Crear índices
cypher> CREATE INDEX FOR (n:Instruction) ON (n.id);
cypher> CREATE INDEX FOR (n:EnergyPattern) ON (n.cpa_value);

# Milvus: Particionamiento
# Crear particiones por timestamp
```

### Monitoreo

```bash
# Prometheus metrics
docker-compose exec lightrag-api curl http://localhost:8000/metrics

# Grafana dashboard
# http://localhost:3000

# Redis monitoring
docker-compose exec redis redis-cli INFO stats
```

---

## 📚 REFERENCIAS Y RECURSOS

### Documentación Oficial
- [LightRAG GitHub](https://github.com/GAIR-NLP/LightRAG)
- [Renode Documentation](https://renode.readthedocs.io/)
- [Neo4j Graph Database](https://neo4j.com/docs/)
- [Milvus Vector DB](https://milvus.io/docs/)

### Ejemplos Adicionales
- `examples/lightrag_openai_demo.py`
- `examples/graph_visual_with_neo4j.py`
- `renode_entity/scripts/test_entity.sh`

---

## 📞 SOPORTE

**¿Preguntas o problemas?**
1. Consultar logs: `docker-compose logs -f`
2. Revisar troubleshooting
3. Abrir issue en GitHub
4. Contactar equipo técnico

---

**Última actualización:** 2024
**Estado:** ✅ READY FOR DEPLOYMENT
