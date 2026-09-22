#!/bin/bash
# OpenClaw Transcription System Launcher
# Starts OpenClaw with optimized performance settings

set -e

echo "🚀 OpenClaw Transcription System"
echo "=================================="
echo ""

# Check if OpenClaw script exists
if [ ! -f "openclaw.py" ]; then
    echo "✗ openclaw.py not found. Please ensure you're in the project directory."
    exit 1
fi

# Setup performance environment
echo "⚙️  Setting up performance environment..."
export OMP_NUM_THREADS=16
export NUMEXPR_NUM_THREADS=16
export MKL_NUM_THREADS=16
export CUDA_VISIBLE_DEVICES=0
export CUDA_LAUNCH_BLOCKING=0
export MAX_MEMORY=8GB
export CACHE_SIZE=4GB

echo "✓ Environment configured"
echo ""

# Display available commands
echo "📋 Available Commands:"
echo "  python openclaw.py transcribe <audio_file>  - Transcribe single file"
echo "  python openclaw.py batch <files...>         - Transcribe multiple files"
echo "  python openclaw.py status                   - Show system status"
echo ""

# Check if Ollama is available
echo "🔍 Checking dependencies..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found"

    # List available models
    echo ""
    echo "📦 Available Ollama models:"
    ollama list 2>/dev/null || echo "  (No models installed yet)"

    echo ""
    echo "💡 To use OpenClaw with Ollama models:"
    echo "  1. Pull a model: ollama pull gemma:2b"
    echo "  2. Start Ollama: ollama serve"
    echo "  3. In another terminal, run OpenClaw"
else
    echo "⚠️  Ollama not found. Install from: https://ollama.ai"
fi

echo ""

# If arguments provided, run OpenClaw with those arguments
if [ $# -gt 0 ]; then
    echo "▶️  Running: python openclaw.py $@"
    echo ""
    python openclaw.py "$@"
else
    echo "▶️  Starting interactive mode..."
    echo "    Run: python openclaw.py --help for more information"
    echo ""
    python openclaw.py status
fi
