import { motion } from 'motion/react';
import { User, Bot, ExternalLink } from 'lucide-react';

export interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  structuredContent?: {
    concise: string;
    context: string;
    resources?: Array<{
      title?: string;
      url?: string;
      snippet?: string;
      [key: string]: any;
    }>;
  };
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.type === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-start gap-3 max-w-4xl ${isUser ? 'ml-auto flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
          isUser
            ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-blue-500/30'
            : 'bg-gradient-to-br from-orange-500/20 via-purple-500/20 to-blue-500/20 border border-orange-500/30'
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-blue-400" />
        ) : (
          <Bot className="w-4 h-4 text-orange-400" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 ${isUser ? 'flex justify-end' : ''}`}>
        <div
          className={`rounded-2xl px-6 py-4 ${
            isUser
              ? 'bg-gradient-to-br from-blue-600/30 via-purple-600/30 to-blue-600/20 border border-blue-500/30'
              : 'bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 border border-white/10'
          } backdrop-blur-xl`}
        >
          {/* Main Content */}
          {message.structuredContent ? (
            <div className="space-y-4">
              {/* Concise Answer */}
              <div>
                <p className="text-slate-100 leading-relaxed whitespace-pre-wrap">
                  {message.structuredContent.concise}
                </p>
              </div>

              {/* Context (if different from concise) */}
              {message.structuredContent.context &&
                message.structuredContent.context !== message.structuredContent.concise && (
                  <div className="pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 mb-2">Additional Context:</p>
                    <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
                      {message.structuredContent.context}
                    </p>
                  </div>
                )}

              {/* Resources */}
              {message.structuredContent.resources &&
                message.structuredContent.resources.length > 0 && (
                  <div className="pt-4 border-t border-white/10">
                    <p className="text-sm text-slate-400 mb-3">Sources:</p>
                    <div className="space-y-2">
                      {message.structuredContent.resources.map((resource, idx) => (
                        <div
                          key={idx}
                          className="p-3 rounded-lg bg-slate-900/30 border border-white/5 hover:border-orange-500/30 transition-colors"
                        >
                          {resource.title && (
                            <div className="flex items-start justify-between gap-2 mb-1">
                              <p className="text-sm text-orange-400">
                                {resource.title}
                              </p>
                              {resource.url && (
                                <a
                                  href={resource.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex-shrink-0 text-blue-400 hover:text-blue-300 transition-colors"
                                >
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              )}
                            </div>
                          )}
                          {resource.snippet && (
                            <p className="text-xs text-slate-400 line-clamp-2">
                              {resource.snippet}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
            </div>
          ) : (
            <p className="text-slate-100 leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          )}

          {/* Timestamp */}
          <p className="text-xs text-slate-500 mt-3">
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
