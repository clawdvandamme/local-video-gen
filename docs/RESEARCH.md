# Research: Local AI Video Generation Tools

## Video Generation Models

### AnimateDiff
- **Type:** Motion module for Stable Diffusion
- **Source:** https://github.com/guoyww/AnimateDiff
- **ComfyUI:** https://github.com/SipherAGI/comfyui-animatediff
- **VRAM:** 8-12GB minimum
- **Features:** Text-to-video, image-to-video, motion LoRAs
- **Models:**
  - mm_sd_v15_v2.ckpt (SD 1.5)
  - mm_sdxl_v10_beta.safetensors (SDXL)
  - Various motion LoRAs for specific movements

### Stable Video Diffusion (SVD)
- **Type:** Image-to-video
- **Source:** Stability AI
- **VRAM:** 16GB+ recommended
- **Features:** High quality image animation
- **Models:**
  - svd_xt_1_1.safetensors

### Mochi
- **Type:** Text-to-video
- **Source:** Genmo
- **ComfyUI:** Native support
- **Features:** High quality motion, good prompt adherence

### Wan 2.x / HunyuanVideo
- **Type:** Text-to-video
- **Features:** Large scale, high quality
- **VRAM:** High requirements (24GB+)

---

## Face Swap Tools

### FaceFusion
- **Source:** https://facefusion.io / https://github.com/facefusion/facefusion
- **Type:** Standalone + ComfyUI node
- **Features:**
  - Face swap in images/videos
  - Face enhancer
  - Expression restoration
  - Multi-face support
- **Models:**
  - inswapper_128.onnx
  - GFPGANv1.4.pth (face restoration)
  - CodeFormer (alternative restoration)

### Roop-Unleashed
- **Source:** https://github.com/C0untFloyd/roop-unleashed
- **Features:**
  - Face swap
  - Live streaming support
  - Batch processing
  - VR face replacement
- **Evolved fork with more features**

### ReActor (ComfyUI)
- **Source:** ComfyUI node
- **Features:** Direct integration with ComfyUI workflows

---

## Pose & Body Control

### ControlNet
- **Source:** https://github.com/lllyasviel/ControlNet
- **ComfyUI:** Native support
- **Preprocessors:**
  - OpenPose (body + hands + face)
  - DWPose (improved pose detection)
  - DensePose (body surface mapping)
  - Canny (edge detection)
  - Depth (depth maps)

### OpenPose Models
- **Source:** CMU Perceptual Computing Lab
- **Detects:** Body keypoints, hand keypoints, facial keypoints

### NSFW Pose Packs
- **Source:** Civitai
- **civitai.com/models/297881** - 525 NSFW poses
- Various position/pose LoRAs

---

## Age & Body Sliders

### Concept Sliders
- **Source:** https://github.com/rohitgandikota/sliders
- **Paper:** "Concept Sliders for Precise Control of Diffusion Models"
- **Features:** Continuous control over concepts

### Age Slider LoRAs
- **civitai.com/models/128417** - Age Slider v2.0 (SD 1.5)
- **civitai.com/models/402667** - Age Slider (Pony/SDXL)
- **Usage:** Positive weight = older, negative = younger

### Body Feature LoRAs
- Various on Civitai for body proportions
- Breast size, muscle definition, etc.

---

## Motion Mimicking

### MagicAnimate
- **Source:** https://github.com/magic-research/magic-animate
- **Paper:** "MagicAnimate: Temporally Consistent Human Image Animation"
- **Features:**
  - Reference image + motion sequence → animated video
  - Temporal consistency
  - Identity preservation
  - Cross-ID animations

### LivePortrait
- **Source:** https://github.com/KwaiVGI/LivePortrait
- **Features:**
  - Portrait animation
  - Stitching and retargeting control
  - Efficient inference

### MimicMotion
- **Source:** https://github.com/Tencent/MimicMotion
- **Features:**
  - High-quality human motion video
  - Confidence-aware pose guidance
  - Arbitrary length generation

### AnimateAnyone
- **Features:**
  - Pose-guided video generation
  - Identity preservation
  - Temporal consistency

---

## Base Models (NSFW-capable)

### Pony Diffusion
- **Source:** Civitai
- **Features:** NSFW-capable, high quality
- **Versions:** V6, XL variants

### Realistic Vision
- **Source:** Civitai
- **Features:** Photorealistic, NSFW versions available

### AbsoluteReality
- **Source:** Civitai
- **Features:** Highly realistic outputs

### Various Hentai/Anime Models
- AOM3 (Anything v3)
- Counterfeit
- Various merged models

---

## VRAM Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| AnimateDiff (SD 1.5) | 8GB | 12GB |
| AnimateDiff (SDXL) | 12GB | 16GB |
| FaceFusion | 4GB | 8GB |
| ControlNet | 8GB | 12GB |
| SVD | 12GB | 16GB+ |
| Full Pipeline | 12GB | 24GB |

---

## ComfyUI Custom Nodes Needed

1. **ComfyUI-AnimateDiff-Evolved** - AnimateDiff integration
2. **ComfyUI-VideoHelperSuite** - Video loading/saving
3. **ComfyUI_IPAdapter_plus** - Image prompt adapter
4. **comfyui_controlnet_aux** - ControlNet preprocessors
5. **ComfyUI-Impact-Pack** - Face detection, segmentation
6. **ReActor** or **FaceFusion node** - Face swap
7. **ComfyUI-Manager** - Easy node installation

---

## Download Sources

- **HuggingFace:** https://huggingface.co
- **Civitai:** https://civitai.com
- **GitHub Releases:** Various repos
- **ComfyUI Manager:** Auto-download many models

---

*Research compiled: 2026-01-28*
