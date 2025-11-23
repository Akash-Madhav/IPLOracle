import { Component, ReactNode } from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-4">
          <div className="max-w-md w-full">
            <div className="p-8 rounded-2xl bg-gradient-to-br from-slate-800/50 via-slate-800/30 to-slate-900/50 backdrop-blur-xl border border-red-500/30 text-center">
              {/* Error Icon */}
              <div className="w-16 h-16 rounded-full bg-red-500/20 border border-red-500/30 flex items-center justify-center mx-auto mb-6">
                <AlertCircle className="w-8 h-8 text-red-400" />
              </div>

              {/* Error Message */}
              <h2 className="text-2xl mb-3 bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
                Something went wrong
              </h2>
              <p className="text-slate-400 mb-6">
                {this.state.error?.message || 'An unexpected error occurred'}
              </p>

              {/* Reset Button */}
              <button
                onClick={this.handleReset}
                className="px-6 py-3 rounded-lg bg-gradient-to-r from-orange-500 via-purple-600 to-blue-600 hover:from-orange-600 hover:via-purple-700 hover:to-blue-700 transition-all flex items-center gap-2 mx-auto"
              >
                <RefreshCw className="w-4 h-4" />
                Reload Application
              </button>

              {/* Technical Details */}
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="mt-6 text-left">
                  <summary className="text-sm text-slate-500 cursor-pointer hover:text-slate-400">
                    Technical Details
                  </summary>
                  <pre className="mt-3 p-3 rounded bg-slate-950/50 text-xs text-red-400 overflow-auto">
                    {this.state.error.stack}
                  </pre>
                </details>
              )}
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
