let worker: Worker | null = null;
let messageId = 0;
let isInitialized = false;
let initializationPromise: Promise<void> | null = null;

/**
 * Create worker from inline code to avoid module resolution issues
 */
function createWorker(): Worker {
  const workerCode = `
    import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js';

    // Configure for browser environment
    env.allowLocalModels = false;
    env.useBrowserCache = true;

    let embeddingPipeline = null;

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
            throw new Error(\`Expected 384 dimensions, got \${embedding.length}\`);
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
  `;

  const blob = new Blob([workerCode], { type: 'application/javascript' });
  const workerUrl = URL.createObjectURL(blob);
  return new Worker(workerUrl, { type: 'module' });
}

/**
 * Initialize the embedding worker
 */
export async function initEmbeddings(): Promise<void> {
  // Return existing initialization promise if already initializing
  if (initializationPromise) {
    return initializationPromise;
  }

  // Already initialized
  if (isInitialized && worker) {
    return Promise.resolve();
  }

  initializationPromise = new Promise((resolve, reject) => {
    try {
      // Create worker with inline code
      worker = createWorker();

      const timeoutId = setTimeout(() => {
        reject(new Error('Worker initialization timeout'));
      }, 60000); // 60 second timeout

      // Handle worker errors
      worker.onerror = (error) => {
        clearTimeout(timeoutId);
        console.error('Worker error:', error);
        reject(new Error('Worker failed to start'));
      };

      // Send initialization message
      const id = messageId++;
      const initHandler = (event: MessageEvent) => {
        if (event.data.id === id && event.data.type === 'init') {
          clearTimeout(timeoutId);
          worker?.removeEventListener('message', initHandler);
          isInitialized = true;
          resolve();
        } else if (event.data.id === id && event.data.type === 'error') {
          clearTimeout(timeoutId);
          worker?.removeEventListener('message', initHandler);
          reject(new Error(event.data.error));
        }
      };

      worker.addEventListener('message', initHandler);
      worker.postMessage({ id, type: 'init' });
    } catch (error) {
      initializationPromise = null;
      console.error('Failed to create worker:', error);
      reject(error);
    }
  });

  return initializationPromise;
}

/**
 * Generate a 384-dimensional embedding for a given text query
 * @param text The input text to embed
 * @returns A 384-dimensional embedding vector
 */
export async function generateEmbedding(text: string): Promise<number[]> {
  try {
    // Ensure worker is initialized
    if (!isInitialized || !worker) {
      await initEmbeddings();
    }

    if (!worker) {
      throw new Error('Worker not initialized');
    }

    return new Promise((resolve, reject) => {
      const id = messageId++;
      const timeoutId = setTimeout(() => {
        reject(new Error('Embedding generation timeout'));
      }, 30000); // 30 second timeout

      const handler = (event: MessageEvent) => {
        if (event.data.id === id) {
          clearTimeout(timeoutId);
          worker?.removeEventListener('message', handler);

          if (event.data.type === 'embed') {
            resolve(event.data.embedding);
          } else if (event.data.type === 'error') {
            reject(new Error(event.data.error));
          }
        }
      };

      if (!worker) {
        throw new Error('Worker not initialized');
      }
      worker.addEventListener('message', handler);
      worker.postMessage({ id, type: 'embed', text });
    });
  } catch (error) {
    console.error('Failed to generate embedding:', error);
    throw new Error('Failed to generate embedding for query');
  }
}

/**
 * Clean up the worker
 */
export function cleanupEmbeddings(): void {
  if (worker) {
    worker.terminate();
    worker = null;
    isInitialized = false;
    initializationPromise = null;
  }
}
