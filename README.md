# Local AI Video Generator

Fully local text-to-video and image-to-video generation with face swap, pose control, age/body sliders, and motion mimicking.

## Quick Start

```bash
# Launch ComfyUI
./scripts/launch.sh

# Open in browser
open http://127.0.0.1:8188
```

## Features

| Feature | Node/Tool | Status |
|---------|-----------|--------|
| Text-to-Video | AnimateDiff | ✅ |
| Image-to-Video | AnimateDiff | ✅ |
| Face Swap | InstantID, IPAdapterFaceID | ✅ |
| Pose Control | ControlNet + OpenPose/DWPose | ✅ |
| Age Slider | LoRA | ✅ |
| Body/Muscle Slider | LoRA | ✅ |
| Motion Mimicking | LivePortrait | ✅ |
| NSFW Mode | Realistic Vision V5.1 | ✅ |

## Workflows

Load these in ComfyUI (`Ctrl+O` or drag-drop):

- `workflows/text-to-video-basic.json` - Simple text prompt → video
- `workflows/image-to-video-basic.json` - Static image → animated video  
- `workflows/master-video-gen.json` - All features combined

## Models Installed

### Checkpoints (~6GB)
- `sd_v1-5-pruned-emaonly.safetensors` - Base SD 1.5
- `Realistic_Vision_V5.1_fp16-no-ema.safetensors` - NSFW-capable

### AnimateDiff (~2.6GB)
- `mm_sd_v15_v2.ckpt` - SD 1.5 motion module
- `mm_sdxl_v10_beta.ckpt` - SDXL motion module

### ControlNet (~2.2GB)
- `control_v11p_sd15_openpose.pth` - Pose control
- `control_v11f1p_sd15_depth.pth` - Depth control

### LoRAs (~15MB)
- `age_slider_v2.safetensors` - Age control (±0.5 range)
- `muscle_slider_v1.safetensors` - Body musculature

### Face Models (~1.1GB)
- InsightFace buffalo_l - Face detection
- inswapper_128.onnx - Face swap
- GFPGANv1.4.pth - Face restoration

## Usage Tips

### Age Slider
```
Positive weight = older appearance
Negative weight = younger appearance
Recommended range: -0.5 to 0.5
```

### Muscle Slider
```
Positive weight = more muscular
Recommended range: 0.2 to 0.6
```

### Pose Control
```
Strength 0.6-0.9 works best
Use DWPreprocessor for accurate pose extraction
```

### Face Transfer
```
IPAdapterFaceID weight: 0.7-1.0
Higher = stronger face similarity
```

## System Requirements

- macOS with Apple Silicon (M1/M2/M3)
- 16GB+ RAM (24GB recommended)
- ~50GB disk space for all models
- Python 3.11+

## Directory Structure

```
~/ComfyUI/
├── models/
│   ├── checkpoints/     # Base models
│   ├── animatediff_models/  # Motion modules
│   ├── controlnet/      # ControlNet models
│   ├── loras/          # Slider LoRAs
│   ├── insightface/    # Face detection/swap
│   └── facerestore_models/  # Face restoration
├── custom_nodes/
│   ├── ComfyUI-AnimateDiff-Evolved/
│   ├── ComfyUI_InstantID/
│   ├── ComfyUI_IPAdapter_plus/
│   ├── ComfyUI-LivePortraitKJ/
│   ├── comfyui_controlnet_aux/
│   └── ComfyUI-VideoHelperSuite/
└── output/              # Generated videos
```

## Troubleshooting

### ComfyUI won't start
```bash
# Check if port is in use
lsof -i :8188
# Kill existing process
kill $(lsof -t -i :8188)
```

### Out of memory
- Reduce resolution (512x512 recommended)
- Reduce frame count (8-16 frames)
- Use fp16 models

### Slow generation
- Normal on Apple Silicon (~1-2 min per video)
- MPS acceleration enabled by default

---

*Built: 2026-01-28*
