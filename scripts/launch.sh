#!/bin/bash
# Local Video Generator Launcher
# Starts ComfyUI with optimal settings for Apple Silicon

COMFYUI_DIR="$HOME/ComfyUI"
PORT="${1:-8188}"
LOG_FILE="/tmp/comfyui-videogen.log"

echo "🎬 Local Video Generator"
echo "========================"

# Check if ComfyUI is already running
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "✅ ComfyUI already running on port $PORT"
    echo "   Open: http://127.0.0.1:$PORT"
    exit 0
fi

# Activate venv and start
cd "$COMFYUI_DIR" || exit 1
source venv/bin/activate

echo "🚀 Starting ComfyUI on port $PORT..."
echo "   Log: $LOG_FILE"

# Start with MPS-optimized settings
nohup python main.py \
    --port $PORT \
    --force-fp16 \
    --preview-method auto \
    > "$LOG_FILE" 2>&1 &

# Wait for startup
echo "⏳ Waiting for server..."
for i in {1..30}; do
    if curl -s "http://127.0.0.1:$PORT" > /dev/null 2>&1; then
        echo "✅ ComfyUI ready!"
        echo ""
        echo "📍 Open: http://127.0.0.1:$PORT"
        echo ""
        echo "📂 Workflows available:"
        ls -1 "$HOME/clawd/projects/local-video-gen/workflows/"*.json 2>/dev/null | while read f; do
            echo "   - $(basename "$f")"
        done
        echo ""
        echo "🎛️  Models loaded:"
        echo "   Checkpoints: $(ls -1 "$COMFYUI_DIR/models/checkpoints/"*.safetensors 2>/dev/null | wc -l | tr -d ' ')"
        echo "   LoRAs: $(ls -1 "$COMFYUI_DIR/models/loras/"*.safetensors 2>/dev/null | wc -l | tr -d ' ')"
        echo "   ControlNets: $(ls -1 "$COMFYUI_DIR/models/controlnet/"*.pth 2>/dev/null | wc -l | tr -d ' ')"
        exit 0
    fi
    sleep 1
done

echo "❌ Timeout waiting for ComfyUI to start"
echo "   Check log: $LOG_FILE"
exit 1
