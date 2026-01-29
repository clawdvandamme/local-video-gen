# Features: Local AI Video Generator

## Core Features

### 1. Text-to-Video Generation

**Description:** Generate video from text prompts

**Parameters:**
- Prompt (positive)
- Negative prompt
- Number of frames (8-64)
- FPS (8-24)
- Resolution (512x512, 768x768, 1024x1024)
- Seed
- CFG Scale (1-20)
- Sampler (euler, euler_a, dpm++, etc.)
- Steps (10-50)

**Models Used:**
- Base checkpoint (SD 1.5 or SDXL)
- AnimateDiff motion module
- Optional LoRAs

---

### 2. Image-to-Video Generation

**Description:** Animate a static image

**Parameters:**
- Source image
- Motion type (zoom, pan, bounce, custom)
- Motion intensity
- Number of frames
- FPS

**Models Used:**
- AnimateDiff
- Stable Video Diffusion (SVD)
- IP-Adapter (for style preservation)

---

### 3. Face Swap

**Description:** Replace faces in video with a target face

**Parameters:**
- Target video/image
- Face source image
- Face restoration (on/off)
- Restoration strength
- Multi-face mode (swap all/select specific)
- Blend amount

**Models Used:**
- InsightFace (face detection)
- inswapper_128 (face swap)
- GFPGAN/CodeFormer (restoration)

---

### 4. Pose Control

**Description:** Control character poses using reference

**Parameters:**
- Reference pose image
- Pose type (OpenPose, DWPose, DensePose)
- Control strength (0-2)
- Start/end control percentage

**Pose Sources:**
- Upload pose image
- Select from pose library (525+ NSFW poses)
- Extract from reference video frame

---

### 5. Age Slider

**Description:** Modify apparent age of subjects

**Parameters:**
- Age offset (-1.0 to +1.0)
  - Negative = younger
  - Positive = older
- LoRA strength

**Implementation:**
- Age Slider LoRA applied during generation
- Works with both SD 1.5 and SDXL

---

### 6. Body Feature Sliders

**Description:** Adjust body proportions and features

**Sliders:**
- Breast size (-1 to +1)
- Muscle definition (-1 to +1)
- Body weight (-1 to +1)
- Height appearance (-1 to +1)
- Hip ratio (-1 to +1)

**Implementation:**
- Concept Sliders or dedicated LoRAs
- Applied during generation

---

### 7. Motion Mimicking

**Description:** Transfer motion from reference video to target image

**Parameters:**
- Reference video (motion source)
- Target image (person to animate)
- Motion smoothing
- Identity preservation strength
- Background handling (keep/replace)

**Models Used:**
- DWPose/OpenPose (pose extraction)
- MagicAnimate or LivePortrait (motion transfer)
- Appearance encoder (identity preservation)

---

### 8. NSFW Mode

**Description:** Enable adult content generation

**Features:**
- Uncensored base models
- NSFW LoRAs
- Position/pose presets
- Safety filter bypass
- Age verification prompt (first launch)

**Safeguards:**
- Local-only (no cloud)
- Clear labeling
- Default off
- Configurable restrictions

---

### 9. LoRA Support

**Description:** Apply custom style/character LoRAs

**Parameters:**
- LoRA file selection
- LoRA strength (0-2)
- Multiple LoRAs (stackable)
- Trigger words

**LoRA Types Supported:**
- Character LoRAs
- Style LoRAs
- Pose LoRAs
- Concept Sliders
- Motion LoRAs (AnimateDiff)

---

### 10. Batch Processing

**Description:** Queue multiple generations

**Features:**
- Prompt list input
- Variable seed mode
- Progress tracking
- Auto-save outputs
- Resume on crash

---

## UI Components

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│  [Text-Video] [Img-Video] [Face Swap] [Motion] [Settings]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐  ┌───────────────────────────────┐│
│  │                     │  │         Parameters            ││
│  │                     │  │  ┌─────────────────────────┐  ││
│  │    Preview Area     │  │  │ Prompt                  │  ││
│  │                     │  │  └─────────────────────────┘  ││
│  │                     │  │  Frames: [16] FPS: [12]       ││
│  │                     │  │  Steps: [20]  CFG: [7.5]      ││
│  └─────────────────────┘  │                               ││
│                           │  ─── Sliders ───              ││
│  ┌─────────────────────┐  │  Age:  [────●────] 0.0       ││
│  │    Progress Bar     │  │  Body: [────●────] 0.0       ││
│  └─────────────────────┘  │                               ││
│                           │  [x] NSFW Mode                ││
│  [Generate] [Stop] [Save] │  [ ] Face Swap                ││
│                           └───────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                      Output Gallery                         │
│  [vid1] [vid2] [vid3] [vid4] [vid5] ...                    │
└─────────────────────────────────────────────────────────────┘
```

### Settings Tab

- Model selection (checkpoints, VAE)
- Default parameters
- Output directory
- NSFW toggle with warning
- Hardware info display
- Model download manager

---

## Output Formats

### Video
- MP4 (H.264)
- WebM (VP9)
- GIF (for short clips)

### Frame Export
- PNG sequence
- JPEG sequence

### Metadata
- Generation parameters saved in video metadata
- Optional JSON sidecar file

---

## Presets

### Quick Presets
- **Cinematic:** 24fps, 48 frames, high CFG
- **Anime:** Anime model, stylized motion
- **Realistic:** Photo model, subtle motion
- **Loop:** Seamless loop settings
- **Portrait:** Face-focused, minimal motion

### NSFW Presets (when enabled)
- Various position presets
- Style presets (realistic, anime, etc.)

---

*Features defined: 2026-01-28*
