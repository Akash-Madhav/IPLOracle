import { useState } from 'react';
import { motion } from 'motion/react';
import { Trophy, Mail, Lock, ArrowRight, ArrowLeft, AlertCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { AnimatedBackground } from './AnimatedBackground';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Alert, AlertDescription } from './ui/alert';

interface LoginProps {
  onSwitchToRegister: () => void;
  onBackToLanding?: () => void;
}

export function Login({ onSwitchToRegister, onBackToLanding }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    setError('');
    setLoading(true);

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
      <AnimatedBackground />

      {/* Back Button */}
      {onBackToLanding && (
        <motion.button
          onClick={onBackToLanding}
          className="absolute top-6 left-6 flex items-center gap-2 backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-xl px-4 py-2 text-slate-300 hover:text-white hover:border-orange-500/50 transition-all duration-300"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </motion.button>
      )}

      <div className="relative z-10 w-full max-w-md">
        {/* Logo Section */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, scale: 0.9, rotate: -10 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-block mb-4">
            <div className="relative">
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-xl opacity-50"
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
              <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-5 rounded-full">
                <Trophy className="w-12 h-12 text-white" />
              </div>
            </div>
          </div>
          <h1 className="text-4xl mb-2 bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
            IPL Oracle
          </h1>
          <p className="text-slate-400">Cricket Intelligence AI</p>
        </motion.div>

        {/* Login Form */}
        <motion.div
          className="backdrop-blur-xl bg-slate-800/60 border border-slate-700/30 rounded-3xl p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2 className="text-2xl mb-6 text-center text-slate-100">Welcome Back</h2>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Alert className="mb-6 bg-red-500/10 border-red-500/30 text-red-400">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="email" className="text-slate-300 mb-2 block">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  className="pl-11 bg-slate-900/50 border-slate-700/50 focus:border-orange-500/50 rounded-xl text-white"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="password" className="text-slate-300 mb-2 block">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  className="pl-11 bg-slate-900/50 border-slate-700/50 focus:border-orange-500/50 rounded-xl text-white"
                />
              </div>
            </div>

            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:shadow-[0_0_30px_rgba(249,115,22,0.4),0_0_60px_rgba(147,51,234,0.3)] transition-all duration-300 py-6 group"
            >
              {loading ? 'Signing in...' : 'Sign In'}
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-700/50"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-slate-800/60 text-slate-400">New to IPL Oracle?</span>
            </div>
          </div>

          <Button
            onClick={onSwitchToRegister}
            variant="outline"
            className="w-full border-slate-700/50 hover:border-orange-500/50 bg-transparent transition-all duration-300"
          >
            Create an Account
          </Button>
        </motion.div>

        <motion.p
          className="text-center text-slate-500 text-sm mt-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          Secure authentication powered by Firebase
        </motion.p>
      </div>
    </div>
  );
}
