# Slider Settings Guide

LoRA-based concept sliders for controlling age, body features, and style attributes.

## How Sliders Work

Sliders are trained LoRAs that shift latent space in a specific direction. Weight controls intensity:
- **0.0** = No effect
- **Positive** = More of the attribute
- **Negative** = Less of the attribute (opposite direction)

## Age Slider

**Model:** `age_slider_v2.safetensors`

| Weight | Effect |
|--------|--------|
| -1.0 to -0.5 | Significantly younger (may distort) |
| -0.5 to -0.2 | Noticeably younger |
| -0.2 to 0.0 | Slightly younger |
| 0.0 | No change |
| 0.0 to 0.2 | Slightly older |
| 0.2 to 0.5 | Noticeably older |
| 0.5 to 1.0 | Significantly older (may add wrinkles) |

**Recommended:** Stay within `-0.5` to `0.5` for realistic results.

**Tips:**
- Combine with face restoration (GFPGAN) to clean up artifacts
- Lower weights work better for video (less flickering)
- Test on single frame first before generating full video

## Body/Muscle Slider

**Model:** `muscle_slider_v1.safetensors`

| Weight | Effect |
|--------|--------|
| -0.8 to -0.5 | Very slim/thin |
| -0.5 to -0.2 | Slim |
| -0.2 to 0.0 | Slightly slim |
| 0.0 | No change |
| 0.0 to 0.3 | Slightly athletic |
| 0.3 to 0.6 | Athletic/toned |
| 0.6 to 1.0 | Very muscular |

**Recommended:** `-0.5` to `0.6` for natural-looking results.

## Combining Multiple Sliders

When using multiple LoRAs:
1. Total LoRA weight should stay under 1.5 combined
2. Apply in order: base model → age → body → style
3. Reduce individual weights when stacking (0.3-0.4 each)

**Example stack:**
```
age_slider: 0.3
muscle_slider: 0.4
style_lora: 0.5
Total: 1.2 ✓
```

## Video-Specific Considerations

Sliders can cause temporal inconsistency (flickering). Mitigate with:

1. **Lower weights** - Use 50-70% of image-gen weights
2. **Temporal smoothing** - AnimateDiff handles some of this
3. **Consistent seed** - Lock seed for coherent sequences
4. **Post-processing** - Frame interpolation can smooth artifacts

## Troubleshooting

**Distorted faces:**
- Weight too high, reduce by 0.2
- Add face restoration node after generation

**Flickering between frames:**
- Reduce slider weight
- Increase AnimateDiff context length if possible
- Try different motion module

**No visible effect:**
- LoRA not loaded (check file path)
- Weight too low (try 0.5)
- Incompatible base model (sliders trained on SD1.5)

## Finding More Sliders

- [Civitai](https://civitai.com) - Search "slider" or "concept slider"
- [HuggingFace](https://huggingface.co) - ntc-ai/SDXL-LoRA-slider collections
- Custom training with [slider-trainer](https://github.com/rohitgandikota/sliders)
