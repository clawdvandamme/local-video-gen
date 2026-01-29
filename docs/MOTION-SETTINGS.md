# Motion Transfer Settings Guide

Using LivePortrait, MimicMotion, and related tools to transfer motion from reference videos.

## Overview

Motion transfer extracts movement from a source video and applies it to a target image/video:
- **Source:** Reference video with the motion you want
- **Target:** Image or video of the subject to animate

## LivePortrait Settings

LivePortrait excels at portrait animation (face/head movement).

### Key Parameters

| Parameter | Range | Recommended | Notes |
|-----------|-------|-------------|-------|
| `retargeting_factor` | 0.0-2.0 | 1.0 | Motion intensity multiplier |
| `paste_back` | bool | true | Composite onto original |
| `crop_factor` | 0.5-2.0 | 1.7 | Face crop size |
| `driving_smooth` | 0-10 | 2 | Temporal smoothing |

### Best Practices

1. **Source video quality:**
   - Clear face visibility throughout
   - Consistent lighting
   - Minimal occlusion (hands, objects)
   - 24-30 fps preferred

2. **Target image quality:**
   - Front-facing or 3/4 view
   - Neutral expression works best
   - High resolution (512x512+)
   - Good lighting, no harsh shadows

3. **Motion intensity:**
   - Start with `retargeting_factor: 1.0`
   - Reduce to 0.7-0.8 for subtle movement
   - Increase to 1.2-1.5 for exaggerated motion

## AnimateDiff Motion Modules

For general video generation (not face-specific).

### Module Selection

| Module | Best For | Notes |
|--------|----------|-------|
| `mm_sd_v15_v2` | General motion | Most versatile |
| `mm_sdxl_v10_beta` | SDXL models | Higher quality, more VRAM |
| `temporaldiff-v1-animatediff` | Smooth transitions | Good for slow motion |

### Motion Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `motion_scale` | 0.5-1.5 | Amount of movement |
| `context_length` | 8-32 | Frames considered together |
| `context_overlap` | 2-8 | Frame overlap for consistency |

**Recommended starting point:**
```
motion_scale: 1.0
context_length: 16
context_overlap: 4
```

## MimicMotion Settings

Full-body motion transfer using pose sequences.

### Workflow

1. Extract pose from source video (DWPose/OpenPose)
2. Apply pose sequence to target with ControlNet
3. Blend with reference image for identity

### Key Settings

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| `pose_strength` | 0.7-0.9 | ControlNet conditioning |
| `reference_strength` | 0.3-0.5 | IP-Adapter for identity |
| `temporal_consistency` | enabled | Reduces flickering |

## Common Issues & Fixes

### Jittery motion
- Increase `driving_smooth` (LivePortrait)
- Lower `motion_scale` (AnimateDiff)
- Add frame interpolation post-processing

### Identity loss
- Increase `reference_strength`
- Use IP-Adapter FaceID
- Add face restoration (GFPGAN)

### Unnatural poses
- Source pose too extreme for target
- Reduce `retargeting_factor`
- Try different source video

### Temporal artifacts (flickering)
- Increase `context_length`
- Add temporal smoothing node
- Check for consistent lighting in source

## Performance Tips

1. **VRAM management:**
   - Process in 16-frame chunks
   - Use fp16 precision
   - Enable `--lowvram` flag if needed

2. **Speed vs quality:**
   - Lower `context_length` = faster, less consistent
   - Higher `context_length` = slower, smoother

3. **Batch processing:**
   - Pre-extract all poses before generation
   - Queue multiple targets with same motion
