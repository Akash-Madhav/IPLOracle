import { motion } from 'motion/react';
import { Trophy, TrendingUp, Users, BarChart3, Shield, Sparkles, Zap, ArrowRight } from 'lucide-react';
import { AnimatedBackground } from './AnimatedBackground';

interface LandingPageProps {
  onGetStarted: () => void;
}

export function LandingPage({ onGetStarted }: LandingPageProps) {
  const features = [
    {
      icon: Trophy,
      title: 'Match Analytics',
      description: 'Real-time match insights, live scores, and comprehensive match analysis',
      gradient: 'from-orange-500 to-orange-600',
      glowColor: 'orange',
    },
    {
      icon: TrendingUp,
      title: 'Predictions & Stats',
      description: 'AI-powered predictions, historical statistics, and trending analytics',
      gradient: 'from-blue-500 to-blue-600',
      glowColor: 'blue',
    },
    {
      icon: Users,
      title: 'Player Intelligence',
      description: 'Detailed player profiles, performance metrics, and career statistics',
      gradient: 'from-purple-500 to-purple-600',
      glowColor: 'purple',
    },
    {
      icon: BarChart3,
      title: 'Team Comparisons',
      description: 'In-depth team analysis, head-to-head records, and strategic insights',
      gradient: 'from-teal-500 to-teal-600',
      glowColor: 'teal',
    },
  ];

  const badges = [
    {
      icon: Shield,
      text: 'Secure authentication powered by Firebase',
    },
    {
      icon: Sparkles,
      text: 'AI-powered insights & real-time data',
    },
    {
      icon: Zap,
      text: 'Lightning-fast responses',
    },
  ];

  return (
    <div className="min-h-screen w-full text-white relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 container mx-auto px-4 py-12 md:py-20">
        {/* Hero Section */}
        <div className="flex flex-col items-center text-center mb-20 md:mb-32">
          {/* Animated Trophy Icon */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{
              type: "spring",
              stiffness: 200,
              damping: 20,
              duration: 0.8,
            }}
            className="relative mb-8"
          >
            <motion.div
              className="relative p-8 rounded-3xl bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600"
              animate={{
                boxShadow: [
                  '0 0 20px rgba(249, 115, 22, 0.5), 0 0 40px rgba(147, 51, 234, 0.3)',
                  '0 0 40px rgba(249, 115, 22, 0.7), 0 0 60px rgba(147, 51, 234, 0.5)',
                  '0 0 20px rgba(249, 115, 22, 0.5), 0 0 40px rgba(147, 51, 234, 0.3)',
                ],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <Trophy className="w-16 h-16 md:w-20 md:h-20" />
            </motion.div>
          </motion.div>

          {/* Hero Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="space-y-6 max-w-4xl"
          >
            <h1 className="bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 bg-clip-text text-transparent text-5xl md:text-7xl">
              IPL Oracle
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-300">
              Your AI-Powered Cricket Intelligence
            </p>
            
            <p className="text-slate-400 max-w-2xl mx-auto text-base md:text-lg px-4">
              Experience the future of cricket analytics with IPL Oracle. Get instant access to match predictions, 
              player statistics, team comparisons, and real-time insights powered by advanced AI technology. 
              Your ultimate companion for the Indian Premier League.
            </p>

            {/* CTA Button */}
            <motion.button
              onClick={onGetStarted}
              className="group relative mt-8 px-8 py-4 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full overflow-hidden"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.8 }}
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-orange-600 via-purple-700 to-blue-700 opacity-0 group-hover:opacity-100 transition-opacity"
                animate={{
                  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "linear",
                }}
              />
              <span className="relative flex items-center gap-2 text-lg">
                Get Started
                <motion.div
                  className="inline-block"
                  animate={{ x: [0, 5, 0] }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                >
                  <ArrowRight className="w-5 h-5" />
                </motion.div>
              </span>
              <motion.div
                className="absolute inset-0 rounded-full"
                animate={{
                  boxShadow: [
                    '0 0 20px rgba(249, 115, 22, 0.5)',
                    '0 0 40px rgba(147, 51, 234, 0.7)',
                    '0 0 20px rgba(249, 115, 22, 0.5)',
                  ],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              />
            </motion.button>
          </motion.div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  delay: 0.7 + index * 0.1,
                  duration: 0.8,
                  ease: "easeOut",
                }}
                whileHover={{ 
                  y: -10,
                  transition: { duration: 0.2 }
                }}
                className="group relative"
              >
                {/* Radial glow on hover */}
                <motion.div
                  className={`absolute inset-0 rounded-2xl bg-${feature.glowColor}-500/0 blur-xl group-hover:bg-${feature.glowColor}-500/20 transition-all duration-500`}
                  initial={{ opacity: 0 }}
                  whileHover={{ opacity: 1 }}
                />
                
                {/* Card */}
                <div className="relative h-full p-6 rounded-2xl bg-slate-800/60 backdrop-blur-xl border border-slate-700/30 overflow-hidden">
                  {/* Gradient overlay */}
                  <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${feature.gradient}`} />
                  
                  {/* Icon */}
                  <div className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${feature.gradient} mb-4`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400 text-sm">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Footer Badges */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1, duration: 0.8 }}
          className="flex flex-col md:flex-row items-center justify-center gap-4 px-4"
        >
          {badges.map((badge, index) => {
            const Icon = badge.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.2 + index * 0.1 }}
                className="flex items-center gap-3 px-6 py-3 rounded-full bg-slate-800/60 backdrop-blur-xl border border-slate-700/30"
              >
                <Icon className="w-5 h-5 text-slate-400" />
                <span className="text-slate-300 text-sm whitespace-nowrap">
                  {badge.text}
                </span>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </div>
  );
}
