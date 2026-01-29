# Quick Start Tutorial

## 1. Launch

```bash
cd ~/clawd/projects/local-video-gen
./scripts/launch.sh
```

Open http://127.0.0.1:8188

## 2. Load a Workflow

1. Press `Ctrl+O` (or `Cmd+O` on Mac)
2. Navigate to `~/clawd/projects/local-video-gen/workflows/`
3. Select `text-to-video-basic.json`

## 3. Generate Your First Video

1. Find the **positive prompt** node (CLIPTextEncode)
2. Change the text to your prompt:
   ```
   a cat walking on a beach, cute, fluffy, sunset lighting
   ```
3. Click **Queue Prompt** (or press `Ctrl+Enter`)
4. Wait ~1-2 minutes
5. Video appears in output folder: `~/ComfyUI/output/`

## 4. Try Different Features

### Change the Model (for NSFW)
1. Click the **CheckpointLoaderSimple** node
2. Change dropdown to `Realistic_Vision_V5.1_fp16-no-ema.safetensors`

### Add Age Control
1. Right-click canvas → Add Node → loaders → LoraLoader
2. Select `age_slider_v2.safetensors`
3. Connect MODEL output → AnimateDiff input
4. Set strength: negative = younger, positive = older

### Add Pose Control
1. Load `master-video-gen.json` workflow
2. Add your pose reference image to **LoadImage** node
3. DWPreprocessor extracts the pose
4. ControlNet applies it to generation

### Face Swap
1. Add **IPAdapterFaceID** node
2. Load source face image
3. Adjust weight (0.7-1.0)
4. Connect to model pipeline

## 5. Save Your Creation

Generated videos save to:
```
~/ComfyUI/output/AnimateDiff_XXXXX.gif
~/ComfyUI/output/AnimateDiff_XXXXX.mp4
```

## Recommended First Prompts

**Realistic person:**
```
photo of a young woman smiling, natural lighting, 
high quality, detailed face, cinematic
```

**Anime style:**
```
anime girl with blue hair, walking in city, 
studio ghibli style, beautiful, detailed
```

**Action scene:**
```
man running through forest, action shot, 
motion blur, dramatic lighting, cinematic
```

## Next Steps

- Experiment with different prompts
- Try the `master-video-gen.json` for all features
- Adjust sliders and weights
- Combine face swap with pose control

---
*Get help: See TROUBLESHOOTING.md*
