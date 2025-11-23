import { motion } from 'motion/react';
import { Sparkles, Zap, Shield, TrendingUp } from 'lucide-react';

interface WelcomeScreenProps {
  onGetStarted: () => void;
}

export function WelcomeScreen({ onGetStarted }: WelcomeScreenProps) {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Insights',
      description: 'Get intelligent answers about IPL stats, players, and matches',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Instant responses powered by advanced semantic search',
    },
    {
      icon: Shield,
      title: 'Stat-Agnostic',
      description: 'Ask anything - runs, wickets, venues, or any IPL data',
    },
    {
      icon: TrendingUp,
      title: 'Contextual Answers',
      description: 'Comprehensive responses with sources and context',
    },
  ];

  const exampleQuestions = [
    "Who has the most runs in IPL history?",
    "Which team won the most IPL titles?",
    "Tell me about Virat Kohli's IPL performance",
    "What's the highest team score in an IPL match?",
  ];

  return (
    <div className="flex-1 flex items-center justify-center p-4 overflow-y-auto">
      <div className="max-w-4xl w-full">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          {/* Hero Section */}
          <div className="relative inline-block mb-6">
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
                rotate: [0, 5, -5, 0],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                repeatType: 'reverse',
              }}
              className="absolute inset-0 blur-3xl bg-gradient-to-r from-orange-500/30 via-purple-500/30 to-blue-500/30"
            />
            <h1 className="relative text-5xl md:text-6xl mb-4 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
              Welcome to IPL Oracle
            </h1>
          </div>
          
          <p className="text-xl text-slate-300 mb-2">
            Your AI-Powered Cricket Intelligence Assistant
          </p>
          <p className="text-slate-500">
            Ask me anything about IPL - stats, players, teams, matches, and more!
          </p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
              className="p-6 rounded-2xl bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 backdrop-blur-xl border border-white/10 hover:border-orange-500/30 transition-all group"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br from-orange-500/20 via-purple-500/20 to-blue-500/20 border border-orange-500/30 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <feature.icon className="w-6 h-6 text-orange-400" />
                </div>
                <div className="flex-1">
                  <h3 className="text-slate-100 mb-1">{feature.title}</h3>
                  <p className="text-sm text-slate-400">{feature.description}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Example Questions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mb-12"
        >
          <h2 className="text-center text-slate-300 mb-4">Try asking:</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {exampleQuestions.map((question, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02, x: 5 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onGetStarted()}
                className="p-4 rounded-xl bg-gradient-to-br from-slate-800/30 to-slate-900/30 border border-white/10 hover:border-orange-500/30 text-left transition-all group"
              >
                <p className="text-sm text-slate-300 group-hover:text-orange-300 transition-colors">
                  "{question}"
                </p>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* CTA Button */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="text-center"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onGetStarted}
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:from-orange-600 hover:via-purple-700 hover:to-blue-700 transition-all shadow-lg shadow-orange-500/20 group"
          >
            <span className="text-lg text-white group-hover:scale-110 inline-block transition-transform">
              Start Chatting Now
            </span>
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
}
