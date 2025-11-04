import { useState, KeyboardEvent } from 'react';
import { motion } from 'motion/react';
import { Send } from 'lucide-react';
import { Textarea } from './ui/textarea';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSendMessage(trimmedMessage);
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend = message.trim() && !disabled;

  return (
    <div className="sticky bottom-0 bg-slate-900/90 backdrop-blur-xl border-t border-slate-800/50 p-4">
      <div className="max-w-4xl mx-auto relative">
        <Textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about IPL..."
          disabled={disabled}
          className="min-h-[60px] max-h-[120px] resize-none bg-slate-800/60 border-slate-700/50 focus:border-orange-500/50 rounded-2xl pr-14 text-white placeholder:text-slate-400"
          rows={1}
        />
        
        <motion.button
          onClick={handleSend}
          disabled={!canSend}
          className={`absolute right-2 bottom-2 w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-300 ${
            canSend
              ? 'bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:scale-105 shadow-[0_0_20px_rgba(249,115,22,0.3),0_0_40px_rgba(147,51,234,0.2)]'
              : 'bg-slate-700/50 cursor-not-allowed'
          }`}
          animate={canSend ? {
            scale: [1, 1.05, 1],
          } : {}}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <Send className={`w-5 h-5 ${canSend ? 'text-white' : 'text-slate-500'}`} />
        </motion.button>
      </div>
    </div>
  );
}
