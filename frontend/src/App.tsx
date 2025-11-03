import { useState, useEffect, useRef } from "react";
import { motion } from "motion/react";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { ChatHeader } from "./components/ChatHeader";
import { ChatMessage } from "./components/ChatMessage";
import { ChatInput } from "./components/ChatInput";
import { TypingIndicator } from "./components/TypingIndicator";
import { MedicalDisclaimer } from "./components/MedicalDisclaimer";
import { WelcomeScreen } from "./components/WelcomeScreen";
import { AnimatedBackground } from "./components/AnimatedBackground";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

function ChatApp() {
  const { currentUser } = useAuth();
  const [authView, setAuthView] = useState<"login" | "register">("login");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  // ✅ Always dark mode
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  // ✅ Initial welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: "welcome",
      text: "👩‍⚕️ Hello! I'm Dr. Athena, your medical insight assistant. Ask your medical questions and I'll provide evidence-based insights. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
    setIsLoadingHistory(false);
  }, []);

  // ✅ Auto scroll to latest message
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // ✅ Handle message sending
  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      text,
      isUser: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      console.log("🟡 Sending query to backend:", text);

      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text }),
      });

      console.log("🟢 Received response:", response);

      const data = await response.json();
      console.log("🔵 Backend JSON:", data);

      // ✅ Handle backend JSON structure
      const concise = data?.answer?.concise || "";
      const context = data?.answer?.context || "";
      const resources =
        data?.answer?.resources && Array.isArray(data.answer.resources)
          ? data.answer.resources
          : [];

      const botText =
        concise || context
          ? `**🩺 Concise:** ${concise}\n\n**📖 Context:** ${context}`
          : "⚠️ No response received from backend.";

      const sourcesText =
        resources.length > 0
          ? `\n\n📚 **Sources:**\n${resources
              .map(
                (s: any, i: number) =>
                  `${i + 1}. ${s.name}: ${s.snippet || ""}`
              )
              .join("\n")}`
          : "";

      const fullBotText = botText + sourcesText;

      const botMsg: Message = {
        id: `bot-${Date.now()}`,
        text: fullBotText,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("❌ Error fetching backend:", error);
      const errMsg: Message = {
        id: `error-${Date.now()}`,
        text: "⚠️ Sorry, something went wrong. Please try again.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  // ✅ Auth handling
  if (!currentUser) {
    return authView === "login" ? (
      <Login onSwitchToRegister={() => setAuthView("register")} />
    ) : (
      <Register onSwitchToLogin={() => setAuthView("login")} />
    );
  }

  // ✅ Main chat UI
  return (
    <div className="relative h-screen flex flex-col overflow-hidden">
      <AnimatedBackground />
      <div className="relative z-10 h-screen flex flex-col">
        <ChatHeader />
        <MedicalDisclaimer />
        <div className="flex-1 overflow-hidden">
          <div
            ref={scrollRef}
            className="h-full overflow-y-auto px-4 py-6 scrollbar-thin scrollbar-thumb-cyan-500/20 scrollbar-track-transparent"
          >
            <div className="max-w-6xl mx-auto">
              {isLoadingHistory ? (
                <div className="flex items-center justify-center h-full">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full"
                  />
                </div>
              ) : (
                <>
                  {messages.length === 1 && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.8, delay: 0.5 }}
                    >
                      <WelcomeScreen />
                    </motion.div>
                  )}

                  {messages.map((msg) => (
                    <ChatMessage
                      key={msg.id}
                      message={msg.text}
                      isUser={msg.isUser}
                      timestamp={msg.timestamp}
                    />
                  ))}

                  {isTyping && <TypingIndicator />}
                </>
              )}
            </div>
          </div>
        </div>
        <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <ChatApp />
    </AuthProvider>
  );
}
