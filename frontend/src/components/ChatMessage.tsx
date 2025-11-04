import { motion } from 'motion/react';
import { Trophy, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: Date;
}

export function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  const formattedTime = timestamp.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });

  if (isUser) {
    return (
      <motion.div
        className="flex items-start gap-3 justify-end mb-4"
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
      >
        <div className="flex flex-col items-end max-w-[80%]">
          <div className="bg-gradient-to-r from-orange-600 to-purple-600 rounded-2xl rounded-br-md px-4 py-3 shadow-lg">
            <p className="text-white whitespace-pre-wrap break-words">{message}</p>
          </div>
          <span className="text-xs text-slate-500 mt-1">{formattedTime}</span>
        </div>

        <div className="flex-shrink-0">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-orange-500 to-blue-600 rounded-full blur-md opacity-40"></div>
            <div className="relative bg-gradient-to-br from-orange-500 to-blue-600 p-2 rounded-full">
              <User className="w-4 h-4 text-white" />
            </div>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="flex items-start gap-3 mb-4"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <div className="flex-shrink-0">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-md opacity-40"></div>
          <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-2 rounded-full">
            <Trophy className="w-4 h-4 text-white" />
          </div>
        </div>
      </div>

      <div className="flex flex-col max-w-[80%]">
        <div className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-2xl rounded-bl-md px-4 py-3 shadow-lg">
          <p className="text-slate-100 whitespace-pre-wrap break-words">{message}</p>
        </div>
        <span className="text-xs text-slate-400 mt-1">{formattedTime}</span>
      </div>
    </motion.div>
  );
}
