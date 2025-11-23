import { useState } from 'react';
import { motion } from 'motion/react';
import { Mail, Lock, Trophy, ArrowRight, AlertCircle, ArrowLeft, User } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useAuth } from '../contexts/AuthContext';
import { AnimatedBackground } from './AnimatedBackground';

interface RegisterProps {
  onSwitchToLogin: () => void;
  onBackToLanding?: () => void;
}

export function Register({ onSwitchToLogin, onBackToLanding }: RegisterProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signUp } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!email || !password || !displayName) {
      setError('Please fill in all fields');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setError('');
    setLoading(true);

    try {
      await signUp(email, password, displayName);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full text-white relative overflow-hidden">
      <AnimatedBackground />
      
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 min-h-screen flex items-center justify-center p-4"
      >
        <div className="w-full max-w-md">
          {/* Back Button */}
          {onBackToLanding && (
            <motion.button
              onClick={onBackToLanding}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="absolute top-6 left-6 flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800/40 backdrop-blur-xl border border-slate-700/30 text-slate-300 hover:text-orange-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </motion.button>
          )}

          {/* Logo Section */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{
              type: "spring",
              stiffness: 200,
              damping: 20,
              duration: 0.8,
            }}
            className="flex flex-col items-center mb-8"
          >
            {/* Trophy Icon */}
            <motion.div
              className="relative p-6 rounded-2xl bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 mb-4"
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
              <div className="relative">
                <Trophy className="w-12 h-12" />
                <div className="absolute inset-0 bg-white/5 rounded-lg" />
              </div>
            </motion.div>
            
            {/* Title */}
            <h1 className="bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent text-3xl mb-1">
              IPL Oracle
            </h1>
            <p className="text-slate-400 text-sm">Cricket Intelligence AI</p>
          </motion.div>

          {/* Register Form Card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8, ease: "easeOut" }}
            className="relative p-8 rounded-3xl bg-slate-800/60 backdrop-blur-xl border border-slate-700/30 overflow-hidden"
          >
            {/* Glass overlay gradient */}
            <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent pointer-events-none" />
            
            <div className="relative">
              <h2 className="text-white text-2xl mb-6">Create Account</h2>

              {/* Error Alert */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-3"
                >
                  <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <p className="text-red-400 text-sm">{error}</p>
                </motion.div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Display Name Input */}
                <div className="space-y-2">
                  <label htmlFor="displayName" className="text-slate-300 text-sm block">
                    Display Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="displayName"
                      type="text"
                      placeholder="Your Name"
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      disabled={loading}
                      className="w-full h-12 pl-12 pr-4 bg-slate-900/50 border-slate-700/50 rounded-xl text-white placeholder:text-slate-500 focus:border-orange-500/50 focus:ring-orange-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>

                {/* Email Input */}
                <div className="space-y-2">
                  <label htmlFor="email" className="text-slate-300 text-sm block">
                    Email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="your@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      disabled={loading}
                      className="w-full h-12 pl-12 pr-4 bg-slate-900/50 border-slate-700/50 rounded-xl text-white placeholder:text-slate-500 focus:border-orange-500/50 focus:ring-orange-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div className="space-y-2">
                  <label htmlFor="password" className="text-slate-300 text-sm block">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      disabled={loading}
                      className="w-full h-12 pl-12 pr-4 bg-slate-900/50 border-slate-700/50 rounded-xl text-white placeholder:text-slate-500 focus:border-orange-500/50 focus:ring-orange-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                  </div>
                  <p className="text-slate-500 text-xs">Must be at least 6 characters</p>
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={loading}
                  className="group w-full h-12 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:from-orange-600 hover:via-purple-700 hover:to-blue-700 text-white rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(249,115,22,0.3),0_0_40px_rgba(147,51,234,0.2)]"
                >
                  <span className="flex items-center justify-center gap-2">
                    {loading ? 'Creating Account...' : 'Create Account'}
                    {!loading && (
                      <motion.div
                        className="inline-block"
                        whileHover={{ x: 5 }}
                        transition={{ duration: 0.2 }}
                      >
                        <ArrowRight className="w-5 h-5" />
                      </motion.div>
                    )}
                  </span>
                </Button>
              </form>

              {/* Divider */}
              <div className="relative my-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-slate-700/50" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-slate-800/60 text-slate-400">
                    Already have an account?
                  </span>
                </div>
              </div>

              {/* Login Link Button */}
              <Button
                type="button"
                onClick={onSwitchToLogin}
                variant="outline"
                className="w-full h-12 border-slate-700/50 hover:border-orange-500/50 text-slate-300 hover:text-orange-400 hover:bg-slate-900/30 rounded-xl transition-all"
              >
                Sign In Instead
              </Button>
            </div>
          </motion.div>

          {/* Footer */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-center text-slate-500 text-sm mt-6"
          >
            Secure authentication powered by Firebase
          </motion.p>
        </div>
      </motion.div>
    </div>
  );
}
