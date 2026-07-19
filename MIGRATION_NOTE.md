# Migration to Local ONNX Embeddings

## Important Change

The ATLAS memory system has been migrated from **Gemini API embeddings (3072 dimensions)** to **local ONNX embeddings (384 dimensions)**.

## What This Means

1. **New Collection**: The system now uses a new ChromaDB collection named `atlas_memory_onnx` (instead of `atlas_memory`)

2. **Previous Memories**: Your old memories stored with Gemini embeddings are preserved in the old collection but won't be accessible in the new system due to dimension mismatch

3. **Fresh Start**: The new system starts with an empty memory that will be populated as you use ATLAS

## Benefits

✅ **Fully Local**: No external API calls for embeddings
✅ **Faster**: Local embeddings are much quicker
✅ **More Private**: Your data never leaves your machine
✅ **No API Key Needed**: No more `GEMINI_API_KEY` requirement
✅ **Cost-Free**: No API usage costs

## If You Want to Keep Old Memories

If you have important memories in the old collection and want to migrate them:

1. The old collection `atlas_memory` still exists in `data/chroma_db`
2. You would need to:
   - Export memories from the old collection
   - Re-embed them using the new ONNX model
   - Import into the new collection

This is optional. The system works fine starting fresh.

## Technical Details

- **Old System**: Gemini API `text-embedding-004` (3072 dimensions)
- **New System**: Local ONNX `all-MiniLM-L6-v2` (384 dimensions)
- **Old Collection**: `atlas_memory` (preserved but inactive)
- **New Collection**: `atlas_memory_onnx` (active)

## No Action Required

The system automatically uses the new embedding model. Just restart ATLAS and it will work with the new local embeddings.
