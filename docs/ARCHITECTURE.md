# Architecture: Local AI Video Generator

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Web UI (Gradio)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │Text-Video│ │Img-Video │ │Face Swap │ │Motion    │           │
│  │   Tab    │ │   Tab    │ │   Tab    │ │Mimic Tab │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
└───────┼────────────┼────────────┼────────────┼──────────────────┘
        │            │            │            │
        v            v            v            v
┌─────────────────────────────────────────────────────────────────┐
│                    Pipeline Orchestrator                        │
│  • Workflow selection    • Parameter validation                 │
│  • Queue management      • Progress tracking                    │
└─────────────────────────────────────────────────────────────────┘
        │
        v
┌─────────────────────────────────────────────────────────────────┐
│                     ComfyUI Backend                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Workflow Engine                          ││
│  │  • Load workflow JSON    • Execute nodes                    ││
│  │  • Handle callbacks      • Return outputs                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                  │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┐ │
│  │AnimateDiff│ControlNet │ FaceFusion│  Sliders  │  Motion   │ │
│  │  Nodes    │  Nodes    │   Nodes   │  LoRAs    │  Extract  │ │
│  └───────────┴───────────┴───────────┴───────────┴───────────┘ │
└─────────────────────────────────────────────────────────────────┘
        │
        v
┌─────────────────────────────────────────────────────────────────┐
│                      Model Storage                              │
│  /models/                                                       │
│  ├── checkpoints/     # Base SD models                         │
│  ├── loras/           # LoRA weights                           │
│  ├── controlnet/      # ControlNet models                      │
│  ├── animatediff/     # Motion modules                         │
│  ├── faceswap/        # InsightFace, GFPGAN                    │
│  └── motion/          # MagicAnimate, LivePortrait             │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Web UI (Gradio)

**Purpose:** User-friendly interface for all features

**Tabs:**
- **Text-to-Video:** Prompt → video generation
- **Image-to-Video:** Source image → animated video
- **Face Swap:** Target video + face source → swapped video
- **Motion Mimic:** Reference video + target image → motion transfer
- **Settings:** Model selection, NSFW toggle, output settings

**Features:**
- Live preview
- Progress bar
- Gallery of outputs
- Preset management
- Batch queue

### 2. Pipeline Orchestrator

**Purpose:** Manage workflow execution and parameters

**Responsibilities:**
- Select appropriate ComfyUI workflow
- Validate inputs
- Apply sliders (age, body features)
- Queue multiple jobs
- Track progress
- Handle errors

### 3. ComfyUI Backend

**Purpose:** Execute AI workflows

**Integration:**
- Run ComfyUI in API mode
- Load workflow JSONs programmatically
- Execute via WebSocket
- Stream progress updates
- Retrieve outputs

### 4. Workflow Library

Pre-built workflows for each use case:

```
/workflows/
├── text_to_video_basic.json
├── text_to_video_nsfw.json
├── image_to_video_animatediff.json
├── image_to_video_svd.json
├── face_swap_basic.json
├── face_swap_video.json
├── pose_guided_generation.json
├── motion_transfer_magicanimate.json
└── combined_pipeline.json
```

## Data Flow

### Text-to-Video Pipeline

```
User Input (prompt, settings)
    │
    v
┌─────────────────┐
│ Load Checkpoint │ (NSFW model if enabled)
└────────┬────────┘
         v
┌─────────────────┐
│ CLIP Encode     │ (prompt → embeddings)
└────────┬────────┘
         v
┌─────────────────┐
│ Load LoRAs      │ (age, body sliders)
└────────┬────────┘
         v
┌─────────────────┐
│ AnimateDiff     │ (add motion)
│ Motion Module   │
└────────┬────────┘
         v
┌─────────────────┐
│ KSampler        │ (denoise)
└────────┬────────┘
         v
┌─────────────────┐
│ VAE Decode      │ (latents → frames)
└────────┬────────┘
         v
┌─────────────────┐
│ Video Combine   │ (frames → video)
└────────┬────────┘
         v
Output Video (MP4)
```

### Face Swap Pipeline

```
Input Video + Face Source Image
    │
    v
┌─────────────────┐
│ Extract Frames  │
└────────┬────────┘
         v
┌─────────────────┐
│ Face Detection  │ (InsightFace)
└────────┬────────┘
         v
┌─────────────────┐
│ Face Swap       │ (inswapper_128)
└────────┬────────┘
         v
┌─────────────────┐
│ Face Enhance    │ (GFPGAN/CodeFormer)
└────────┬────────┘
         v
┌─────────────────┐
│ Combine Frames  │
└────────┬────────┘
         v
Output Video
```

### Motion Mimicking Pipeline

```
Reference Video + Target Image
    │
    v
┌─────────────────┐
│ Pose Extraction │ (DWPose/OpenPose)
└────────┬────────┘
         v
┌─────────────────┐
│ Motion Sequence │ (pose keyframes)
└────────┬────────┘
         v
┌─────────────────┐
│ MagicAnimate/   │
│ LivePortrait    │
└────────┬────────┘
         v
┌─────────────────┐
│ Identity        │ (preserve target face)
│ Preservation    │
└────────┬────────┘
         v
Output Video
```

## Configuration

### config.yaml

```yaml
# General
output_dir: "./outputs"
temp_dir: "./temp"
log_level: "INFO"

# Models
default_checkpoint: "realisticVision_v51.safetensors"
nsfw_checkpoint: "ponyDiffusionV6XL.safetensors"
vae: "vae-ft-mse-840000-ema-pruned.safetensors"

# Video Settings
default_fps: 12
default_frames: 16
max_frames: 64
video_format: "mp4"
video_codec: "libx264"

# Generation
default_steps: 20
default_cfg: 7.5
default_sampler: "euler_ancestral"

# Face Swap
face_enhancer: "gfpgan"
face_swap_model: "inswapper_128"

# NSFW Mode
nsfw_enabled: false
nsfw_safety_filter: false

# Sliders
age_slider_default: 0.0
age_slider_range: [-1.0, 1.0]
body_slider_default: 0.0
body_slider_range: [-1.0, 1.0]
```

## Directory Structure

```
local-video-gen/
├── main.py                 # Entry point
├── config.yaml             # Configuration
├── requirements.txt        # Python dependencies
│
├── app/
│   ├── __init__.py
│   ├── ui.py              # Gradio interface
│   ├── orchestrator.py    # Pipeline management
│   └── comfyui_api.py     # ComfyUI integration
│
├── workflows/             # ComfyUI workflow JSONs
│   └── *.json
│
├── models/                # Model storage (symlink to ComfyUI)
│   ├── checkpoints/
│   ├── loras/
│   ├── controlnet/
│   └── ...
│
├── outputs/               # Generated videos
│
├── docs/                  # Documentation
│   ├── RESEARCH.md
│   ├── ARCHITECTURE.md
│   ├── FEATURES.md
│   └── MODELS.md
│
└── scripts/               # Utility scripts
    ├── download_models.py
    └── setup_comfyui.py
```

## API Design

### REST Endpoints (optional)

```
POST /api/generate/text-to-video
POST /api/generate/image-to-video
POST /api/generate/face-swap
POST /api/generate/motion-mimic
GET  /api/status/{job_id}
GET  /api/outputs
```

### WebSocket (for progress)

```
WS /ws/progress
  → {"job_id": "...", "progress": 45, "stage": "sampling"}
```

---

*Architecture designed: 2026-01-28*
