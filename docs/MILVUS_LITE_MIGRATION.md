# Milvus Lite Migration Plan

**Version**: 0.4.0  
**Date**: 2025-10-31  
**Status**: Planning  
**Branch**: `milvus-lite-migration`

## Overview

This document outlines the migration plan from Milvus Standalone to Milvus Lite for the GOST RAG system. The migration is necessary because Milvus Standalone requires Docker-in-Docker, which is not available on RunPod GPU instances.

## Background

### Current State (v0.3.1)
- **Vector Database**: Milvus Standalone (requires Docker)
- **Deployment Target**: RunPod GPU instance
- **Problem**: Docker-in-Docker not supported on RunPod
- **Status**: Infrastructure ready, code needs adaptation

### Target State (v0.4.0)
- **Vector Database**: Milvus Lite (embedded SQLite-based)
- **Deployment**: Works directly on RunPod without Docker
- **Benefits**: Simpler deployment, no Docker dependency

## Technical Changes Required

### 1. Update Dependencies

**File**: `requirements.txt`

```diff
- pymilvus==2.6.2
+ pymilvus==2.6.2
+ milvus-lite==2.3.5  # Already installed
```

### 2. Update Vector Store Implementation

**File**: `src/vector_store/milvus_store.py`

#### Current Implementation (Milvus Standalone)
```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)
```

#### Target Implementation (Milvus Lite)
```python
from milvus import MilvusClient

client = MilvusClient(uri="./milvus_lite.db")
```

### 3. Update Collection Operations

#### Create Collection
**Before**:
```python
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
]
schema = CollectionSchema(fields=fields)
collection = Collection(name="gost_documents", schema=schema)
```

**After**:
```python
client.create_collection(
    collection_name="gost_documents",
    dimension=1024,
    metric_type="COSINE"
)
```

#### Insert Data
**Before**:
```python
collection.insert([ids, embeddings, texts])
```

**After**:
```python
client.insert(
    collection_name="gost_documents",
    data=[
        {"id": id, "vector": embedding, "text": text}
        for id, embedding, text in zip(ids, embeddings, texts)
    ]
)
```

#### Search
**Before**:
```python
results = collection.search(
    data=[query_embedding],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=top_k
)
```

**After**:
```python
results = client.search(
    collection_name="gost_documents",
    data=[query_embedding],
    limit=top_k,
    search_params={"metric_type": "COSINE"}
)
```

### 4. Update Configuration

**File**: `config.yaml`

```yaml
vector_store:
  type: "milvus_lite"  # Changed from "milvus"
  uri: "./milvus_lite.db"  # Changed from host/port
  collection_name: "gost_documents"
  dimension: 1024
  metric_type: "COSINE"
```

## Migration Steps

### Phase 1: Code Adaptation (30-60 minutes)

1. **Update `src/vector_store/milvus_store.py`**
   - Replace `connections.connect()` with `MilvusClient()`
   - Update all collection operations to use MilvusClient API
   - Maintain backward compatibility with existing data structures

2. **Update `config.yaml`**
   - Change vector_store.type to "milvus_lite"
   - Replace host/port with uri parameter

3. **Update `src/config.py`**
   - Add support for Milvus Lite configuration
   - Validate uri parameter instead of host/port

### Phase 2: Testing (15-30 minutes)

1. **Local Testing**
   ```bash
   # Test configuration validation
   python -m src.main --help
   
   # Test document indexing
   python -m src.main index --input data/raw --create-new
   
   # Test extraction
   python -m src.main extract --class-name C235
   
   # Test query
   python -m src.main query --question "Какие характеристики у класса C235?"
   ```

2. **Verify Results**
   - Check that milvus_lite.db is created
   - Verify document count matches input
   - Confirm extraction returns correct data
   - Validate query responses

### Phase 3: RunPod Deployment (15-30 minutes)

1. **Upload Code to RunPod**
   ```bash
   scp -P 40039 -r . root@213.192.2.89:/workspace/gost_rag/
   ```

2. **Run Indexing**
   ```bash
   ssh -p 40039 root@213.192.2.89
   cd /workspace/gost_rag
   source venv/bin/activate
   python -m src.main index --input data/raw --create-new
   ```

3. **Test Extraction**
   ```bash
   python -m src.main extract --class-name C235
   ```

### Phase 4: Web Interface Integration (30-60 minutes)

1. **Update Web Project**
   - Copy updated RAG code to web project
   - Test FastAPI integration
   - Verify frontend displays results correctly

2. **Production Testing**
   - Test all API endpoints
   - Verify error handling
   - Check performance metrics

## API Compatibility Matrix

| Operation | Milvus Standalone | Milvus Lite | Status |
|-----------|------------------|-------------|--------|
| Create Collection | ✅ | ✅ | Compatible |
| Insert Data | ✅ | ✅ | Compatible |
| Search | ✅ | ✅ | Compatible |
| Delete | ✅ | ✅ | Compatible |
| Drop Collection | ✅ | ✅ | Compatible |
| Get Stats | ✅ | ✅ | Compatible |
| Index Creation | ✅ | ⚠️ Limited | Simplified |

## Performance Considerations

### Milvus Standalone
- **Pros**: Full feature set, optimized for large-scale
- **Cons**: Requires Docker, complex setup
- **Best for**: Production with >1M vectors

### Milvus Lite
- **Pros**: Simple setup, no Docker, embedded
- **Cons**: Limited indexing options, single-node only
- **Best for**: Development, small-scale (<100K vectors)

### Current Dataset
- **Documents**: 1 GOST PDF (~50 pages)
- **Expected Vectors**: ~1,000-2,000
- **Recommendation**: Milvus Lite is sufficient

## Rollback Plan

If migration fails, rollback to v0.3.1:

```bash
git checkout RAG-Milvus-Manus-Edition
```

Original Milvus Standalone code is preserved in the main branch.

## Success Criteria

- ✅ Code runs without Docker dependency
- ✅ All 19 tests pass
- ✅ Document indexing completes successfully
- ✅ Extraction returns correct data for C235
- ✅ Query returns relevant results
- ✅ Deployment works on RunPod
- ✅ Web interface integration functional

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Code Adaptation | 30-60 min | Pending |
| Local Testing | 15-30 min | Pending |
| RunPod Deployment | 15-30 min | Pending |
| Web Integration | 30-60 min | Pending |
| **Total** | **1.5-3 hours** | **Pending** |

## References

- [Milvus Lite Documentation](https://milvus.io/docs/milvus_lite.md)
- [Milvus Lite vs Standalone Comparison](/home/ubuntu/milvus_comparison.md)
- [PyMilvus API Reference](https://milvus.io/api-reference/pymilvus/v2.4.x/About.md)

## Next Steps

1. Review this migration plan
2. Begin Phase 1: Code Adaptation
3. Test locally before RunPod deployment
4. Update documentation after successful migration
