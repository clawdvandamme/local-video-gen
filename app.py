#!/usr/bin/env python3
"""
Local Video Generator - Simple UI
Wraps ComfyUI with a clean Gradio interface
"""

import gradio as gr
import requests
import json
import time
import random
import os
import subprocess
from pathlib import Path
from PIL import Image

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path.home() / "ComfyUI" / "output"

# === ComfyUI API Helpers ===

def queue_prompt(workflow: dict) -> str:
    """Send workflow to ComfyUI, return prompt_id"""
    p = {"prompt": workflow}
    r = requests.post(f"{COMFYUI_URL}/prompt", json=p)
    resp = r.json()
    if "error" in resp:
        raise Exception(f"ComfyUI error: {resp['error']}")
    return resp.get("prompt_id")

def get_queue() -> dict:
    """Get current queue status"""
    r = requests.get(f"{COMFYUI_URL}/queue")
    return r.json()

def cancel_all():
    """Cancel all running and pending jobs"""
    requests.post(f"{COMFYUI_URL}/interrupt")
    requests.post(f"{COMFYUI_URL}/queue", json={"clear": True})
    return "🛑 Cancelled all jobs"

def get_history(prompt_id: str) -> dict:
    """Get execution history for a prompt"""
    r = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
    return r.json()

def get_progress() -> dict:
    """Get current execution progress"""
    try:
        # Check queue for running job info
        q = get_queue()
        running = q.get("queue_running", [])
        if running:
            return {"status": "running", "queue_size": len(running)}
        return {"status": "idle"}
    except:
        return {"status": "error"}

def get_queue_status() -> str:
    """Get formatted queue status"""
    try:
        q = get_queue()
        running = len(q.get("queue_running", []))
        pending = len(q.get("queue_pending", []))
        if running == 0 and pending == 0:
            return "✅ Idle"
        return f"🔄 Running: {running} | Pending: {pending}"
    except:
        return "❌ ComfyUI not responding"

def get_output_files(history: dict) -> list:
    """Extract output file paths from history"""
    files = []
    outputs = history.get("outputs", {})
    for node_id, node_output in outputs.items():
        for key in ["gifs", "images"]:
            if key in node_output:
                for item in node_output[key]:
                    subfolder = item.get("subfolder", "")
                    filename = item["filename"]
                    if subfolder:
                        files.append(OUTPUT_DIR / subfolder / filename)
                    else:
                        files.append(OUTPUT_DIR / filename)
    return files

def webp_to_mp4(webp_path: Path) -> Path:
    """Convert animated webp to mp4"""
    mp4_path = webp_path.with_suffix('.mp4')
    
    # Extract frames using PIL
    img = Image.open(webp_path)
    frames = []
    try:
        while True:
            frames.append(img.copy())
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    
    if not frames:
        return None
    
    # Save frames temporarily
    temp_dir = Path("/tmp/video_frames")
    temp_dir.mkdir(exist_ok=True)
    for i, frame in enumerate(frames):
        frame.save(temp_dir / f"frame_{i:04d}.png")
    
    # Convert to mp4
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "8",
        "-i", str(temp_dir / "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(mp4_path)
    ], capture_output=True)
    
    # Cleanup
    for f in temp_dir.glob("*.png"):
        f.unlink()
    
    return mp4_path if mp4_path.exists() else None

# === Workflow Loaders ===

def load_workflow(name: str) -> dict:
    """Load a workflow JSON file"""
    workflow_dir = Path(__file__).parent / "workflows"
    with open(workflow_dir / f"{name}.json") as f:
        return json.load(f)

# === Generation Functions ===

def generate_text_to_video(
    prompt: str,
    negative_prompt: str,
    frames: int,
    fps: int,
    width: int,
    height: int,
    steps: int,
    cfg: float,
):
    """Generate video from text prompt"""
    
    if not prompt.strip():
        yield None, "❌ Please enter a prompt", "✅ Idle"
        return
    
    try:
        yield None, "📂 Loading workflow...", "🔄 Starting..."
        
        workflow = load_workflow("text-to-video-api")
        
        # Update workflow with user inputs
        for node_id, node in workflow.items():
            if node.get("class_type") == "CLIPTextEncode":
                meta_title = str(node.get("_meta", {}).get("title", "")).lower()
                if "positive" in meta_title or node_id == "6":
                    node["inputs"]["text"] = prompt
                elif "negative" in meta_title or node_id == "7":
                    node["inputs"]["text"] = negative_prompt
            
            if node.get("class_type") == "KSampler":
                node["inputs"]["steps"] = steps
                node["inputs"]["cfg"] = cfg
                node["inputs"]["seed"] = random.randint(0, 2**32 - 1)
            
            if node.get("class_type") == "EmptyLatentImage":
                node["inputs"]["width"] = width
                node["inputs"]["height"] = height
                node["inputs"]["batch_size"] = frames
            
            if node.get("class_type") == "SaveAnimatedWEBP":
                node["inputs"]["fps"] = float(fps)
        
        yield None, "📤 Sending to ComfyUI...", "🔄 Queuing..."
        
        prompt_id = queue_prompt(workflow)
        
        yield None, f"🆔 Job queued: {prompt_id[:8]}...\n⏳ Generating {frames} frames @ {width}x{height}...", get_queue_status()
        
        # Poll for completion with progress updates
        start = time.time()
        timeout = 600
        last_check = 0
        
        while time.time() - start < timeout:
            elapsed = int(time.time() - start)
            
            # Check completion
            history = get_history(prompt_id)
            if prompt_id in history:
                status = history[prompt_id].get("status", {})
                if status.get("status_str") == "error":
                    msgs = status.get("messages", [])
                    error_msg = msgs[-1] if msgs else "Unknown error"
                    yield None, f"❌ Generation failed: {error_msg}", "✅ Idle"
                    return
                
                # Success - get output
                yield None, f"✅ Generation complete! ({elapsed}s)\n🔄 Converting to MP4...", "✅ Processing..."
                
                files = get_output_files(history[prompt_id])
                if files:
                    webp_file = files[0]
                    mp4_file = webp_to_mp4(webp_file)
                    
                    if mp4_file and mp4_file.exists():
                        yield str(mp4_file), f"✅ Done! ({elapsed}s)\n📁 {mp4_file.name}", "✅ Idle"
                    else:
                        yield str(webp_file), f"✅ Done! ({elapsed}s)\n📁 {webp_file.name} (webp)", "✅ Idle"
                else:
                    yield None, f"⚠️ Complete but no output found", "✅ Idle"
                return
            
            # Progress update every 3 seconds
            progress_msg = f"⏳ Generating... ({elapsed}s elapsed)\n"
            progress_msg += f"   {frames} frames @ {width}x{height}, {steps} steps"
            
            yield None, progress_msg, get_queue_status()
            time.sleep(3)
        
        yield None, "⏰ Generation timed out (10 min limit)", "✅ Idle"
            
    except Exception as e:
        yield None, f"❌ Error: {str(e)}", "✅ Idle"

def check_comfyui_status():
    """Check if ComfyUI is running"""
    try:
        r = requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        if r.status_code == 200:
            stats = r.json()
            devices = stats.get("devices", [{}])
            if devices:
                vram = devices[0].get("vram_total", 0) / 1e9
                name = devices[0].get("name", "Unknown")
                return f"✅ ComfyUI Online | {name} | {vram:.1f}GB"
            return "✅ ComfyUI Online"
    except:
        pass
    return "❌ ComfyUI Offline - Run: cd ~/ComfyUI && python main.py"

def get_recent_outputs():
    """List recent output files"""
    try:
        files = sorted(OUTPUT_DIR.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]
        if not files:
            files = sorted(OUTPUT_DIR.glob("*.webp"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]
        return "\n".join([f"• {f.name} ({f.stat().st_size // 1024}KB)" for f in files]) or "No outputs yet"
    except:
        return "Error reading outputs"

# === UI ===

with gr.Blocks(title="Local Video Generator") as app:
    gr.Markdown("# 🎬 Local Video Generator")
    
    with gr.Row():
        status = gr.Textbox(value=check_comfyui_status(), label="ComfyUI", interactive=False, scale=3)
        queue_status = gr.Textbox(value=get_queue_status(), label="Queue", interactive=False, scale=1)
    
    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh", scale=1)
        cancel_btn = gr.Button("🛑 Cancel All", variant="stop", scale=1)
        
    refresh_btn.click(check_comfyui_status, outputs=status)
    refresh_btn.click(get_queue_status, outputs=queue_status)
    cancel_btn.click(cancel_all, outputs=queue_status)
    
    with gr.Tabs():
        # === Text to Video ===
        with gr.Tab("📝 Text to Video"):
            with gr.Row():
                with gr.Column(scale=1):
                    t2v_prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="A cat walking through a garden, cinematic lighting",
                        lines=3
                    )
                    t2v_negative = gr.Textbox(
                        label="Negative Prompt",
                        value="ugly, blurry, low quality, distorted",
                        lines=2
                    )
                    with gr.Row():
                        t2v_frames = gr.Slider(4, 32, value=16, step=1, label="Frames")
                        t2v_fps = gr.Slider(4, 24, value=8, step=1, label="FPS")
                    with gr.Row():
                        t2v_width = gr.Slider(256, 768, value=512, step=64, label="Width")
                        t2v_height = gr.Slider(256, 768, value=512, step=64, label="Height")
                    with gr.Row():
                        t2v_steps = gr.Slider(10, 40, value=20, step=1, label="Steps")
                        t2v_cfg = gr.Slider(1, 15, value=7.5, step=0.5, label="CFG")
                    t2v_btn = gr.Button("🎬 Generate Video", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    t2v_output = gr.Video(label="Output", height=400)
                    t2v_logs = gr.Textbox(label="Status", lines=6, interactive=False)
            
            t2v_btn.click(
                generate_text_to_video,
                inputs=[t2v_prompt, t2v_negative, t2v_frames, t2v_fps, t2v_width, t2v_height, t2v_steps, t2v_cfg],
                outputs=[t2v_output, t2v_logs, queue_status]
            )
        
        # === Recent Outputs ===
        with gr.Tab("📁 Outputs"):
            outputs_list = gr.Textbox(label="Recent Outputs", lines=15, interactive=False, value=get_recent_outputs())
            outputs_refresh = gr.Button("🔄 Refresh")
            outputs_refresh.click(get_recent_outputs, outputs=outputs_list)
            gr.Markdown(f"**Output folder:** `{OUTPUT_DIR}`")
        
        # === Settings ===
        with gr.Tab("⚙️ Settings"):
            gr.Markdown("## Configuration")
            gr.Markdown(f"**Output Directory:** `{OUTPUT_DIR}`")
            gr.Markdown(f"**ComfyUI URL:** `{COMFYUI_URL}`")
            gr.Markdown("### Models")
            gr.Markdown("- Realistic Vision V5.1")
            gr.Markdown("- SD 1.5 base")

if __name__ == "__main__":
    app.launch(server_port=7860)
