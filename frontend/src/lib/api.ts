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

/**
 * Ping backend health endpoint to check status and prevent backend spin-down / sleep on free hosting (e.g. Render)
 */
export async function checkBackendHealth(): Promise<{ status: string; ok: boolean }> {
  try {
    const res = await fetch(`${API_URL}/health`, { method: 'GET', cache: 'no-store' });
    if (res.ok) {
      const data = await res.json();
      return { status: data.status || 'ok', ok: true };
    }
    return { status: 'degraded', ok: false };
  } catch (error) {
    console.warn('Backend health ping failed:', error);
    return { status: 'offline', ok: false };
  }
}

/**
 * Start recurring background health ping to keep backend active and prevent idle spin-down.
 * Defaults to pinging every 5 minutes (300,000 ms).
 */
export function startHealthPing(intervalMs: number = 300000): () => void {
  // Initial immediate wake-up ping
  checkBackendHealth();

  // Periodic recurring ping
  const intervalId = setInterval(() => {
    checkBackendHealth();
  }, intervalMs);

  // Ping when browser tab becomes active again
  const handleVisibilityChange = () => {
    if (document.visibilityState === 'visible') {
      checkBackendHealth();
    }
  };

  if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', handleVisibilityChange);
  }

  // Cleanup function
  return () => {
    clearInterval(intervalId);
    if (typeof document !== 'undefined') {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    }
  };
}