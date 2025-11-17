#!/bin/bash
echo "🧹 Running memory cleanup before startup..."
python -c "import gc; gc.collect(); print('✅ Python GC complete')"

echo "🚀 Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1 --limit-concurrency 50 --timeout-keep-alive 5