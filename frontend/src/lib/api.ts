/// <reference types="vite/client" />
import { generateEmbedding } from './embeddings';

const API_URL = typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL 
  ? import.meta.env.VITE_API_URL 
  : 'https://iploracle-2wxn.onrender.com';

export interface ChatResponse {
  query: string;
  answer: string | {
    concise: string;
    context: string;
    resources?: any[];
  };
  results?: any[];
}

/**
 * Send a query to the IPL Oracle backend
 * @param query The user's question
 * @returns The chatbot's response
 */
export async function askIPLOracle(query: string): Promise<ChatResponse> {
  try {
    // Generate embedding for the query
    const vector = await generateEmbedding(query);

    // Send request to backend
    const response = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        vector,
      }),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to get response from IPL Oracle:', error);
    throw error;
  }
}