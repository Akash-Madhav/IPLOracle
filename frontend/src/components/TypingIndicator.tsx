import { motion } from 'motion/react';
import { Trophy } from 'lucide-react';

export function TypingIndicator() {
  return (
    <motion.div
      className="flex items-start gap-3 max-w-xs mb-4"
      initial={{ opacity: 0, x: -20, scale: 0.95 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex-shrink-0">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-md opacity-40"></div>
          <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-2 rounded-full">
            <Trophy className="w-4 h-4 text-white" />
          </div>
        </div>
      </div>

      <div className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-2xl px-4 py-3">
        <div className="flex gap-1">
          {[0, 1, 2].map((index) => (
            <motion.div
              key={index}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-orange-500 to-purple-500"
              animate={{
                y: [0, -8, 0]
              }}
              transition={{
                duration: 0.6,
                repeat: Infinity,
                delay: index * 0.2,
                ease: "easeInOut"
              }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
