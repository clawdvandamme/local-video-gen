# Installation Guide: Local AI Video Generator

## System Requirements

### Minimum
- macOS 12+ (Monterey) or Windows 10/Linux
- Apple Silicon (M1/M2/M3) or NVIDIA GPU with 8GB+ VRAM
- 16GB RAM
- 50GB free disk space (100GB+ recommended)
- Python 3.10-3.12 (3.11 recommended)

### Recommended
- Apple Silicon M2 Pro/Max/Ultra or NVIDIA RTX 3080+
- 32GB+ RAM
- 100GB+ free disk space
- Fast SSD storage

---

## Installation Steps

### Step 1: Clone ComfyUI

```bash
cd ~
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### Step 2: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

### Step 3: Install PyTorch

**For Apple Silicon (MPS):**
```bash
pip install torch torchvision torchaudio
```

**For NVIDIA GPU (CUDA):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Step 4: Install ComfyUI Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install ComfyUI Manager

```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..
```

### Step 6: Start ComfyUI

```bash
python main.py
# Access at http://127.0.0.1:8188
```

---

## Installing Custom Nodes

### Via ComfyUI Manager (Recommended)

1. Open ComfyUI in browser
2. Click "Manager" button
3. Search and install:
   - ComfyUI-AnimateDiff-Evolved
   - ComfyUI-VideoHelperSuite
   - ComfyUI_IPAdapter_plus
   - comfyui_controlnet_aux
   - ComfyUI-Impact-Pack
   - ReActor Node (for face swap)

### Manual Installation

```bash
cd ~/ComfyUI/custom_nodes

# AnimateDiff
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
cd ComfyUI-AnimateDiff-Evolved && pip install -r requirements.txt && cd ..

# Video Helper Suite
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
cd ComfyUI-VideoHelperSuite && pip install -r requirements.txt && cd ..

# ControlNet Aux
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
cd comfyui_controlnet_aux && pip install -r requirements.txt && cd ..

# Impact Pack
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
cd ComfyUI-Impact-Pack && pip install -r requirements.txt && cd ..
```

---

## Installing FaceFusion (Standalone)

```bash
cd ~
git clone https://github.com/facefusion/facefusion.git
cd facefusion
python install.py
```

Or use the ComfyUI ReActor node which integrates face swap directly.

---

## Downloading Models

### Using Download Script

```bash
cd ~/local-video-gen
python scripts/download_models.py
```

### Manual Downloads

See `docs/MODELS.md` for complete list with links.

**Essential models:**
1. Base checkpoint → `ComfyUI/models/checkpoints/`
2. AnimateDiff motion module → `ComfyUI/models/animatediff_models/`
3. VAE → `ComfyUI/models/vae/`
4. ControlNet OpenPose → `ComfyUI/models/controlnet/`

---

## Apple Silicon Optimization

### Enable MPS (Metal Performance Shaders)

ComfyUI auto-detects MPS on Apple Silicon. Verify with:

```python
import torch
print(torch.backends.mps.is_available())  # Should be True
```

### Memory Settings

For M1/M2 (8-16GB unified memory):
```bash
python main.py --lowvram
```

For M1 Pro/Max/M2 Pro/Max (16-32GB):
```bash
python main.py --normalvram
```

For M1 Ultra/M2 Ultra (64GB+):
```bash
python main.py --highvram
```

---

## Troubleshooting

### "MPS backend not available"

Ensure PyTorch is installed correctly for macOS:
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio
```

### "CUDA out of memory"

- Use `--lowvram` flag
- Reduce resolution
- Reduce batch size
- Use FP16 models

### "Model not found"

- Check model is in correct directory
- Verify filename matches workflow
- Restart ComfyUI after adding models

### Slow generation

- Enable xformers (NVIDIA): `pip install xformers`
- Use smaller resolution
- Use fewer steps
- Use faster sampler (euler_a, dpm++ 2m sde)

---

## Quick Start After Installation

```bash
# Start ComfyUI
cd ~/ComfyUI
source venv/bin/activate
python main.py

# Open browser to http://127.0.0.1:8188
# Load a workflow from local-video-gen/workflows/
# Generate!
```

---

## Directory Structure After Setup

```
~/
├── ComfyUI/
│   ├── models/
│   │   ├── checkpoints/
│   │   ├── vae/
│   │   ├── loras/
│   │   ├── controlnet/
│   │   └── animatediff_models/
│   ├── custom_nodes/
│   │   ├── ComfyUI-Manager/
│   │   ├── ComfyUI-AnimateDiff-Evolved/
│   │   ├── ComfyUI-VideoHelperSuite/
│   │   └── ...
│   └── venv/
│
├── facefusion/  (optional standalone)
│
└── clawd/projects/local-video-gen/
    ├── workflows/
    ├── docs/
    └── scripts/
```

---

*Installation guide: 2026-01-28*
