import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { AlertCircle } from 'lucide-react';
import { ChatHeader } from './ChatHeader';
import { ChatMessage, Message } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { TypingIndicator } from './TypingIndicator';
import { WelcomeScreen } from './WelcomeScreen';
import { IPLDisclaimer } from './IPLDisclaimer';
import { AnimatedBackground } from './AnimatedBackground';
import { askIPLOracle } from '../lib/api';
import { initEmbeddings } from '../lib/embeddings';

export function ChatDashboard() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showWelcome, setShowWelcome] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Initialize embeddings model on mount
  useEffect(() => {
    const initialize = async () => {
      try {
        setIsInitializing(true);
        await initEmbeddings();
        setIsInitializing(false);
      } catch (err) {
        console.error('Failed to initialize:', err);
        setError('Failed to initialize AI model. Please refresh the page.');
        setIsInitializing(false);
      }
    };

    initialize();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (content: string) => {
    // Hide welcome screen after first message
    if (showWelcome) {
      setShowWelcome(false);
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Get response from backend
      const response = await askIPLOracle(content);

      // Create bot message
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: typeof response.answer === 'string' ? response.answer : response.answer.concise,
        structuredContent:
          typeof response.answer === 'object'
            ? {
                concise: response.answer.concise,
                context: response.answer.context,
                resources: response.answer.resources,
              }
            : undefined,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err: any) {
      console.error('Error getting response:', err);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: `Sorry, I encountered an error: ${err.message || 'Unable to process your request'}. Please try again.`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
      setError(err.message || 'Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <AnimatedBackground />
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Header */}
        <ChatHeader />

        {/* Disclaimer */}
        {!showWelcome && <IPLDisclaimer />}

        {/* Messages or Welcome Screen */}
        <div
          ref={messagesContainerRef}
          className="flex-1 overflow-y-auto"
          style={{
            scrollbarWidth: 'thin',
            scrollbarColor: 'rgba(148, 163, 184, 0.3) transparent',
          }}
        >
          {showWelcome ? (
            <WelcomeScreen onGetStarted={() => setShowWelcome(false)} />
          ) : (
            <div className="container mx-auto px-4 py-6">
              <div className="max-w-4xl mx-auto space-y-6">
                {/* Initialization Status */}
                {isInitializing && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="p-4 rounded-xl bg-blue-900/30 border border-blue-500/30 flex items-center gap-3"
                  >
                    <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-sm text-blue-300">
                      Initializing AI model... Downloading ~25MB on first load (cached for future use).
                    </p>
                  </motion.div>
                )}

                {/* Error Alert */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="p-4 rounded-xl bg-red-900/30 border border-red-500/30 flex items-start gap-3"
                    >
                      <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                      <div className="flex-1">
                        <p className="text-sm text-red-300">{error}</p>
                      </div>
                      <button
                        onClick={() => setError(null)}
                        className="text-red-400 hover:text-red-300 transition-colors"
                      >
                        ×
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Messages */}
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}

                {/* Typing Indicator */}
                {isLoading && <TypingIndicator />}

                {/* Scroll Anchor */}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        {!showWelcome && (
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={isLoading || isInitializing}
          />
        )}
      </div>
    </div>
  );
}