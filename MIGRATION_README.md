# Milvus Lite Migration Branch

**Branch**: `milvus-lite-migration`  
**Base Version**: v0.3.1  
**Target Version**: v0.4.0  
**Status**: Planning Complete, Ready for Implementation

## Purpose

This branch contains the migration from Milvus Standalone to Milvus Lite to enable deployment on RunPod GPU instances without Docker-in-Docker requirements.

## Current Status

### ✅ Completed
- Migration plan created (`docs/MILVUS_LITE_MIGRATION.md`)
- Technical requirements documented
- API compatibility analysis completed
- Timeline and success criteria defined

### 🚧 Pending
- Code adaptation in `src/vector_store/milvus_store.py`
- Configuration updates in `config.yaml`
- Local testing (19 test suite)
- RunPod deployment testing
- Web interface integration

## Quick Start

### Review Migration Plan
```bash
git checkout milvus-lite-migration
cat docs/MILVUS_LITE_MIGRATION.md
```

### Begin Implementation
Follow the phases outlined in the migration plan:

1. **Phase 1**: Code Adaptation (30-60 min)
2. **Phase 2**: Testing (15-30 min)
3. **Phase 3**: RunPod Deployment (15-30 min)
4. **Phase 4**: Web Integration (30-60 min)

## Key Changes

### Vector Store API
- **Before**: `connections.connect(host, port)` → Milvus Standalone
- **After**: `MilvusClient(uri="./milvus_lite.db")` → Milvus Lite

### Benefits
- ✅ No Docker dependency
- ✅ Simpler deployment
- ✅ Works on RunPod GPU instances
- ✅ Embedded SQLite-based storage
- ✅ Sufficient for current dataset size

### Trade-offs
- ⚠️ Limited indexing options (acceptable for <100K vectors)
- ⚠️ Single-node only (not an issue for current use case)

## Testing Checklist

Before merging to main:

- [ ] All 19 tests pass locally
- [ ] Document indexing works (ГОСТ 27772-2021.pdf)
- [ ] Extraction returns correct data for C235
- [ ] Query returns relevant results
- [ ] Deployment successful on RunPod
- [ ] Web interface integration functional
- [ ] Performance acceptable (GPU acceleration working)

## Rollback

If migration fails, return to stable version:

```bash
git checkout RAG-Milvus-Manus-Edition
```

The original Milvus Standalone implementation is preserved in the main branch.

## Documentation

- **Migration Plan**: `docs/MILVUS_LITE_MIGRATION.md`
- **Milvus Comparison**: `docs/milvus_comparison.md`
- **Deployment Summary**: `docs/deployment_summary.md`
- **System Architecture**: `docs/SYSTEM_ARCHITECTURE.md`

## Timeline

**Estimated Total**: 1.5-3 hours

| Phase | Duration | Status |
|-------|----------|--------|
| Planning | 30 min | ✅ Complete |
| Code Adaptation | 30-60 min | 🚧 Pending |
| Local Testing | 15-30 min | 🚧 Pending |
| RunPod Deployment | 15-30 min | 🚧 Pending |
| Web Integration | 30-60 min | 🚧 Pending |

## Next Steps

1. Review migration plan
2. Implement code changes in `src/vector_store/milvus_store.py`
3. Update configuration files
4. Run local tests
5. Deploy to RunPod
6. Integrate with web interface
7. Create pull request to merge back to main

## Contact

For questions or issues during migration, refer to:
- Migration plan: `docs/MILVUS_LITE_MIGRATION.md`
- Milvus Lite docs: https://milvus.io/docs/milvus_lite.md
