import { motion } from 'motion/react';
import { Trophy, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Avatar, AvatarFallback } from './ui/avatar';

export function ChatHeader() {
  const { currentUser, signout } = useAuth();

  const getInitials = (name: string | null) => {
    if (!name) return 'U';
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <motion.header
      className="sticky top-0 z-50 h-20 bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/50 shadow-lg"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="h-full max-w-7xl mx-auto px-4 flex items-center justify-between">
        {/* Left Section - Logo */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-lg opacity-50"
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
            <div className="relative bg-gradient-to-br from-orange-500 via-purple-600 to-blue-600 p-3 rounded-full">
              <Trophy className="w-6 h-6 text-white" />
            </div>
          </div>
          <div className="hidden sm:block">
            <h1 className="bg-gradient-to-r from-orange-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
              IPL Oracle
            </h1>
            <p className="text-sm text-slate-400">Cricket Intelligence AI</p>
          </div>
        </div>

        {/* Right Section - User Info */}
        <div className="flex items-center gap-4">
          <div className="hidden md:block text-right">
            <p className="text-slate-100">{currentUser?.displayName || 'User'}</p>
            <p className="text-sm text-slate-400">{currentUser?.email}</p>
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 rounded-full blur-sm opacity-50"></div>
            <Avatar className="relative border-2 border-transparent bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 p-[2px]">
              <AvatarFallback className="bg-slate-800 text-white">
                {getInitials(currentUser?.displayName || null)}
              </AvatarFallback>
            </Avatar>
          </div>

          <button
            onClick={signout}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800/60 border border-slate-700/30 text-slate-300 hover:text-red-400 hover:border-red-500/30 transition-all duration-300"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </motion.header>
  );
}
