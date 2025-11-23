# Embedding Worker Setup

## Problem
The Transformer.js library was trying to use Node.js file system APIs (specifically `fileURLToPath` from the `node:url` module) which aren't available in the browser environment, causing the error:

```
TypeError: The URL must be of scheme file
    at Object.Z14 [as fileURLToPath] (https://esm.sh/node/url.mjs:1:2180)
```

## Solution
To resolve this, we've moved the embedding generation to a Web Worker. This isolates the Transformer.js library in a separate thread and properly configures it for browser usage.

## Architecture

### 1. Web Worker (`/workers/embeddings.worker.ts`)
- Runs in a separate thread, preventing UI blocking
- Loads the `Xenova/all-MiniLM-L6-v2` model (generates 384-dimensional embeddings)
- Handles two message types:
  - `init`: Initializes the embedding pipeline
  - `embed`: Generates embeddings for given text

### 2. Embeddings Library (`/lib/embeddings.ts`)
- Creates and manages the Web Worker
- Provides clean API: `initEmbeddings()` and `generateEmbedding(text)`
- Handles message passing between main thread and worker
- Implements timeouts and error handling

### 3. Integration (`/components/ChatDashboard.tsx`)
- Initializes embeddings on component mount
- Shows initialization status to users
- Handles initialization errors gracefully

## Benefits

1. **Browser Compatible**: No Node.js dependencies in browser environment
2. **Non-Blocking**: Model loading and inference run in separate thread
3. **User Feedback**: Clear loading states and error messages
4. **Caching**: Model is cached after first download (~25MB)
5. **Error Resilience**: Comprehensive error handling and timeouts

## Usage

```typescript
// Initialize (usually done once on app load)
await initEmbeddings();

// Generate embedding
const embedding = await generateEmbedding("Who won IPL 2024?");
// Returns: number[] with 384 dimensions
```

## First Load Experience
- Downloads ~25MB model on first use
- Shows "Initializing AI model... Downloading ~25MB on first load (cached for future use)"
- Subsequent loads use cached model (instant)

## Technical Details
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` via Xenova/transformers
- **Dimensions**: 384
- **Pooling**: Mean pooling with normalization
- **Worker Type**: ES Module
- **Timeouts**: 60s for init, 30s for embedding generation
