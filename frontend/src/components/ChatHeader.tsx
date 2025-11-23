import { LogOut, Trophy } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'motion/react';

export function ChatHeader() {
  const { user, signOut } = useAuth();

  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/80 backdrop-blur-xl"
    >
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <Trophy className="w-8 h-8 text-orange-400" />
            <div className="absolute inset-0 blur-xl bg-orange-400/30"></div>
          </div>
          <div>
            <h1 className="text-xl bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
              IPL Oracle
            </h1>
            <p className="text-xs text-slate-500">AI Cricket Intelligence</p>
          </div>
        </div>

        {/* User Info and Sign Out */}
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-sm text-slate-300">{user?.displayName || 'User'}</p>
            <p className="text-xs text-slate-500">{user?.email}</p>
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={signOut}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-orange-500/10 via-purple-500/10 to-blue-500/10 border border-orange-500/20 hover:border-orange-500/40 transition-all group"
          >
            <div className="flex items-center gap-2">
              <LogOut className="w-4 h-4 text-orange-400 group-hover:text-orange-300 transition-colors" />
              <span className="text-sm text-slate-300 hidden sm:inline">Sign Out</span>
            </div>
          </motion.button>
        </div>
      </div>
    </motion.header>
  );
}
