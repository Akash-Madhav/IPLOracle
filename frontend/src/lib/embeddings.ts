/**
 * Generate embeddings for text using Xenova's Transformers.js
 * This provides client-side embedding generation without requiring a separate API call
 */

import { pipeline, Pipeline } from '@xenova/transformers';

let embedder: Pipeline | null = null;

/**
 * Initialize the embedding model (lazy loading)
 */
async function getEmbedder(): Promise<Pipeline> {
  if (!embedder) {
    // Using the same model as backend: all-MiniLM-L6-v2
    embedder = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
  }
  return embedder;
}

/**
 * Generate embedding vector for given text
 * @param text - Text to embed
 * @returns 384-dimensional embedding vector
 */
export async function generateEmbedding(text: string): Promise<number[]> {
  try {
    const model = await getEmbedder();
    const output = await model(text, { pooling: 'mean', normalize: true });
    
    // Convert to regular array
    const embedding = Array.from(output.data as Float32Array);
    return embedding;
  } catch (error) {
    console.error('Error generating embedding:', error);
    throw new Error('Failed to generate text embedding');
  }
}
