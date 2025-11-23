import { motion, AnimatePresence } from 'motion/react';
import { Info, X } from 'lucide-react';
import { useState } from 'react';

export function IPLDisclaimer() {
  const [isVisible, setIsVisible] = useState(true);

  if (!isVisible) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="mx-4 mb-4"
      >
        <div className="max-w-4xl mx-auto">
          <div className="p-4 rounded-xl bg-gradient-to-br from-blue-900/30 via-blue-800/20 to-blue-900/30 backdrop-blur-xl border border-blue-500/30">
            <div className="flex items-start gap-3">
              {/* Icon */}
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                <Info className="w-4 h-4 text-blue-400" />
              </div>

              {/* Content */}
              <div className="flex-1">
                <h3 className="text-sm text-blue-300 mb-1">About IPL Oracle</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  IPL Oracle uses AI-powered semantic search to answer your cricket questions. 
                  Responses are generated based on available data and may occasionally contain 
                  inaccuracies. For official statistics, please refer to IPL's official sources.
                </p>
              </div>

              {/* Close Button */}
              <button
                onClick={() => setIsVisible(false)}
                className="flex-shrink-0 w-6 h-6 rounded-lg hover:bg-blue-500/20 flex items-center justify-center transition-colors group"
              >
                <X className="w-4 h-4 text-slate-500 group-hover:text-blue-400 transition-colors" />
              </button>
            </div>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
