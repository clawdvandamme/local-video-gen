# Local Video Gen - Common Commands

COMFYUI_PATH ?= ~/ComfyUI
PYTHON ?= python3
PORT ?= 8188

.PHONY: help check launch batch clean

help:
	@echo "Local Video Gen - Available Commands"
	@echo ""
	@echo "  make check     - Verify installation (models, nodes)"
	@echo "  make launch    - Start ComfyUI server"
	@echo "  make batch     - Run sample batch generation"
	@echo "  make clean     - Clean temp files"
	@echo ""
	@echo "Options:"
	@echo "  COMFYUI_PATH=~/ComfyUI  - Path to ComfyUI"
	@echo "  PORT=8188              - Server port"

# Verify installation
check:
	@$(PYTHON) scripts/check-install.py

# Launch ComfyUI
launch:
	@echo "Starting ComfyUI on port $(PORT)..."
	@cd $(COMFYUI_PATH) && $(PYTHON) main.py --port $(PORT)

# Launch with low VRAM mode
launch-lowvram:
	@echo "Starting ComfyUI (low VRAM mode)..."
	@cd $(COMFYUI_PATH) && $(PYTHON) main.py --port $(PORT) --lowvram

# Run sample batch
batch:
	@$(PYTHON) scripts/batch.py \
		-w workflows/text-to-video-basic.json \
		-p prompts/sample-batch.json \
		-o outputs/batch

# Run single prompt
generate:
	@$(PYTHON) scripts/batch.py \
		-w workflows/text-to-video-basic.json \
		--prompt "$(PROMPT)" \
		-o outputs/single

# Clean temp files
clean:
	@rm -rf /tmp/local-video-gen
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "Cleaned temp files"

# Install custom nodes (requires ComfyUI Manager)
install-nodes:
	@echo "Install nodes via ComfyUI Manager UI at http://localhost:$(PORT)"
	@echo "Required: AnimateDiff-Evolved, controlnet_aux"
	@echo "Optional: LivePortraitKJ, IPAdapter_plus, InstantID"

# Download base models
download-models:
	@echo "Downloading essential models..."
	@mkdir -p $(COMFYUI_PATH)/models/checkpoints
	@mkdir -p $(COMFYUI_PATH)/models/animatediff_models
	@echo "Download Realistic Vision V5.1 from Civitai:"
	@echo "  https://civitai.com/models/4201/realistic-vision-v51"
	@echo ""
	@echo "Download AnimateDiff motion module:"
	@echo "  https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
