#!/bin/bash
# Verify Local Video Generator Installation

echo "🔍 Verifying Local Video Generator Setup"
echo "=========================================="

COMFYUI="$HOME/ComfyUI"
PASS=0
FAIL=0

check() {
    if [ "$1" = "true" ]; then
        echo "  ✅ $2"
        ((PASS++))
    else
        echo "  ❌ $2"
        ((FAIL++))
    fi
}

echo ""
echo "📁 Directories:"
check "$([ -d "$COMFYUI" ] && echo true)" "ComfyUI installed"
check "$([ -d "$COMFYUI/venv" ] && echo true)" "Python venv exists"
check "$([ -d "$COMFYUI/custom_nodes" ] && echo true)" "Custom nodes folder"

echo ""
echo "🎬 AnimateDiff:"
check "$([ -d "$COMFYUI/custom_nodes/ComfyUI-AnimateDiff-Evolved" ] && echo true)" "AnimateDiff-Evolved node"
check "$([ -f "$COMFYUI/models/animatediff_models/mm_sd_v15_v2.ckpt" ] && echo true)" "SD 1.5 motion module"
check "$([ -f "$COMFYUI/models/animatediff_models/mm_sdxl_v10_beta.ckpt" ] && echo true)" "SDXL motion module"

echo ""
echo "🖼️ Checkpoints:"
check "$([ -f "$COMFYUI/models/checkpoints/sd_v1-5-pruned-emaonly.safetensors" ] && echo true)" "SD 1.5 base"
check "$([ -f "$COMFYUI/models/checkpoints/Realistic_Vision_V5.1_fp16-no-ema.safetensors" ] && echo true)" "Realistic Vision V5.1"

echo ""
echo "🎭 Face Swap:"
check "$([ -d "$COMFYUI/custom_nodes/ComfyUI_InstantID" ] && echo true)" "InstantID node"
check "$([ -d "$COMFYUI/custom_nodes/ComfyUI_IPAdapter_plus" ] && echo true)" "IPAdapter node"
check "$([ -f "$COMFYUI/models/insightface/inswapper_128.onnx" ] && echo true)" "Inswapper model"
check "$([ -d "$COMFYUI/models/insightface/models" ] && echo true)" "InsightFace models"
check "$([ -f "$COMFYUI/models/facerestore_models/GFPGANv1.4.pth" ] && echo true)" "GFPGAN restoration"

echo ""
echo "🕺 Pose Control:"
check "$([ -d "$COMFYUI/custom_nodes/comfyui_controlnet_aux" ] && echo true)" "ControlNet aux node"
check "$([ -f "$COMFYUI/models/controlnet/control_v11p_sd15_openpose.pth" ] && echo true)" "OpenPose ControlNet"
check "$([ -f "$COMFYUI/models/controlnet/control_v11f1p_sd15_depth.pth" ] && echo true)" "Depth ControlNet"

echo ""
echo "🎚️ Sliders:"
check "$([ -f "$COMFYUI/models/loras/age_slider_v2.safetensors" ] && echo true)" "Age slider LoRA"
check "$([ -f "$COMFYUI/models/loras/muscle_slider_v1.safetensors" ] && echo true)" "Muscle slider LoRA"

echo ""
echo "🎥 Motion Mimicking:"
check "$([ -d "$COMFYUI/custom_nodes/ComfyUI-LivePortraitKJ" ] && echo true)" "LivePortrait node"

echo ""
echo "🎨 VAE:"
check "$([ -f "$COMFYUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors" ] && echo true)" "MSE VAE"

echo ""
echo "📊 Workflows:"
check "$([ -f "$HOME/clawd/projects/local-video-gen/workflows/text-to-video-basic.json" ] && echo true)" "Text-to-video workflow"
check "$([ -f "$HOME/clawd/projects/local-video-gen/workflows/image-to-video-basic.json" ] && echo true)" "Image-to-video workflow"
check "$([ -f "$HOME/clawd/projects/local-video-gen/workflows/master-video-gen.json" ] && echo true)" "Master workflow"

echo ""
echo "🌐 Server:"
if curl -s http://localhost:8188 > /dev/null 2>&1; then
    check "true" "ComfyUI running on port 8188"
else
    check "false" "ComfyUI running on port 8188"
fi

echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"

if [ $FAIL -eq 0 ]; then
    echo "🎉 All checks passed! Ready to generate videos."
else
    echo "⚠️  Some checks failed. See above for details."
fi
