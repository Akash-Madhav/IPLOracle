import { useState, KeyboardEvent } from 'react';
import { motion } from 'motion/react';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="sticky bottom-0 border-t border-white/10 bg-slate-950/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-end gap-3 p-4 rounded-2xl bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 backdrop-blur-xl border border-white/10">
            {/* Text Input */}
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything about IPL..."
              disabled={disabled}
              rows={1}
              className="flex-1 bg-transparent text-slate-100 placeholder-slate-500 resize-none focus:outline-none min-h-[40px] max-h-[120px] overflow-y-auto disabled:opacity-50"
              style={{
                scrollbarWidth: 'thin',
                scrollbarColor: 'rgba(148, 163, 184, 0.3) transparent',
              }}
            />

            {/* Send Button */}
            <motion.button
              whileHover={{ scale: disabled ? 1 : 1.05 }}
              whileTap={{ scale: disabled ? 1 : 0.95 }}
              onClick={handleSubmit}
              disabled={disabled || !message.trim()}
              className="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 disabled:from-slate-700 disabled:via-slate-700 disabled:to-slate-700 disabled:opacity-50 flex items-center justify-center transition-all group"
            >
              {disabled ? (
                <Loader2 className="w-5 h-5 text-white animate-spin" />
              ) : (
                <Send className="w-5 h-5 text-white group-hover:scale-110 transition-transform" />
              )}
            </motion.button>
          </div>

          {/* Helper Text */}
          <p className="text-xs text-slate-500 mt-2 text-center">
            Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-white/10">Enter</kbd> to send,{' '}
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-white/10">Shift+Enter</kbd> for new line
          </p>
        </div>
      </div>
    </div>
  );
}
