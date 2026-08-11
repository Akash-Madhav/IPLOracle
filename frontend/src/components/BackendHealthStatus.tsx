import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Activity, RefreshCw } from 'lucide-react';
import { checkBackendHealth } from '../lib/api';

const PING_INTERVAL_SECONDS = 300; // Ping every 300 seconds (5 minutes)

export function BackendHealthStatus() {
  const [status, setStatus] = useState<'checking' | 'active' | 'degraded' | 'offline'>('checking');
  const [lastPingTime, setLastPingTime] = useState<Date | null>(null);
  const [pingCount, setPingCount] = useState<number>(0);
  const [isPinging, setIsPinging] = useState(false);
  const [secondsUntilNextPing, setSecondsUntilNextPing] = useState<number>(PING_INTERVAL_SECONDS);
  const [showTooltip, setShowTooltip] = useState(false);

  const performHealthCheck = useCallback(async () => {
    setIsPinging(true);
    console.log(`🔍 [Keep-Alive] Sending health check request to backend...`);
    try {
      const result = await checkBackendHealth();
      if (result.ok) {
        setStatus('active');
        setLastPingTime(new Date());
        setPingCount((prev) => prev + 1);
        console.log(`✅ [Keep-Alive] Backend health check OK (Status: ${result.status})`);
      } else {
        setStatus('degraded');
        console.warn(`⚠️ [Keep-Alive] Backend health check returned non-OK status`);
      }
    } catch (err) {
      setStatus('offline');
      console.error(`❌ [Keep-Alive] Backend health check failed:`, err);
    } finally {
      setIsPinging(false);
    }
  }, []);

  // Perform initial ping on mount
  useEffect(() => {
    performHealthCheck();
  }, [performHealthCheck]);

  // Per-second countdown timer
  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsUntilNextPing((prev) => {
        if (prev <= 1) {
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Watch countdown state and handle ping triggers cleanly
  useEffect(() => {
    if (secondsUntilNextPing === 0) {
      console.log(`🚀 [Keep-Alive Ticker] ${PING_INTERVAL_SECONDS}s (5m) completed! Triggering backend /health check now...`);
      performHealthCheck();
      setSecondsUntilNextPing(PING_INTERVAL_SECONDS);
    } else {
      console.log(`⏱️ [Keep-Alive Ticker] Next ping in ${secondsUntilNextPing}s`);
    }
  }, [secondsUntilNextPing, performHealthCheck]);

  const handleManualPing = () => {
    if (!isPinging) {
      console.log(`👆 [Keep-Alive] Manual ping triggered by user click`);
      setSecondsUntilNextPing(PING_INTERVAL_SECONDS);
      performHealthCheck();
    }
  };

  return (
    <div className="relative inline-block">
      <motion.div
        whileHover={{ scale: 1.02 }}
        onClick={handleManualPing}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        className="flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-slate-900/90 border border-emerald-500/40 hover:border-emerald-500/70 backdrop-blur-md cursor-pointer transition-all shadow-md group"
      >
        {/* Animated Pulsing Status Dot */}
        <div className="relative flex items-center justify-center">
          {status === 'active' && (
            <>
              <span className="absolute inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400 opacity-75 animate-ping" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            </>
          )}
          {status === 'checking' && (
            <RefreshCw className="w-3 h-3 text-amber-400 animate-spin" />
          )}
          {status === 'degraded' && (
            <span className="relative inline-flex h-2 w-2 rounded-full bg-amber-400" />
          )}
          {status === 'offline' && (
            <span className="relative inline-flex h-2 w-2 rounded-full bg-rose-500" />
          )}
        </div>

        {/* Status Text & Live Countdown Badge */}
        <div className="flex items-center gap-1.5 text-xs">
          <span className="font-semibold text-emerald-400 group-hover:text-emerald-300 transition-colors">
            {status === 'active' ? 'Backend Active' : status === 'checking' ? 'Pinging...' : 'Backend Status'}
          </span>
          <span className="text-[10px] text-slate-400 border-l border-slate-700 pl-1.5 hidden md:inline font-mono">
            {isPinging ? 'Pinging...' : `Next in ${secondsUntilNextPing}s`}
          </span>
        </div>

        {/* Refresh Icon */}
        <RefreshCw
          className={`w-3 h-3 text-slate-400 group-hover:text-emerald-400 transition-colors ${
            isPinging ? 'animate-spin text-emerald-400' : ''
          }`}
        />
      </motion.div>

      {/* Interactive Hover Tooltip */}
      <AnimatePresence>
        {showTooltip && (
          <motion.div
            initial={{ opacity: 0, y: 5, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 5, scale: 0.95 }}
            className="absolute right-0 top-full mt-2 w-72 p-3.5 rounded-xl bg-slate-950/95 border border-emerald-500/40 backdrop-blur-xl shadow-2xl z-50 text-xs text-slate-300 pointer-events-none"
          >
            <div className="flex items-center justify-between mb-2 font-semibold text-emerald-400">
              <div className="flex items-center gap-1.5">
                <Activity className="w-4 h-4" />
                Backend Keep-Alive Service
              </div>
              <span className="px-1.5 py-0.5 rounded bg-emerald-500/20 text-[10px] text-emerald-300 font-mono">
                {secondsUntilNextPing}s
              </span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed mb-2.5">
              Continuously pings <code className="text-emerald-300 font-mono text-[10px]">/health</code> every 5 minutes (300s) to keep the backend warm and prevent Render sleep.
            </p>
            <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-800/80">
              <span>Total Pings: <strong className="text-emerald-300 font-semibold">{pingCount}</strong></span>
              <span>
                {lastPingTime ? `Last: ${lastPingTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}` : 'Pinging...'}
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
