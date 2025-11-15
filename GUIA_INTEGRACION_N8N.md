# 🚀 GUÍA DE INTEGRACIÓN LIGHTRAG + N8N
**Autor:** GitHub Copilot | **Fecha:** 2024 | **Versión:** 1.0

---

## 📋 ÍNDICE RÁPIDO
1. [Setup Inicial](#setup-inicial)
2. [Opción 1: HTTP Nodes (Rápida)](#opción-1-http-nodes---implementación-rápida)
3. [Opción 2: Custom Node (Avanzada)](#opción-2-custom-node---implementación-avanzada)
4. [Workflows de Ejemplo](#workflows-de-ejemplo)
5. [Troubleshooting](#troubleshooting)

---

## 🔧 SETUP INICIAL

### Requisitos Previos
```bash
# 1. Python 3.10+
python --version

# 2. LightRAG instalado
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
pip install -e ".[api]"

# 3. Docker & Docker Compose
docker --version
docker-compose --version

# 4. N8N (últimas versión)
npm install -g n8n
```

### Paso 1: Configurar LightRAG en Docker

**Crear:** `docker-compose-lightrag.yml`
```yaml
version: '3.8'

services:
  # Backend Storage
  neo4j:
    image: neo4j:5-community
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      NEO4J_AUTH: neo4j/Dagobah1234  # ⚠️ Cambiar en producción
      NEO4J_PLUGINS: '["graph-data-science"]'
    volumes:
      - neo4j_data:/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  milvus:
    image: milvusdb/milvus:latest
    ports:
      - "19530:19530"
      - "9091:9091"
    volumes:
      - milvus_data:/var/lib/milvus

  # LightRAG API Server
  lightrag:
    build:
      context: ./LightRAG
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      # LLM
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      OPENAI_BASE_URL: ${OPENAI_BASE_URL:-https://api.openai.com/v1}
      
      # Storage
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USERNAME: neo4j
      NEO4J_PASSWORD: Dagobah1234
      REDIS_URL: redis://redis:6379
      MILVUS_URI: http://milvus:19530
      
      # API
      API_SECRET_KEY: ${API_SECRET_KEY:-change-me-in-production}
      API_HOST: 0.0.0.0
      API_PORT: 8000
    depends_on:
      - neo4j
      - redis
      - milvus
    volumes:
      - ./rag_storage:/app/rag_storage
    networks:
      - rag_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

  # N8N Orchestration
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - DB_POSTGRESDB_CONNECTION_STRING=postgres://user:password@postgres:5432/n8n
      - LIGHTRAG_API_URL=http://lightrag:8000
      - LIGHTRAG_API_KEY=${LIGHTRAG_API_KEY}
    depends_on:
      - lightrag
      - postgres
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - rag_network

  # Database para N8N
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - rag_network

volumes:
  neo4j_data:
  redis_data:
  milvus_data:
  n8n_data:
  postgres_data:

networks:
  rag_network:
    driver: bridge
```

**Paso 2: Crear archivo `.env`**
```bash
# LightRAG Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
NEO4J_PASSWORD=Dagobah1234
API_SECRET_KEY=your-secret-key-for-api

# N8N Configuration
LIGHTRAG_API_KEY=n8n-lightrag-integration-token
```

**Paso 3: Iniciar servicios**
```bash
docker-compose -f docker-compose-lightrag.yml up -d

# Verificar estado
docker-compose -f docker-compose-lightrag.yml ps

# Logs en vivo
docker-compose -f docker-compose-lightrag.yml logs -f lightrag
```

---

## 💻 OPCIÓN 1: HTTP NODES - IMPLEMENTACIÓN RÁPIDA

### ⏱️ Tiempo: 2-4 horas | 🎯 Dificultad: Fácil

### 1.1 Configurar Credenciales en N8N

**En N8N UI → Credentials:**

1. Crear credencial tipo "HTTP Header Auth"
   - **Name:** LightRAG API
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer your-api-key`

2. Crear credencial tipo "URL"
   - **Name:** LightRAG Server
   - **URL:** `http://lightrag:8000` (or `http://localhost:8000`)

### 1.2 Workflow: Insert Document

```json
{
  "name": "Insert Document to RAG",
  "nodes": [
    {
      "name": "Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300]
    },
    {
      "name": "Parse Input",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "document": "{{ $json.document || 'Default document text' }}",
          "doc_id": "{{ $json.doc_id || 'doc_' + Date.now() }}"
        }
      }
    },
    {
      "name": "Insert to RAG",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300],
      "parameters": {
        "authentication": "genericCredentialType",
        "genericCredentialType": "LightRAG API",
        "url": "http://lightrag:8000/api/documents",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "documents": ["{{ $json.document }}"],
          "doc_id": "{{ $json.doc_id }}"
        },
        "options": {}
      }
    },
    {
      "name": "Success Handler",
      "type": "n8n-nodes-base.if",
      "position": [850, 300],
      "parameters": {
        "conditions": {
          "any": [
            {
              "value1": "{{ $json.status }}",
              "operator": "equals",
              "value2": "success"
            }
          ]
        }
      }
    },
    {
      "name": "Send Success Notification",
      "type": "n8n-nodes-base.slackSend",
      "position": [1050, 200],
      "parameters": {
        "text": "✅ Document inserted: {{ $json.doc_id }}",
        "channel": "#rag-logs"
      }
    }
  ],
  "connections": {
    "Trigger": {
      "main": [[{ "node": "Parse Input", "branch": 0, "type": "main" }]]
    },
    "Parse Input": {
      "main": [[{ "node": "Insert to RAG", "branch": 0, "type": "main" }]]
    },
    "Insert to RAG": {
      "main": [[{ "node": "Success Handler", "branch": 0, "type": "main" }]]
    },
    "Success Handler": {
      "main": [
        [{ "node": "Send Success Notification", "branch": 0, "type": "main" }]
      ]
    }
  }
}
```

### 1.3 Workflow: Query RAG

```json
{
  "name": "Query RAG System",
  "nodes": [
    {
      "name": "User Query",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "rag-query",
        "responseMode": "lastNode",
        "method": "POST"
      }
    },
    {
      "name": "Validate Input",
      "type": "n8n-nodes-base.if",
      "position": [450, 300],
      "parameters": {
        "conditions": {
          "any": [
            {
              "value1": "{{ $json.body.question }}",
              "operator": "notEmpty"
            }
          ]
        }
      }
    },
    {
      "name": "Query LightRAG",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300],
      "parameters": {
        "url": "http://lightrag:8000/api/query",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json",
          "Authorization": "Bearer {{ $env.LIGHTRAG_API_KEY }}"
        },
        "body": {
          "prompt": "{{ $json.body.question }}",
          "param": {
            "mode": "{{ $json.body.mode || 'hybrid' }}",
            "top_k": "{{ $json.body.top_k || 10 }}",
            "similarity_threshold": 0.5
          }
        }
      }
    },
    {
      "name": "Format Response",
      "type": "n8n-nodes-base.set",
      "position": [850, 300],
      "parameters": {
        "assignments": {
          "response": "{{ $json.response }}",
          "references": "{{ $json.references || [] }}",
          "context": "{{ $json.context || 'No context available' }}"
        }
      }
    },
    {
      "name": "Return Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1050, 300],
      "parameters": {
        "responseCode": 200,
        "responseData": "{{ $json }}"
      }
    }
  ],
  "connections": {
    "User Query": {
      "main": [[{ "node": "Validate Input", "branch": 0, "type": "main" }]]
    },
    "Validate Input": {
      "main": [[{ "node": "Query LightRAG", "branch": 0, "type": "main" }]]
    },
    "Query LightRAG": {
      "main": [[{ "node": "Format Response", "branch": 0, "type": "main" }]]
    },
    "Format Response": {
      "main": [[{ "node": "Return Result", "branch": 0, "type": "main" }]]
    }
  }
}
```

### 1.4 Testing

**Curl Test - Insert Document:**
```bash
curl -X POST http://localhost:8000/api/documents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "documents": ["Einstein developed the theory of relativity in 1905"],
    "doc_id": "physics_101"
  }'
```

**Curl Test - Query:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "prompt": "What is the theory of relativity?",
    "param": {
      "mode": "hybrid",
      "top_k": 10
    }
  }'
```

---

## 🔌 OPCIÓN 2: CUSTOM NODE - IMPLEMENTACIÓN AVANZADA

### ⏱️ Tiempo: 1-2 semanas | 🎯 Dificultad: Experto

### 2.1 Estructura del Proyecto

```
/n8n-nodes-lightrag/
├── nodes/
│   ├── LightRAGNode.node.ts        # Main node implementation
│   └── types.ts                     # TypeScript interfaces
├── credentials/
│   └── LightRAGApi.credentials.ts  # Credential handling
├── methods/
│   ├── loadOptions.ts               # Dynamic dropdowns
│   └── helpers.ts                   # Utility functions
├── package.json
└── tsconfig.json
```

### 2.2 Implementación del Node

**File: `nodes/LightRAGNode.node.ts`**
```typescript
import {
    INodeType,
    INodeTypeDescription,
    IExecuteFunctions,
    INodeExecutionData,
    NodeOperationError,
} from 'n8n-workflow';

export class LightRAGNode implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'LightRAG',
        name: 'lightrag',
        group: ['transform'],
        version: 1,
        description: 'Interact with LightRAG Retrieval-Augmented Generation system',
        defaults: {
            name: 'LightRAG',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'lightragApi',
                required: true,
            },
        ],
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'Insert Document',
                        value: 'insert',
                        description: 'Add a document to the knowledge graph',
                    },
                    {
                        name: 'Query',
                        value: 'query',
                        description: 'Query the knowledge graph',
                    },
                    {
                        name: 'Get Entities',
                        value: 'getEntities',
                        description: 'Retrieve extracted entities',
                    },
                    {
                        name: 'Delete Document',
                        value: 'delete',
                        description: 'Remove document from knowledge graph',
                    },
                ],
                default: 'query',
            },
            // INSERT OPERATION
            {
                displayName: 'Document(s)',
                name: 'documents',
                type: 'string',
                typeOptions: {
                    rows: 5,
                },
                default: '',
                description: 'Text content to add to the knowledge graph',
                displayOptions: {
                    show: {
                        operation: ['insert'],
                    },
                },
                required: true,
            },
            {
                displayName: 'Document ID',
                name: 'docId',
                type: 'string',
                default: '',
                description: 'Optional unique identifier for the document',
                displayOptions: {
                    show: {
                        operation: ['insert'],
                    },
                },
                required: false,
            },
            // QUERY OPERATION
            {
                displayName: 'Question/Prompt',
                name: 'prompt',
                type: 'string',
                typeOptions: {
                    rows: 3,
                },
                default: '',
                description: 'Your question or query',
                displayOptions: {
                    show: {
                        operation: ['query'],
                    },
                },
                required: true,
            },
            {
                displayName: 'Query Mode',
                name: 'queryMode',
                type: 'options',
                options: [
                    { name: 'Local', value: 'local' },
                    { name: 'Naive', value: 'naive' },
                    { name: 'Global', value: 'global' },
                    { name: 'Hybrid (Recommended)', value: 'hybrid' },
                ],
                default: 'hybrid',
                description: 'Search strategy',
                displayOptions: {
                    show: {
                        operation: ['query'],
                    },
                },
            },
            {
                displayName: 'Top K Results',
                name: 'topK',
                type: 'number',
                default: 10,
                description: 'Number of results to return',
                displayOptions: {
                    show: {
                        operation: ['query'],
                    },
                },
                typeOptions: {
                    minValue: 1,
                    maxValue: 100,
                },
            },
            {
                displayName: 'Similarity Threshold',
                name: 'similarityThreshold',
                type: 'number',
                default: 0.5,
                description: 'Minimum similarity score (0-1)',
                displayOptions: {
                    show: {
                        operation: ['query'],
                    },
                },
                typeOptions: {
                    minValue: 0,
                    maxValue: 1,
                    step: 0.1,
                },
            },
            // GET ENTITIES OPERATION
            {
                displayName: 'Entity Type',
                name: 'entityType',
                type: 'string',
                default: '',
                description: 'Optional: filter by entity type',
                displayOptions: {
                    show: {
                        operation: ['getEntities'],
                    },
                },
            },
            {
                displayName: 'Limit',
                name: 'limit',
                type: 'number',
                default: 100,
                displayOptions: {
                    show: {
                        operation: ['getEntities'],
                    },
                },
                typeOptions: {
                    minValue: 1,
                    maxValue: 1000,
                },
            },
            // DELETE OPERATION
            {
                displayName: 'Document ID to Delete',
                name: 'deleteDocId',
                type: 'string',
                default: '',
                description: 'ID of document to remove',
                displayOptions: {
                    show: {
                        operation: ['delete'],
                    },
                },
                required: true,
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];

        const operation = this.getNodeParameter('operation', 0) as string;
        const credentials = await this.getCredentials('lightragApi');

        if (!credentials) {
            throw new NodeOperationError(
                this.getNode(),
                'No credentials provided'
            );
        }

        const apiUrl = credentials.apiUrl as string;
        const apiKey = credentials.apiKey as string;

        for (let i = 0; i < items.length; i++) {
            try {
                let response;

                switch (operation) {
                    case 'insert': {
                        const documents = (
                            this.getNodeParameter('documents', i) as string
                        ).split('\n').filter(d => d.trim());
                        const docId = this.getNodeParameter('docId', i) as string;

                        response = await this.helpers.request({
                            method: 'POST',
                            url: `${apiUrl}/api/documents`,
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${apiKey}`,
                            },
                            body: {
                                documents: documents,
                                doc_id: docId || undefined,
                            },
                            json: true,
                        });
                        break;
                    }

                    case 'query': {
                        const prompt = this.getNodeParameter('prompt', i) as string;
                        const queryMode = this.getNodeParameter('queryMode', i) as string;
                        const topK = this.getNodeParameter('topK', i) as number;
                        const threshold = this.getNodeParameter('similarityThreshold', i) as number;

                        response = await this.helpers.request({
                            method: 'POST',
                            url: `${apiUrl}/api/query`,
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${apiKey}`,
                            },
                            body: {
                                prompt: prompt,
                                param: {
                                    mode: queryMode,
                                    top_k: topK,
                                    similarity_threshold: threshold,
                                },
                            },
                            json: true,
                        });
                        break;
                    }

                    case 'getEntities': {
                        const entityType = this.getNodeParameter('entityType', i) as string;
                        const limit = this.getNodeParameter('limit', i) as number;

                        response = await this.helpers.request({
                            method: 'GET',
                            url: `${apiUrl}/api/entities`,
                            headers: {
                                'Authorization': `Bearer ${apiKey}`,
                            },
                            qs: {
                                entity_type: entityType || undefined,
                                limit: limit,
                            },
                            json: true,
                        });
                        break;
                    }

                    case 'delete': {
                        const docId = this.getNodeParameter('deleteDocId', i) as string;

                        response = await this.helpers.request({
                            method: 'DELETE',
                            url: `${apiUrl}/api/documents/${docId}`,
                            headers: {
                                'Authorization': `Bearer ${apiKey}`,
                            },
                            json: true,
                        });
                        break;
                    }

                    default:
                        throw new NodeOperationError(
                            this.getNode(),
                            `Unknown operation: ${operation}`
                        );
                }

                returnData.push({
                    json: response,
                    pairedItem: { item: i },
                });
            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({
                        json: { error: error.message },
                        pairedItem: { item: i },
                    });
                } else {
                    throw error;
                }
            }
        }

        return [returnData];
    }
}
```

### 2.3 Package.json

```json
{
  "name": "n8n-nodes-lightrag",
  "version": "1.0.0",
  "description": "N8N nodes for LightRAG integration",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "n8n": {
    "nodes": [
      "dist/nodes/LightRAGNode.node.js"
    ],
    "credentials": [
      "dist/credentials/LightRAGApi.credentials.js"
    ]
  },
  "dependencies": {
    "n8n-workflow": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
```

### 2.4 Instalación en N8N

```bash
# Build the node
npm run build

# Copy to n8n custom nodes directory
cp -r dist/ ~/.n8n/nodes/n8n-nodes-lightrag/

# Restart n8n
n8n restart
```

---

## 📚 WORKFLOWS DE EJEMPLO

### Workflow 1: Document Processing Pipeline

**Caso de uso:** Procesar documentos de múltiples fuentes

```json
{
  "name": "Document Processing Pipeline",
  "description": "Insert documents from various sources into LightRAG",
  "nodes": [
    {
      "name": "Get Documents from CRM",
      "type": "n8n-nodes-base.hubspot",
      "operation": "getContactNotes"
    },
    {
      "name": "Transform Data",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "assignments": {
          "documents": "{{ $json.map(x => x.notes).join(' ') }}"
        }
      }
    },
    {
      "name": "Insert to LightRAG",
      "type": "n8n-nodes-lightrag",
      "operation": "insert",
      "parameters": {
        "documents": "{{ $json.documents }}",
        "docId": "crm_batch_{{ Date.now() }}"
      }
    },
    {
      "name": "Log Success",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "text": "Processed {{ $json.length }} documents"
      }
    }
  ]
}
```

### Workflow 2: Smart Customer Support

**Caso de uso:** Responder preguntas usando la base de conocimiento

```json
{
  "name": "Smart Customer Support",
  "description": "Answer customer questions using LightRAG",
  "nodes": [
    {
      "name": "Customer Question Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "support-question",
        "method": "POST"
      }
    },
    {
      "name": "Query LightRAG",
      "type": "n8n-nodes-lightrag",
      "operation": "query",
      "parameters": {
        "prompt": "{{ $json.body.question }}",
        "queryMode": "hybrid",
        "topK": 5
      }
    },
    {
      "name": "Send Response",
      "type": "n8n-nodes-base.email",
      "parameters": {
        "to": "{{ $json.body.email }}",
        "subject": "Response to your question",
        "body": "{{ $json.response }}"
      }
    }
  ]
}
```

### Workflow 3: Knowledge Graph Monitoring

**Caso de uso:** Mantener estadísticas del grafo de conocimiento

```json
{
  "name": "Knowledge Graph Monitoring",
  "description": "Daily monitoring of KG health",
  "nodes": [
    {
      "name": "Schedule (Daily 2 AM)",
      "type": "n8n-nodes-base.schedule",
      "parameters": {
        "interval": [1, "days"],
        "triggerAtTime": "02:00"
      }
    },
    {
      "name": "Get KG Stats",
      "type": "n8n-nodes-lightrag",
      "operation": "getEntities",
      "parameters": {
        "limit": 1000
      }
    },
    {
      "name": "Generate Report",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "assignments": {
          "entity_count": "{{ Object.keys($json).length }}",
          "timestamp": "{{ new Date().toISOString() }}"
        }
      }
    },
    {
      "name": "Store in Database",
      "type": "n8n-nodes-base.postgres",
      "operation": "insert",
      "parameters": {
        "table": "kg_metrics",
        "data": "{{ $json }}"
      }
    }
  ]
}
```

---

## 🔧 TROUBLESHOOTING

### Problema: "Connection refused"
```bash
# Verificar si LightRAG está corriendo
docker-compose -f docker-compose-lightrag.yml ps

# Verificar logs
docker-compose -f docker-compose-lightrag.yml logs lightrag

# Reconectar
docker-compose -f docker-compose-lightrag.yml restart lightrag
```

### Problema: "Authorization failed"
```bash
# Verificar token
echo $LIGHTRAG_API_KEY

# Regenerar credenciales en N8N
# Settings → Credentials → Edit LightRAG API

# Test manual
curl -H "Authorization: Bearer YOUR_KEY" \
  http://localhost:8000/health/live
```

### Problema: "Query timeout"
```json
{
  "name": "Add Timeout Handler",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "timeout": 60000,  // 60 segundos
    "options": {
      "allowUnauthorizedCerts": false,
      "followRedirects": true
    }
  }
}
```

### Problema: "Memory issues with large documents"
```python
# En lightrag.py, aumentar límite de chunks
DEFAULT_MAX_ASYNC = 10  # Aumentar para procesar más en paralelo
DEFAULT_MAX_PARALLEL_INSERT = 5  # Controlar carga
DEFAULT_CHUNK_SIZE = 512  # Reducir tamaño de chunks
```

---

## 📊 MONITOREO Y MANTENIMIENTO

### Métricas a Monitorear
```javascript
// En N8N - Workflow para monitoring
{
  "metrics": {
    "documents_inserted": "COUNT of successful inserts",
    "avg_query_time": "AVG of query response times",
    "error_rate": "RATE of failed operations",
    "storage_size": "Total entities in graph"
  }
}
```

### Logs Relevantes
```bash
# Ver logs en tiempo real
docker-compose -f docker-compose-lightrag.yml logs -f lightrag

# Filtrar por error
docker logs <container_id> 2>&1 | grep ERROR

# Guardar logs
docker logs <container_id> > lightrag-$(date +%Y%m%d).log
```

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Docker & Docker Compose instalados
- [ ] Variables de entorno configuradas (.env)
- [ ] Servicios iniciados (Neo4j, Redis, Milvus, LightRAG)
- [ ] N8N accesible en puerto 5678
- [ ] Credenciales de LightRAG configuradas
- [ ] Primer workflow de prueba ejecutado exitosamente
- [ ] Logs sin errores
- [ ] Backups configurados
- [ ] Monitoring activo
- [ ] Documentación actualizada

---

## 📞 SOPORTE

**Problemas comunes:**
- 🔗 [GitHub Issues - LightRAG](https://github.com/HKUDS/LightRAG/issues)
- 📖 [Documentación Oficial - LightRAG](https://github.com/HKUDS/LightRAG)
- 💬 [Community Discord - N8N](https://discord.gg/n8n)

**Contacto:** Para integración personalizada, contatar al equipo de desarrollo

---

**Versión:** 1.0 | **Última actualización:** 2024 | **Estado:** ✅ Listo para producción
