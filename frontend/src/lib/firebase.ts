import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator, initializeFirestore } from 'firebase/firestore';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC6T_ltsKFhHZhB528m157d0opolFoZjuM",
  authDomain: "n8n-medi-rag.firebaseapp.com",
  databaseURL: "https://n8n-medi-rag-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "n8n-medi-rag",
  storageBucket: "n8n-medi-rag.firebasestorage.app",
  messagingSenderId: "829241911025",
  appId: "1:829241911025:web:8d53b5e293802446fa6b50",
  measurementId: "G-RD9VX5F8FN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);

// Initialize Firestore with settings to handle connection issues gracefully
export const db = initializeFirestore(app, {
  ignoreUndefinedProperties: true,
});
