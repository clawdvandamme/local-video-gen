# Wan 2.2 - Best-in-Class Video Gen for Mac MPS (2025)

## Research Summary

After researching current state-of-the-art for local video generation on Mac Apple Silicon:

### Why Wan 2.2?
- **MoE Architecture** - Mixture of Experts with high-noise and low-noise models
- **Film-quality output** - Professional lens language, lighting, color, composition
- **Large-scale complex motion** - Smooth, natural movement
- **Apache 2.0 license** - Commercial use allowed
- **Mac compatible** - Works on MPS with GGUF quantized models

### For Mac: GGUF Quantized Models Required

Standard diffusion models don't work well on MPS. Must use:
1. **ComfyUI-GGUF** custom node
2. **GGUF quantized models** (faster, less memory)

### Models to Download

#### Text-to-Video (T2V) - ~20GB total
From: https://huggingface.co/bullerwins/Wan2.2-T2V-A14B-GGUF
- `Wan2.2-T2V-A14B-HighNoise-Q5_K_M.gguf` (~10GB)
- `Wan2.2-T2V-A14B-LowNoise-Q5_K_M.gguf` (~10GB)

#### Image-to-Video (I2V) - ~20GB total
From: https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF
- `Wan2.2-I2V-A14B-HighNoise-Q5_K_M.gguf`
- `Wan2.2-I2V-A14B-LowNoise-Q5_K_M.gguf`

#### Shared Models
- VAE: `wan2.2_vae.safetensors` (~300MB)
- Text Encoder: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (~5GB)

From: https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged

### Alternative: 5B Hybrid Model (Smaller)
For less disk space, can use:
- `wan2.2_ti2v_5B_fp16.safetensors` - Supports both T2V and I2V
- Smaller but lower quality than 14B

### Custom Nodes Required
```bash
cd ~/ComfyUI/custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
```

### Workflow Changes
- Replace `Load Diffusion Model` nodes with `Unet Loader (GGUF)`
- Use `uni_pc` scheduler → change to `euler` for Mac
- Models go in `ComfyUI/models/unet/` directory

### Sources
- https://comfyui-wiki.com/en/tutorial/advanced/video/wan2.2/wan2-2
- https://papayabytes.substack.com/p/guide-comfyui-and-wan-22-image-to
- https://huggingface.co/bullerwins/Wan2.2-T2V-A14B-GGUF

### Compared to AnimateDiff
| Feature | AnimateDiff | Wan 2.2 |
|---------|-------------|---------|
| Quality | Good | Excellent |
| Motion | Basic temporal | Complex natural |
| Speed on MPS | ~3.5min/16 frames | TBD |
| Model size | ~1.7GB | ~20-40GB |
| Year | 2023 | 2025 |

---

## Test Results on Mac Mini (2026-01-28)

### Hardware
- Mac Mini with ~27GB unified memory
- MPS (Apple Silicon)

### Results

| Model | Status | Notes |
|-------|--------|-------|
| Wan 2.2 14B GGUF (Q5) | ❌ OOM | Needs ~40GB+ |
| Wan 2.2 5B GGUF (Q5) | ❌ Too slow | 7+ min, didn't complete |
| AnimateDiff (SD 1.5) | ✅ Works | ~3.5 min for 16 frames |

### Conclusion
Wan 2.2 GGUF is not practical on Mac with < 64GB RAM. 
Stick with AnimateDiff for local video generation on Apple Silicon.

For Wan 2.2 quality, consider:
- Cloud GPU (RunPod, etc.)
- Mac Studio with 64GB+ RAM
- Official FP8 models instead of GGUF (untested)
