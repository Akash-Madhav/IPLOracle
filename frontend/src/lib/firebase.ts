import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAWan1dt-4vnZkt8-HDpLq72_OSg_M7-to",
  authDomain: "iploracle-4c00d.firebaseapp.com",
  projectId: "iploracle-4c00d",
  storageBucket: "iploracle-4c00d.firebasestorage.app",
  messagingSenderId: "3627329638",
  appId: "1:3627329638:web:d185ef1b341ec3c6b3a5a7",
  measurementId: "G-8VJG4NBX6L"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export default app;