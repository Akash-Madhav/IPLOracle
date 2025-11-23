import { motion } from 'motion/react';

export function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 max-w-4xl">
      {/* Bot Avatar */}
      <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-orange-500/20 via-purple-500/20 to-blue-500/20 border border-orange-500/30 flex items-center justify-center">
        <div className="w-3 h-3 rounded-full bg-gradient-to-r from-orange-400 to-purple-400"></div>
      </div>

      {/* Typing Animation */}
      <div className="flex-1 rounded-2xl bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 backdrop-blur-xl border border-white/10 px-6 py-4">
        <div className="flex items-center gap-2">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-orange-400 to-purple-400"
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                delay: i * 0.2,
              }}
            />
          ))}
          <span className="ml-2 text-sm text-slate-400">IPL Oracle is thinking...</span>
        </div>
      </div>
    </div>
  );
}
