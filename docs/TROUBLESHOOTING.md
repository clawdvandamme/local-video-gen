# Troubleshooting Guide

## Startup Issues

### ComfyUI won't start
```bash
# Check if already running
lsof -i :8188

# Kill existing process
kill $(lsof -t -i :8188)

# Check logs
tail -50 /tmp/comfyui-videogen.log
```

### Port already in use
```bash
# Use different port
./scripts/launch.sh 8189
```

### Python/venv issues
```bash
cd ~/ComfyUI
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Generation Issues

### Out of Memory (OOM)
- Reduce resolution: 512x512 instead of 768x768
- Reduce frame count: 8 frames instead of 16
- Close other apps using GPU memory
- Use `--force-fp16` flag (default in launcher)

### Slow generation
- Normal on M1/M2: ~1-2 minutes per 16-frame video
- M3 Max/Ultra will be faster
- First generation is slower (model loading)

### Black/corrupted output
- Check VAE is loaded correctly
- Try different seed
- Reduce CFG scale (try 5-7 instead of 7.5)

### AnimateDiff not working
- Verify motion module loaded: Check ComfyUI console
- Use compatible checkpoint (SD 1.5 for mm_sd_v15_v2)
- Context length must match batch size

## Face Swap Issues

### Face not detected
- Ensure face is clearly visible in source image
- Try higher resolution source (512x512 minimum)
- Check InsightFace models are downloaded

### Face looks wrong
- Adjust IPAdapter weight (0.7-0.9)
- Use GFPGAN for face restoration
- Try different source angle

## Pose Control Issues

### Pose not followed
- Increase ControlNet strength (0.7-0.9)
- Use DWPreprocessor for better pose detection
- Ensure pose image matches target resolution

### Weird body parts
- Lower ControlNet strength
- Add negative prompt: "extra limbs, mutated hands"
- Use depth ControlNet in addition to OpenPose

## Slider Issues

### Age slider not working
- Check LoRA is loaded (green connection in ComfyUI)
- Adjust weight: -0.5 (younger) to 0.5 (older)
- Some checkpoints respond differently

### Muscle slider too strong
- Reduce weight to 0.2-0.3
- Combine with skin tone LoRA to counteract tanning effect

## Model Loading Issues

### Model not found
```bash
# Check model locations
ls ~/ComfyUI/models/checkpoints/
ls ~/ComfyUI/models/loras/
ls ~/ComfyUI/models/controlnet/
```

### Wrong model format
- Use .safetensors or .ckpt files
- SDXL models won't work with SD 1.5 AnimateDiff

## Node Errors

### Missing node type
- Restart ComfyUI to reload custom nodes
- Check custom_nodes folder for errors
- Install missing node via ComfyUI Manager

### Red nodes in workflow
- Node not installed or failed to load
- Check ComfyUI console for import errors
- Try: ComfyUI Manager → Install Missing Nodes

## Quick Fixes

### Reset everything
```bash
# Stop ComfyUI
kill $(lsof -t -i :8188)

# Clear ComfyUI cache
rm -rf ~/ComfyUI/user/default/ComfyUI-Manager/

# Restart
./scripts/launch.sh
```

### Verify installation
```bash
# Check all models present
echo "Checkpoints:" && ls ~/ComfyUI/models/checkpoints/*.safetensors
echo "LoRAs:" && ls ~/ComfyUI/models/loras/*.safetensors  
echo "ControlNets:" && ls ~/ComfyUI/models/controlnet/*.pth
echo "AnimateDiff:" && ls ~/ComfyUI/models/animatediff_models/*.ckpt
```

---
*Last updated: 2026-01-28*
