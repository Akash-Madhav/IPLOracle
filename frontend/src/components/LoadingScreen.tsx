import { motion } from 'motion/react';
import { Trophy, Loader2 } from 'lucide-react';

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = 'Loading...' }: LoadingScreenProps) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="text-center">
        {/* Animated Logo */}
        <motion.div
          className="relative inline-block mb-8"
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {/* Glow Effect */}
          <motion.div
            className="absolute inset-0 blur-3xl"
            animate={{
              background: [
                'radial-gradient(circle, rgba(249,115,22,0.3) 0%, transparent 70%)',
                'radial-gradient(circle, rgba(147,51,234,0.3) 0%, transparent 70%)',
                'radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%)',
                'radial-gradient(circle, rgba(249,115,22,0.3) 0%, transparent 70%)',
              ],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: 'linear',
            }}
          />

          {/* Trophy Icon */}
          <div className="relative w-24 h-24 rounded-2xl bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 backdrop-blur-xl border border-orange-500/30 flex items-center justify-center">
            <Trophy className="w-12 h-12 text-orange-400" />
          </div>
        </motion.div>

        {/* App Name */}
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-3xl mb-3 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent"
        >
          IPL Oracle
        </motion.h1>

        {/* Loading Message */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="flex items-center justify-center gap-3"
        >
          <Loader2 className="w-5 h-5 text-orange-400 animate-spin" />
          <p className="text-slate-400">{message}</p>
        </motion.div>

        {/* Progress Dots */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="flex items-center justify-center gap-2 mt-6"
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-orange-400 to-purple-400"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.3, 1, 0.3],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2,
              }}
            />
          ))}
        </motion.div>
      </div>
    </div>
  );
}
