#!/bin/bash
# Cleanup script for OpenClaw popup windows and artifacts
# Usage: ./cleanup_popups.sh

echo "🧹 Cleaning up OpenClaw artifacts..."
echo ""

# Kill any lingering OpenClaw processes
echo "1. Terminating OpenClaw processes..."
pkill -f openclaw 2>/dev/null && echo "   ✓ Killed OpenClaw processes" || echo "   ✓ No processes to kill"
pkill -f "\.exe" 2>/dev/null && echo "   ✓ Cleaned up executables" || true
echo ""

# Remove temporary files
echo "2. Removing temporary files..."
rm -rf /tmp/*openclaw* 2>/dev/null && echo "   ✓ Cleaned /tmp" || true
rm -rf ~/.openclaw/temp* 2>/dev/null && echo "   ✓ Cleaned ~/.openclaw/temp" || true
echo ""

# Clear cache if needed (preserves logs for debugging)
echo "3. Optional cache cleanup..."
echo "   Run: rm -rf ~/.openclaw/cache"
echo "   (Keeps logs for debugging)"
echo ""

# Verify cleanup
echo "4. Verification:"
if ! pgrep -f openclaw > /dev/null; then
    echo "   ✓ All OpenClaw processes terminated"
else
    echo "   ⚠️  Some OpenClaw processes still running"
    pgrep -f openclaw
fi

echo ""
echo "✓ Cleanup complete!"
