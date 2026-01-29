#!/usr/bin/env python3
"""
Batch Video Generation Script
Queues multiple generations via ComfyUI API
"""

import json
import argparse
import requests
import time
import random
from pathlib import Path
from datetime import datetime

COMFYUI_URL = "http://127.0.0.1:8188"

def load_workflow(workflow_path: str) -> dict:
    """Load a workflow JSON file."""
    with open(workflow_path, 'r') as f:
        return json.load(f)

def update_prompt(workflow: dict, prompt: str, negative: str = None) -> dict:
    """Update prompt in workflow nodes."""
    for node_id, node in workflow.items():
        if isinstance(node, dict) and node.get('class_type') == 'CLIPTextEncode':
            inputs = node.get('inputs', {})
            # Check if this is positive or negative prompt based on common patterns
            if 'text' in inputs:
                current = inputs['text']
                if any(neg in current.lower() for neg in ['blur', 'ugly', 'bad', 'worst']):
                    if negative:
                        inputs['text'] = negative
                else:
                    inputs['text'] = prompt
    return workflow

def update_seed(workflow: dict, seed: int = None) -> dict:
    """Update seed in KSampler nodes."""
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
    
    for node_id, node in workflow.items():
        if isinstance(node, dict) and 'KSampler' in node.get('class_type', ''):
            if 'inputs' in node and 'seed' in node['inputs']:
                node['inputs']['seed'] = seed
    return workflow

def queue_prompt(workflow: dict) -> str:
    """Send workflow to ComfyUI queue."""
    payload = {"prompt": workflow}
    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=payload)
        response.raise_for_status()
        return response.json().get('prompt_id')
    except requests.exceptions.RequestException as e:
        print(f"Error queuing prompt: {e}")
        return None

def check_status(prompt_id: str) -> dict:
    """Check generation status."""
    try:
        response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        if response.status_code == 200:
            return response.json().get(prompt_id, {})
    except:
        pass
    return {}

def wait_for_completion(prompt_id: str, timeout: int = 600) -> bool:
    """Wait for generation to complete."""
    start = time.time()
    while time.time() - start < timeout:
        status = check_status(prompt_id)
        if status.get('status', {}).get('completed'):
            return True
        if status.get('status', {}).get('status_str') == 'error':
            print(f"Generation failed: {status}")
            return False
        time.sleep(2)
    print("Timeout waiting for generation")
    return False

def run_batch(prompts: list, workflow_path: str, output_dir: str, delay: int = 5):
    """Run batch generation from prompt list."""
    workflow_template = load_workflow(workflow_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    total = len(prompts)
    
    print(f"\n🎬 Starting batch generation: {total} prompts")
    print(f"   Workflow: {workflow_path}")
    print(f"   Output: {output_dir}\n")
    
    for i, prompt_data in enumerate(prompts, 1):
        if isinstance(prompt_data, str):
            prompt = prompt_data
            negative = None
            seed = None
        else:
            prompt = prompt_data.get('prompt', '')
            negative = prompt_data.get('negative')
            seed = prompt_data.get('seed')
        
        print(f"[{i}/{total}] Generating: {prompt[:50]}...")
        
        # Prepare workflow
        workflow = json.loads(json.dumps(workflow_template))  # Deep copy
        workflow = update_prompt(workflow, prompt, negative)
        workflow = update_seed(workflow, seed)
        
        # Queue and wait
        prompt_id = queue_prompt(workflow)
        if prompt_id:
            success = wait_for_completion(prompt_id)
            results.append({
                'prompt': prompt,
                'prompt_id': prompt_id,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
            if success:
                print(f"   ✅ Complete")
            else:
                print(f"   ❌ Failed")
        else:
            print(f"   ❌ Failed to queue")
            results.append({'prompt': prompt, 'success': False})
        
        # Delay between generations
        if i < total:
            time.sleep(delay)
    
    # Save results log
    log_path = output_path / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"\n✨ Batch complete: {success_count}/{total} successful")
    print(f"   Log: {log_path}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Batch video generation via ComfyUI')
    parser.add_argument('--workflow', '-w', required=True, help='Path to workflow JSON')
    parser.add_argument('--prompts', '-p', help='Path to prompts file (one per line or JSON array)')
    parser.add_argument('--prompt', help='Single prompt to generate')
    parser.add_argument('--count', '-n', type=int, default=1, help='Number of variations (with --prompt)')
    parser.add_argument('--output', '-o', default='./outputs', help='Output directory')
    parser.add_argument('--delay', '-d', type=int, default=5, help='Delay between generations (seconds)')
    parser.add_argument('--url', default=COMFYUI_URL, help='ComfyUI server URL')
    
    args = parser.parse_args()
    global COMFYUI_URL
    COMFYUI_URL = args.url
    
    # Build prompt list
    prompts = []
    
    if args.prompts:
        prompts_path = Path(args.prompts)
        if prompts_path.suffix == '.json':
            with open(prompts_path) as f:
                prompts = json.load(f)
        else:
            with open(prompts_path) as f:
                prompts = [line.strip() for line in f if line.strip()]
    elif args.prompt:
        prompts = [args.prompt] * args.count
    else:
        print("Error: Provide --prompts file or --prompt text")
        return
    
    if not prompts:
        print("Error: No prompts to process")
        return
    
    run_batch(prompts, args.workflow, args.output, args.delay)

if __name__ == '__main__':
    main()
