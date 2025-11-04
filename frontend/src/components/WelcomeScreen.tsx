import { motion } from 'motion/react';
import { Trophy, Radio, Users, BarChart3, TrendingUp } from 'lucide-react';
import { Badge } from './ui/badge';

export function WelcomeScreen() {
  const features = [
    {
      icon: Radio,
      title: 'Live Match Updates',
      description: 'Real-time scores and match analysis',
      gradient: 'from-orange-500 to-amber-500'
    },
    {
      icon: Users,
      title: 'Player Statistics',
      description: 'Comprehensive player performance data',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: BarChart3,
      title: 'Team Analysis',
      description: 'In-depth team comparisons and stats',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: TrendingUp,
      title: 'Match Predictions',
      description: 'AI-powered outcome predictions',
      gradient: 'from-teal-500 to-emerald-500'
    }
  ];

  const suggestions = [
    'Who won IPL 2024?',
    "Show me Virat Kohli's stats",
    'Which team has the best batting lineup?',
    "Predict today's match winner"
  ];

  return (
    <motion.div
      className="max-w-3xl mx-auto py-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Hero Section */}
      <motion.div
        className="text-center mb-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <div className="inline-block mb-6">
          <div className="relative">
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-2xl opacity-40"
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.4, 0.6, 0.4]
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
            <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-6 rounded-full">
              <Trophy className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>

        <h2 className="text-4xl mb-3 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
          Welcome to IPL Oracle!
        </h2>
        <p className="text-xl text-slate-300 mb-4">Your AI-Powered Cricket Intelligence</p>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Ask me anything about IPL - from match statistics to player performance, 
          team analysis to match predictions. I'm here to provide you with instant cricket insights!
        </p>
      </motion.div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-2xl p-6 hover:scale-105 hover:shadow-[0_0_20px_rgba(249,115,22,0.2)] transition-all duration-300"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
          >
            <div className={`inline-block bg-gradient-to-br ${feature.gradient} p-3 rounded-xl mb-3`}>
              <feature.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg mb-2 text-slate-100">{feature.title}</h3>
            <p className="text-sm text-slate-400">{feature.description}</p>
          </motion.div>
        ))}
      </div>

      {/* Quick Actions */}
      <motion.div
        className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-2xl p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
      >
        <h3 className="text-lg mb-4 text-slate-100">Try asking me about:</h3>
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion, index) => (
            <motion.div
              key={suggestion}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.9 + index * 0.1 }}
            >
              <Badge
                variant="outline"
                className="bg-gradient-to-r from-orange-500/10 to-purple-500/10 border-orange-500/30 text-slate-200 hover:border-orange-500/50 hover:bg-orange-500/20 transition-all duration-300 cursor-pointer px-4 py-2"
              >
                {suggestion}
              </Badge>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
