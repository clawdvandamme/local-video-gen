# Models: Local AI Video Generator

## Required Downloads

### Base Checkpoints

| Model | Size | Use Case | Download |
|-------|------|----------|----------|
| Realistic Vision V5.1 | ~5GB | Realistic humans | [Civitai](https://civitai.com/models/4201/realistic-vision-v60-b1) |
| Pony Diffusion V6 XL | ~6GB | NSFW, high quality | [Civitai](https://civitai.com/models/257749/pony-diffusion-v6-xl) |
| AbsoluteReality | ~5GB | Photorealistic | [Civitai](https://civitai.com/models/81458/absolutereality) |
| SD 1.5 Base | ~4GB | Compatibility | [HuggingFace](https://huggingface.co/runwayml/stable-diffusion-v1-5) |

### AnimateDiff Motion Modules

| Model | Size | Version | Download |
|-------|------|---------|----------|
| mm_sd_v15_v2 | ~1.8GB | SD 1.5 | [HuggingFace](https://huggingface.co/guoyww/animatediff/tree/main) |
| mm_sdxl_v10_beta | ~1.8GB | SDXL | [HuggingFace](https://huggingface.co/guoyww/animatediff/tree/main) |
| temporaldiff-v1-animatediff | ~1.8GB | Alt module | [HuggingFace](https://huggingface.co/CiaraRowles/TemporalDiff) |

### VAE

| Model | Size | Notes | Download |
|-------|------|-------|----------|
| vae-ft-mse-840000 | ~335MB | Standard | [HuggingFace](https://huggingface.co/stabilityai/sd-vae-ft-mse) |
| sdxl_vae | ~335MB | SDXL | [HuggingFace](https://huggingface.co/stabilityai/sdxl-vae) |

### ControlNet Models

| Model | Size | Purpose | Download |
|-------|------|---------|----------|
| control_v11p_sd15_openpose | ~1.4GB | Pose control (SD1.5) | [HuggingFace](https://huggingface.co/lllyasviel/ControlNet-v1-1) |
| controlnet-openpose-sdxl | ~2.5GB | Pose control (SDXL) | [HuggingFace](https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0) |
| control_v11f1e_sd15_tile | ~1.4GB | Upscale/detail | [HuggingFace](https://huggingface.co/lllyasviel/ControlNet-v1-1) |

### Face Swap Models

| Model | Size | Purpose | Download |
|-------|------|---------|----------|
| inswapper_128.onnx | ~555MB | Face swap core | [InsightFace releases](https://github.com/deepinsight/insightface/releases) |
| buffalo_l (det/rec) | ~400MB | Face detection | Auto-download via InsightFace |
| GFPGANv1.4.pth | ~350MB | Face restoration | [GitHub](https://github.com/TencentARC/GFPGAN/releases) |
| codeformer.pth | ~375MB | Alt restoration | [GitHub](https://github.com/sczhou/CodeFormer/releases) |

### Pose Detection

| Model | Size | Purpose | Download |
|-------|------|---------|----------|
| dw-ll_ucoco_384.onnx | ~45MB | DWPose body | Auto via controlnet_aux |
| yolox_l.onnx | ~200MB | Person detection | Auto via controlnet_aux |

### Age/Body LoRAs

| Model | Size | Purpose | Download |
|-------|------|---------|----------|
| Age Slider v2.0 | ~150MB | Age control (SD1.5) | [Civitai](https://civitai.com/models/128417/age-slider) |
| Age Slider PonyXL | ~250MB | Age control (SDXL) | [Civitai](https://civitai.com/models/402667/age-slider-lora-or-ponyxl-sdxl) |
| Body Morph LoRA | ~150MB | Body features | [Civitai - search "body slider"] |

### Motion Mimicking

| Model | Size | Purpose | Download |
|-------|------|---------|----------|
| MagicAnimate | ~3GB | Motion transfer | [GitHub](https://github.com/magic-research/magic-animate) |
| LivePortrait | ~1GB | Portrait animation | [GitHub](https://github.com/KwaiVGI/LivePortrait) |

### NSFW Pose Packs

| Resource | Contents | Download |
|----------|----------|----------|
| OpenPose NSFW Pack | 525 poses | [Civitai](https://civitai.com/models/297881/openpose-nsfw-pose-package-total-525-poses) |
| Sexy Pose LoRA | Pose generation | [TensorArt](https://tensor.art/models/674867399742276499) |

---

## Directory Structure

After downloading, organize models as:

```
ComfyUI/models/
├── checkpoints/
│   ├── realisticVision_v51.safetensors
│   ├── ponyDiffusionV6XL.safetensors
│   └── absolutereality_v16.safetensors
│
├── vae/
│   ├── vae-ft-mse-840000-ema-pruned.safetensors
│   └── sdxl_vae.safetensors
│
├── loras/
│   ├── age_slider_v2.safetensors
│   ├── age_slider_ponyxl.safetensors
│   └── body_morph.safetensors
│
├── controlnet/
│   ├── control_v11p_sd15_openpose.pth
│   └── controlnet-openpose-sdxl.safetensors
│
├── animatediff_models/
│   ├── mm_sd_v15_v2.ckpt
│   └── mm_sdxl_v10_beta.safetensors
│
├── insightface/
│   ├── inswapper_128.onnx
│   └── models/
│       └── buffalo_l/
│
├── facerestore_models/
│   ├── GFPGANv1.4.pth
│   └── codeformer.pth
│
└── custom_nodes/
    └── (ComfyUI nodes auto-manage their models)
```

---

## Download Script

```python
#!/usr/bin/env python3
"""Download all required models for local-video-gen"""

import os
import requests
from pathlib import Path
from tqdm import tqdm

MODELS = {
    "checkpoints": [
        {
            "name": "realisticVision_v51.safetensors",
            "url": "https://civitai.com/api/download/models/130072",
            "size": "5GB"
        }
    ],
    "animatediff": [
        {
            "name": "mm_sd_v15_v2.ckpt",
            "url": "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt",
            "size": "1.8GB"
        }
    ],
    # ... add more
}

def download_file(url, dest):
    """Download with progress bar"""
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    
    with open(dest, 'wb') as f, tqdm(
        total=total, unit='B', unit_scale=True, desc=dest.name
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

def main():
    base = Path("models")
    for category, models in MODELS.items():
        (base / category).mkdir(parents=True, exist_ok=True)
        for model in models:
            dest = base / category / model["name"]
            if not dest.exists():
                print(f"Downloading {model['name']} ({model['size']})...")
                download_file(model["url"], dest)
            else:
                print(f"Skipping {model['name']} (exists)")

if __name__ == "__main__":
    main()
```

---

## Estimated Storage

| Category | Size |
|----------|------|
| Checkpoints (4 models) | ~20GB |
| AnimateDiff modules | ~5GB |
| ControlNet models | ~8GB |
| Face swap models | ~1.5GB |
| LoRAs | ~2GB |
| **Total Minimum** | **~35GB** |
| **With all optional** | **~60GB** |

---

## Model Compatibility Matrix

| Model Type | SD 1.5 | SDXL | Pony |
|------------|--------|------|------|
| AnimateDiff mm_v2 | ✅ | ❌ | ❌ |
| AnimateDiff SDXL | ❌ | ✅ | ✅ |
| Age Slider v2 | ✅ | ❌ | ❌ |
| Age Slider PonyXL | ❌ | ✅ | ✅ |
| ControlNet OpenPose | ✅ | ✅* | ✅* |
| FaceFusion | ✅ | ✅ | ✅ |

*SDXL requires SDXL-specific ControlNet

---

*Models list compiled: 2026-01-28*
