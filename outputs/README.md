# Example Outputs Gallery

Generated samples will be saved here.

## Directory Structure

```
outputs/
├── text-to-video/      # T2V generations
├── image-to-video/     # I2V generations  
├── face-swap/          # Face swap results
├── pose-control/       # Pose-guided outputs
├── motion-transfer/    # Motion mimicking results
└── experiments/        # Test runs and comparisons
```

## Naming Convention

Files are named: `{workflow}_{timestamp}_{seed}.mp4`

Example: `t2v_20260128_143022_12345.mp4`

## Sample Prompts (to test)

**Text-to-Video:**
- `a woman walking through a sunlit forest, cinematic lighting, 4k`
- `ocean waves crashing on rocks at sunset, slow motion`
- `a cat sitting on a windowsill, watching rain outside`

**With Pose Control:**
- Use reference pose image + prompt describing subject/scene

**With Face Swap:**
- Source: clear front-facing portrait
- Target: video with visible face, similar angle
