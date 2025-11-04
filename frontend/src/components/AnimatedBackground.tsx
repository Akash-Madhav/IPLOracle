import { motion } from 'motion/react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Animated Orb 1 - Orange/Amber (Top Left) */}
      <motion.div
        className="absolute -top-40 -left-40 w-96 h-96 bg-gradient-to-br from-orange-500 to-amber-500 rounded-full opacity-30 blur-[120px]"
        animate={{
          x: [0, 100, -50, 0],
          y: [0, -100, 50, 0],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear"
        }}
      />

      {/* Animated Orb 2 - Purple/Pink (Top Right) */}
      <motion.div
        className="absolute -top-20 -right-20 w-[500px] h-[500px] bg-gradient-to-br from-purple-500 to-pink-500 rounded-full opacity-25 blur-[150px]"
        animate={{
          x: [0, -80, 60, 0],
          y: [0, 100, -80, 0],
        }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "linear"
        }}
      />

      {/* Animated Orb 3 - Blue/Cyan (Bottom Left) */}
      <motion.div
        className="absolute -bottom-32 -left-32 w-[600px] h-[600px] bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full opacity-20 blur-[140px]"
        animate={{
          x: [0, 120, -100, 0],
          y: [0, -80, 100, 0],
        }}
        transition={{
          duration: 40,
          repeat: Infinity,
          ease: "linear"
        }}
      />

      {/* Animated Orb 4 - Teal/Emerald (Bottom Right) */}
      <motion.div
        className="absolute -bottom-40 -right-40 w-[550px] h-[550px] bg-gradient-to-br from-teal-500 to-emerald-500 rounded-full opacity-25 blur-[130px]"
        animate={{
          x: [0, -100, 80, 0],
          y: [0, 80, -60, 0],
        }}
        transition={{
          duration: 38,
          repeat: Infinity,
          ease: "linear"
        }}
      />
    </div>
  );
}
