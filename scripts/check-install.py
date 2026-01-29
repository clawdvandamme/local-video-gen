#!/usr/bin/env python3
"""
Installation Verification Script
Checks that all required models and nodes are present before running.
"""

import os
import sys
from pathlib import Path

# Color output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def ok(msg): print(f"{GREEN}✓{RESET} {msg}")
def fail(msg): print(f"{RED}✗{RESET} {msg}")
def warn(msg): print(f"{YELLOW}!{RESET} {msg}")

def check_path(path: Path, name: str, required: bool = True) -> bool:
    """Check if a path exists."""
    if path.exists():
        ok(f"{name}: {path}")
        return True
    elif required:
        fail(f"{name}: NOT FOUND - {path}")
        return False
    else:
        warn(f"{name}: not found (optional) - {path}")
        return True

def main():
    print("\n🔍 Local Video Gen - Installation Check\n")
    print("=" * 50)
    
    # Detect ComfyUI path
    comfy_paths = [
        Path.home() / "ComfyUI",
        Path("/opt/ComfyUI"),
        Path.cwd().parent / "ComfyUI",
    ]
    
    comfy_path = None
    for p in comfy_paths:
        if p.exists():
            comfy_path = p
            break
    
    if not comfy_path:
        fail("ComfyUI not found in common locations")
        print("  Checked:", [str(p) for p in comfy_paths])
        sys.exit(1)
    
    ok(f"ComfyUI: {comfy_path}")
    
    errors = 0
    warnings = 0
    
    # Check core directories
    print("\n📁 Directories")
    print("-" * 50)
    
    models_path = comfy_path / "models"
    custom_nodes = comfy_path / "custom_nodes"
    
    if not check_path(models_path, "Models dir"):
        errors += 1
    if not check_path(custom_nodes, "Custom nodes dir"):
        errors += 1
    
    # Check required models
    print("\n🎨 Checkpoints")
    print("-" * 50)
    
    checkpoints = models_path / "checkpoints"
    required_ckpts = [
        ("realisticVisionV51_v51VAE.safetensors", True),
        ("sd_v1-5-pruned-emaonly.safetensors", False),
    ]
    
    for ckpt, required in required_ckpts:
        if not check_path(checkpoints / ckpt, ckpt, required):
            if required:
                errors += 1
            else:
                warnings += 1
    
    # Check AnimateDiff models
    print("\n🎬 AnimateDiff Motion Modules")
    print("-" * 50)
    
    animatediff_path = models_path / "animatediff_models"
    motion_modules = [
        ("mm_sd_v15_v2.ckpt", True),
        ("mm_sdxl_v10_beta.ckpt", False),
    ]
    
    if animatediff_path.exists():
        for mm, required in motion_modules:
            if not check_path(animatediff_path / mm, mm, required):
                if required:
                    errors += 1
                else:
                    warnings += 1
    else:
        warn(f"AnimateDiff models dir not found: {animatediff_path}")
        warnings += 1
    
    # Check ControlNet models
    print("\n🎮 ControlNet Models")
    print("-" * 50)
    
    controlnet_path = models_path / "controlnet"
    controlnet_models = [
        ("control_v11p_sd15_openpose", False),
        ("control_v11f1p_sd15_depth", False),
    ]
    
    if controlnet_path.exists():
        for cn, required in controlnet_models:
            # Check for both .pth and .safetensors
            found = any((controlnet_path / f"{cn}{ext}").exists() 
                       for ext in ['.pth', '.safetensors', ''])
            if found:
                ok(f"{cn}")
            elif required:
                fail(f"{cn}: NOT FOUND")
                errors += 1
            else:
                warn(f"{cn}: not found (optional)")
                warnings += 1
    else:
        warn(f"ControlNet models dir not found: {controlnet_path}")
        warnings += 1
    
    # Check LoRAs
    print("\n🎚️ LoRA Sliders")
    print("-" * 50)
    
    lora_path = models_path / "loras"
    loras = [
        ("age_slider", False),
        ("muscle_slider", False),
    ]
    
    if lora_path.exists():
        for lora, required in loras:
            found = any(f.name.startswith(lora) for f in lora_path.glob("*.safetensors"))
            if found:
                ok(f"{lora}")
            elif required:
                fail(f"{lora}: NOT FOUND")
                errors += 1
            else:
                warn(f"{lora}: not found (optional)")
                warnings += 1
    else:
        warn(f"LoRA dir not found: {lora_path}")
        warnings += 1
    
    # Check custom nodes
    print("\n🔌 Custom Nodes")
    print("-" * 50)
    
    required_nodes = [
        ("ComfyUI-AnimateDiff-Evolved", True),
        ("ComfyUI-Manager", True),
        ("comfyui_controlnet_aux", False),
        ("ComfyUI-LivePortraitKJ", False),
        ("ComfyUI_IPAdapter_plus", False),
        ("ComfyUI_InstantID", False),
    ]
    
    for node, required in required_nodes:
        if not check_path(custom_nodes / node, node, required):
            if required:
                errors += 1
            else:
                warnings += 1
    
    # Check InsightFace models
    print("\n👤 Face Models (InsightFace)")
    print("-" * 50)
    
    insightface_path = models_path / "insightface"
    if insightface_path.exists():
        ok(f"InsightFace dir exists")
        buffalo = insightface_path / "models" / "buffalo_l"
        if buffalo.exists():
            ok("buffalo_l model")
        else:
            warn("buffalo_l model not found (needed for face swap)")
            warnings += 1
    else:
        warn(f"InsightFace dir not found: {insightface_path}")
        warnings += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    if errors == 0 and warnings == 0:
        print(f"\n{GREEN}✨ All checks passed! Ready to generate.{RESET}\n")
    elif errors == 0:
        print(f"\n{YELLOW}⚠️  {warnings} optional components missing.{RESET}")
        print("Core functionality should work.\n")
    else:
        print(f"\n{RED}❌ {errors} required components missing.{RESET}")
        if warnings > 0:
            print(f"{YELLOW}⚠️  {warnings} optional components missing.{RESET}")
        print("\nPlease install missing components before running.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
