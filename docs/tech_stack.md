# Технический стек GOST RAG System

## Обзор архитектуры

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  Web Interface (React 19 + TypeScript + Tailwind CSS)          │
│  - shadcn/ui components                                         │
│  - Wouter routing                                               │
│  - tRPC client                                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Backend API (Node.js + tRPC + Express)                         │
│  - Type-safe API endpoints                                      │
│  - Authentication (OAuth 2.0)                                   │
│  - Database ORM (Drizzle)                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PROCESSING LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  RAG Engine (Python 3.11)                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LlamaIndex 0.14.6                                       │  │
│  │  - Document loaders (PDF, TXT, MD)                       │  │
│  │  - Text splitters (Sentence, Token)                      │  │
│  │  - Query engines (Vector, Hybrid)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LLM Integration                                         │  │
│  │  - OpenRouter API (Claude 3.5 Sonnet)                    │  │
│  │  - Temperature: 0.1 (precision)                          │  │
│  │  - Max tokens: 4096                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Embeddings                                              │  │
│  │  - Model: intfloat/multilingual-e5-large                 │  │
│  │  - Dimensions: 1024                                      │  │
│  │  - Device: CUDA (GPU accelerated)                        │  │
│  │  - Framework: sentence-transformers 5.1.2                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        STORAGE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Vector Database  │  │ Relational DB    │  │ File Storage │  │
│  │ Milvus 2.6.2     │  │ PostgreSQL       │  │ Local FS     │  │
│  │ (Lite/Standalone)│  │ (via Drizzle)    │  │              │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Детальный технический стек

### 1. Frontend (Web Interface)

#### Core Framework
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **React** | 19.0.0 | UI framework |
| **TypeScript** | 5.7.3 | Type safety |
| **Vite** | 6.0.11 | Build tool & dev server |
| **Wouter** | 3.5.3 | Client-side routing |

#### UI Components & Styling
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **Tailwind CSS** | 4.0.0 | Utility-first CSS |
| **shadcn/ui** | Latest | Pre-built components |
| **Radix UI** | Various | Headless UI primitives |
| **Lucide React** | Latest | Icon library |
| **Streamdown** | Latest | Markdown rendering |

#### State Management & API
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **tRPC Client** | 11.0.0 | Type-safe API calls |
| **React Query** | 5.0.0 | Data fetching & caching |

---

### 2. Backend (API Server)

#### Runtime & Framework
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **Node.js** | 22.13.0 | JavaScript runtime |
| **Express** | 5.0.1 | HTTP server |
| **tRPC** | 11.0.0 | Type-safe API framework |

#### Database & ORM
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **PostgreSQL** | 17.0 | Relational database |
| **Drizzle ORM** | 0.39.0 | Type-safe ORM |
| **Drizzle Kit** | 0.31.0 | Schema migrations |

#### Authentication
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **OAuth 2.0** | - | Authentication protocol |
| **JWT** | - | Token-based auth |

---

### 3. RAG Engine (Python)

#### Core Python
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **Python** | 3.11.14 | Runtime |
| **pip** | 25.2 | Package manager |

#### RAG Framework
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **LlamaIndex Core** | 0.14.6 | RAG orchestration |
| **LlamaIndex Readers** | 0.4.2 | Document loaders |
| **LlamaIndex Vector Stores** | 0.4.5 | Vector DB integration |
| **LlamaIndex Embeddings** | 0.4.3 | Embedding models |
| **LlamaIndex LLMs** | 0.4.5 | LLM integration |

#### Document Processing
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **PyPDF2** | 3.0.1 | PDF parsing |
| **python-docx** | 1.1.2 | Word documents |
| **beautifulsoup4** | 4.12.3 | HTML parsing |
| **lxml** | 5.3.0 | XML/HTML processing |

#### Machine Learning
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **PyTorch** | 2.9.0 | Deep learning framework |
| **CUDA** | 12.8 | GPU acceleration |
| **Transformers** | 4.57.1 | Hugging Face models |
| **Sentence-Transformers** | 5.1.2 | Embedding models |
| **NumPy** | 2.2.3 | Numerical computing |

#### LLM Integration
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **OpenAI SDK** | 1.59.9 | OpenAI API client |
| **OpenRouter** | - | Multi-LLM gateway |
| **Claude 3.5 Sonnet** | - | Primary LLM |

#### Vector Database
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **PyMilvus** | 2.6.2 | Milvus client |
| **Milvus Lite** | 2.3.5 | Embedded vector DB |

#### Utilities
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **python-dotenv** | 1.0.1 | Environment variables |
| **PyYAML** | 6.0.2 | YAML parsing |
| **tqdm** | 4.67.1 | Progress bars |
| **colorama** | 0.4.6 | Colored terminal output |

---

### 4. Infrastructure

#### Deployment
| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **RunPod** | - | GPU cloud platform |
| **Ubuntu** | 24.04 | Operating system |
| **Docker** | 28.5.1 | Containerization (optional) |
| **Docker Compose** | 2.40.3 | Multi-container orchestration |

#### Hardware (RunPod Pod)
| Компонент | Спецификация |
|-----------|--------------|
| **GPU** | NVIDIA RTX 3090 (24 GB VRAM) |
| **CPU** | 32 vCPU @ 3.0+ GHz |
| **RAM** | 125 GB |
| **Storage** | 100 GB Container + 500 GB Volume |
| **Network** | 1 Gbps |

---

## Конфигурация по слоям

### Frontend Configuration

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
});

// tailwind.config.ts
export default {
  content: ['./client/src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        // ... shadcn/ui colors
      }
    }
  }
};
```

### Backend Configuration

```typescript
// server/index.ts
const app = express();
app.use('/api/trpc', trpcExpress.createExpressMiddleware({
  router: appRouter,
  createContext
}));

// drizzle.config.ts
export default {
  schema: './server/db/schema.ts',
  out: './server/db/migrations',
  dialect: 'postgresql'
};
```

### RAG Engine Configuration

```python
# config.yaml
llm:
  provider: openrouter
  model: anthropic/claude-3.5-sonnet
  temperature: 0.1
  max_tokens: 4096

embeddings:
  type: local
  model: intfloat/multilingual-e5-large
  device: cuda
  batch_size: 32

milvus:
  host: localhost
  port: 19530
  collection_name: gost_documents

chunking:
  chunk_size: 1000
  chunk_overlap: 200
```

---

## Модели и алгоритмы

### Embedding Model

**Model:** intfloat/multilingual-e5-large

| Параметр | Значение |
|----------|----------|
| Архитектура | BERT-based |
| Параметры | 560M |
| Размерность | 1024 |
| Языки | 100+ (включая русский) |
| Контекст | 512 tokens |
| Размер | 2.24 GB |
| Производительность | ~1000 docs/sec на RTX 3090 |

**Почему выбрана:**
- ✅ Отличное качество для русского языка
- ✅ Мультиязычность (ГОСТ может содержать английские термины)
- ✅ Оптимальный баланс качество/скорость
- ✅ GPU acceleration

### LLM Model

**Model:** Claude 3.5 Sonnet (via OpenRouter)

| Параметр | Значение |
|----------|----------|
| Параметры | ~175B (оценка) |
| Контекст | 200,000 tokens |
| Стоимость | $3.00 / 1M input tokens |
| Стоимость | $15.00 / 1M output tokens |
| Скорость | ~50 tokens/sec |

**Почему выбрана:**
- ✅ Лучшее понимание русского языка
- ✅ Отличная работа с техническими текстами
- ✅ Большой контекст (200K tokens)
- ✅ Высокая точность извлечения данных

### Vector Search Algorithm

**Index Type:** IVF_FLAT (Inverted File with Flat compression)

| Параметр | Значение |
|----------|----------|
| Метрика | L2 (Euclidean distance) |
| nlist | 128 |
| nprobe | 16 |
| Точность | ~95% recall@10 |
| Скорость | <100ms для 1M векторов |

**Chunking Strategy:**

```python
chunk_size = 1000  # characters
chunk_overlap = 200  # characters
# Причина: баланс между контекстом и точностью
```

---

## API Endpoints

### tRPC Procedures (Backend)

```typescript
// server/ragRouter.ts
export const ragRouter = router({
  // Semantic search
  query: publicProcedure
    .input(z.object({ query: z.string(), limit: z.number() }))
    .query(async ({ input }) => { /* ... */ }),
  
  // Extract strength class data
  extractStrengthClass: publicProcedure
    .input(z.object({ className: z.string() }))
    .query(async ({ input }) => { /* ... */ }),
  
  // Upload documents
  uploadDocument: publicProcedure
    .input(z.object({ file: z.instanceof(File) }))
    .mutation(async ({ input }) => { /* ... */ }),
  
  // Get system stats
  getStats: publicProcedure
    .query(async () => { /* ... */ })
});
```

### Python CLI (RAG Engine)

```bash
# Index documents
python -m src.main index --input data/raw --create-new

# Query
python -m src.main query --question "Что такое класс прочности C235?"

# Extract strength class
python -m src.main extract --class-name C235

# Stats
python -m src.main stats
```

---

## Data Flow

### 1. Document Indexing

```
PDF File → PyPDF2 → Text Extraction → 
→ LlamaIndex TextSplitter → Chunks (1000 chars) →
→ Sentence-Transformers → Embeddings (1024-dim) →
→ Milvus → Vector Storage
```

### 2. Query Processing

```
User Query → Frontend (React) → tRPC → Backend (Node.js) →
→ Python RAG Engine → Embedding Model → Query Vector →
→ Milvus Vector Search → Top-K Chunks →
→ Claude 3.5 Sonnet (via OpenRouter) → Answer →
→ Backend → Frontend → User
```

---

## Performance Metrics

### Indexing Performance

| Метрика | Значение |
|---------|----------|
| PDF parsing | ~10 pages/sec |
| Embedding generation | ~1000 chunks/sec (GPU) |
| Vector insertion | ~5000 vectors/sec |
| **Total** | ~50 pages/min |

### Query Performance

| Метрика | Значение |
|---------|----------|
| Embedding generation | <50ms |
| Vector search | <100ms |
| LLM inference | 1-3 sec |
| **Total latency** | 1.5-3.5 sec |

### Resource Usage

| Ресурс | Idle | Indexing | Querying |
|--------|------|----------|----------|
| GPU VRAM | 3 GB | 8 GB | 5 GB |
| RAM | 4 GB | 12 GB | 8 GB |
| CPU | 5% | 60% | 30% |

---

## Security

### Authentication & Authorization
- OAuth 2.0 для веб-интерфейса
- JWT tokens для API
- Role-based access control (RBAC)

### Data Security
- HTTPS для всех соединений
- Environment variables для секретов
- No logging of sensitive data

### API Security
- Rate limiting
- Input validation (Zod schemas)
- CORS configuration

---

## Monitoring & Logging

### Logging
```python
# Python logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics
- Query latency
- Embedding generation time
- Vector search time
- LLM response time
- Error rates

---

## Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **GitHub** | Code hosting |
| **pytest** | Python testing |
| **Vitest** | TypeScript testing |
| **ESLint** | Code linting |
| **Prettier** | Code formatting |
| **Black** | Python formatting |

---

## Deployment

### Current Setup (RunPod)
```bash
# Python environment
/workspace/gost_rag/venv/  # Python 3.11 virtualenv

# Application code
/workspace/gost_rag/src/   # RAG engine
/workspace/gost_rag/data/  # Documents & DB

# Web interface (separate project)
/home/ubuntu/gost_rag_web/  # React + Node.js
```

### Environment Variables
```bash
# LLM
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Embeddings
EMBEDDING_TYPE=local
LOCAL_EMBEDDING_MODEL=intfloat/multilingual-e5-large
LOCAL_EMBEDDING_DEVICE=cuda

# Vector DB
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

---

## Cost Breakdown

### Infrastructure (RunPod)
- GPU Pod (RTX 3090): $0.40/hour
- Storage (500 GB): $0.0089/hour
- **Total**: ~$0.41/hour (~$295/month)

### API Costs (OpenRouter)
- Claude 3.5 Sonnet: $3/$15 per 1M tokens
- Estimated usage: ~100K tokens/day
- **Total**: ~$50/month

### Total Monthly Cost: ~$345

---

## Future Enhancements

### Planned Features
- [ ] Streaming responses
- [ ] Multi-document comparison
- [ ] Advanced filtering
- [ ] Caching layer (Redis)
- [ ] Horizontal scaling
- [ ] Monitoring dashboard (Grafana)

### Potential Upgrades
- [ ] Fine-tuned embedding model
- [ ] Hybrid search (vector + keyword)
- [ ] Multi-modal support (images in PDFs)
- [ ] Distributed Milvus cluster
- [ ] CI/CD pipeline

---

## Summary

**Полный стек:**
- **Frontend:** React 19 + TypeScript + Tailwind + shadcn/ui
- **Backend:** Node.js + tRPC + Express + PostgreSQL
- **RAG Engine:** Python 3.11 + LlamaIndex + PyTorch
- **Embeddings:** intfloat/multilingual-e5-large (GPU)
- **LLM:** Claude 3.5 Sonnet (OpenRouter)
- **Vector DB:** Milvus 2.6.2 (Lite/Standalone)
- **Infrastructure:** RunPod (RTX 3090, 32 vCPU, 125 GB RAM)

**Ключевые особенности:**
- ✅ Type-safe (TypeScript + tRPC)
- ✅ GPU-accelerated embeddings
- ✅ Production-ready architecture
- ✅ Scalable design
- ✅ Modern UI/UX
