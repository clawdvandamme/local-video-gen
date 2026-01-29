# NSFW Mode Guide

This guide covers generating adult content locally with full privacy.

## Requirements

1. **Uncensored checkpoint** - Models without safety filters:
   - `realisticVisionV51_v51VAE.safetensors` (included) - photorealistic
   - Alternative: Deliberate, AbsoluteReality, or any "uncensored" tagged model

2. **No cloud services** - All processing runs locally on your machine

## Workflows

Use the NSFW-specific workflow variants:
- `workflows/text-to-video-nsfw.json` - Text prompt to video
- `workflows/image-to-video-nsfw.json` - Image input to video

## Recommended Settings

### Positive Prompt Tips
- Be specific about subject, pose, setting, lighting
- Include quality tags: `masterpiece, best quality, highly detailed, 8k`
- Specify camera angle: `front view, from above, close-up`
- Add style: `photorealistic, cinematic lighting, soft shadows`

### Negative Prompt (copy this)
```
worst quality, low quality, blurry, distorted, deformed, bad anatomy, 
bad proportions, extra limbs, missing limbs, disfigured, ugly, 
watermark, text, logo, signature, cropped, out of frame, 
poorly drawn hands, poorly drawn face, mutation, mutated
```

### Quality Settings
- Steps: 25-30 (higher = better quality, slower)
- CFG Scale: 7-8 (higher = more prompt adherence)
- Sampler: `euler_ancestral` or `dpmpp_2m_karras`

## Face Swap with NSFW

1. Generate base video with NSFW workflow
2. Apply face swap using InstantID/ReActor nodes
3. Use GFPGAN for face restoration (strength 0.5-0.7)

**Important:** Source face image should be:
- Clear, front-facing
- Good lighting
- High resolution (512x512+)

## Legal & Ethical Notes

- Only generate content of fictional characters or yourself
- Never create non-consensual content of real people
- Check your local laws regarding AI-generated content
- Keep outputs private and secure

## Troubleshooting

**Black/corrupted output:**
- Reduce resolution (start with 512x288)
- Lower frame count to 16
- Check VRAM usage

**Censored/filtered output:**
- Verify you're using uncensored checkpoint
- Some LoRAs may have built-in filters - avoid them

**Poor quality:**
- Increase steps to 30+
- Try different sampler (dpmpp_2m_karras recommended)
- Add more quality tags to prompt
