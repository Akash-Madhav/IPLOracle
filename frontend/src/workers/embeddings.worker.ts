import { pipeline, env } from '@xenova/transformers';

// Configure for browser environment
env.allowLocalModels = false;
env.useBrowserCache = true;

let embeddingPipeline: any = null;

// Listen for messages from the main thread
self.addEventListener('message', async (event) => {
  const { id, type, text } = event.data;

  try {
    if (type === 'init') {
      // Initialize the pipeline
      if (!embeddingPipeline) {
        embeddingPipeline = await pipeline(
          'feature-extraction',
          'Xenova/all-MiniLM-L6-v2'
        );
      }
      self.postMessage({ id, type: 'init', success: true });
    } else if (type === 'embed') {
      // Ensure pipeline is initialized
      if (!embeddingPipeline) {
        embeddingPipeline = await pipeline(
          'feature-extraction',
          'Xenova/all-MiniLM-L6-v2'
        );
      }

      // Generate embedding
      const output = await embeddingPipeline(text, {
        pooling: 'mean',
        normalize: true,
      });

      // Convert to array
      const embedding = Array.from(output.data);

      // Verify dimensions
      if (embedding.length !== 384) {
        throw new Error(`Expected 384 dimensions, got ${embedding.length}`);
      }

      self.postMessage({ id, type: 'embed', embedding });
    }
  } catch (error) {
    self.postMessage({
      id,
      type: 'error',
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});
