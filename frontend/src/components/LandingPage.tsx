import { motion } from 'motion/react';
import { Trophy, BarChart3, TrendingUp, Users, UserPlus, MessageSquare, Zap } from 'lucide-react';
import { AnimatedBackground } from './AnimatedBackground';
import { Button } from './ui/button';

interface LandingPageProps {
  onNavigateToLogin: () => void;
  onNavigateToRegister: () => void;
}

export function LandingPage({ onNavigateToLogin, onNavigateToRegister }: LandingPageProps) {
  const features = [
    {
      icon: BarChart3,
      title: 'Match Analytics',
      description: 'Real-time match stats and comprehensive analysis',
      gradient: 'from-orange-500 to-amber-500'
    },
    {
      icon: TrendingUp,
      title: 'Match Predictions',
      description: 'AI-powered match outcome predictions',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: Users,
      title: 'Player Intelligence',
      description: 'Detailed player stats and insights',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Trophy,
      title: 'Team Comparisons',
      description: 'Head-to-head team analysis',
      gradient: 'from-teal-500 to-emerald-500'
    }
  ];

  const steps = [
    { icon: UserPlus, title: 'Create Account', description: 'Sign up in seconds' },
    { icon: MessageSquare, title: 'Ask Questions', description: 'Chat with AI assistant' },
    { icon: Zap, title: 'Get Insights', description: 'Receive instant answers' }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 py-12 md:py-20">
        {/* Hero Section */}
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          <motion.div
            className="inline-block mb-8"
            initial={{ opacity: 0, y: 20, rotate: -10 }}
            animate={{ opacity: 1, y: 0, rotate: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
          >
            <div className="relative">
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-2xl opacity-50"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 0.7, 0.5]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-6 rounded-full">
                <Trophy className="w-20 h-20 text-white" />
              </div>
            </div>
          </motion.div>

          <motion.h1
            className="text-5xl md:text-7xl mb-6 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            IPL Oracle
          </motion.h1>

          <motion.p
            className="text-xl md:text-2xl text-slate-300 mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            Your AI-Powered Cricket Intelligence Assistant
          </motion.p>

          <motion.p
            className="text-slate-400 max-w-2xl mx-auto mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            Get instant insights on IPL matches, players, teams, and predictions. 
            Your personal cricket expert powered by cutting-edge AI technology.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <Button
              onClick={onNavigateToRegister}
              className="bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:shadow-[0_0_30px_rgba(249,115,22,0.4),0_0_60px_rgba(147,51,234,0.3)] transition-all duration-300 px-8 py-6 text-lg"
            >
              Get Started
            </Button>
            <Button
              onClick={onNavigateToLogin}
              variant="outline"
              className="border-slate-700/50 hover:border-orange-500/50 bg-slate-800/30 backdrop-blur-xl px-8 py-6 text-lg transition-all duration-300"
            >
              Sign In
            </Button>
          </motion.div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          className="mb-20"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.7 }}
        >
          <h2 className="text-3xl md:text-4xl text-center mb-12 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
            Powerful Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-3xl p-8 hover:scale-105 hover:shadow-[0_0_30px_rgba(249,115,22,0.2)] transition-all duration-300"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
              >
                <div className={`inline-block bg-gradient-to-br ${feature.gradient} p-4 rounded-2xl mb-4`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl mb-3 text-slate-100">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div
          className="mb-20"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
        >
          <h2 className="text-3xl md:text-4xl text-center mb-12 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {steps.map((step, index) => (
              <motion.div
                key={step.title}
                className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-3xl p-8 text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 1.3 + index * 0.1 }}
              >
                <div className="inline-block bg-gradient-to-br from-orange-500 to-purple-600 p-4 rounded-2xl mb-4">
                  <step.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl mb-2 text-slate-100">{step.title}</h3>
                <p className="text-slate-400">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Footer */}
        <motion.div
          className="text-center text-slate-500"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 1.6 }}
        >
          <p className="mb-2">IPL Oracle</p>
          <p className="text-sm">Powered by Firebase & AI • © 2025</p>
        </motion.div>
      </div>
    </div>
  );
}
