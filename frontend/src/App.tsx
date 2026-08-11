import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LandingPage } from './components/LandingPage';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { ChatDashboard } from './components/ChatDashboard';
import { ErrorBoundary } from './components/ErrorBoundary';
import { startHealthPing } from './lib/api';

type Page = 'landing' | 'login' | 'register' | 'dashboard';

function AppContent() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const { user, loading } = useAuth();

  // Start background health ping to keep backend warm and prevent sleep
  useEffect(() => {
    const cleanup = startHealthPing(300000); // Ping every 5 minutes
    return cleanup;
  }, []);

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated, show chat dashboard
  if (user) {
    return <ChatDashboard />;
  }

  // Show appropriate page based on navigation state
  switch (currentPage) {
    case 'login':
      return (
        <Login
          onSwitchToRegister={() => setCurrentPage('register')}
          onBackToLanding={() => setCurrentPage('landing')}
        />
      );
    
    case 'register':
      return (
        <Register
          onSwitchToLogin={() => setCurrentPage('login')}
          onBackToLanding={() => setCurrentPage('landing')}
        />
      );
    
    case 'landing':
    default:
      return (
        <LandingPage
          onGetStarted={() => setCurrentPage('login')}
        />
      );
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ErrorBoundary>
  );
}