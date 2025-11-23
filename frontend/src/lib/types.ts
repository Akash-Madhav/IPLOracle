/**
 * Type definitions for IPL Oracle application
 */

// API Types
export interface IPLOracleRequest {
  query: string;
  vector: number[];
}

export interface IPLOracleResponse {
  query: string;
  answer: string | StructuredAnswer;
  results?: QueryResult[];
}

export interface StructuredAnswer {
  concise: string;
  context: string;
  resources?: Resource[];
}

export interface Resource {
  title?: string;
  url?: string;
  snippet?: string;
  [key: string]: any;
}

export interface QueryResult {
  [key: string]: any;
}

// Chat Types
export interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  structuredContent?: StructuredAnswer;
  timestamp: Date;
}

// Auth Types
export interface User {
  uid: string;
  email: string;
  displayName?: string;
}

export interface AuthError {
  code: string;
  message: string;
}

// UI State Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface ErrorState {
  message: string;
  code?: string;
  details?: any;
}
