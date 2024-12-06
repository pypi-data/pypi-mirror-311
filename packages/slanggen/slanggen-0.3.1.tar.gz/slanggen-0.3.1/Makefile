# Variables
IMAGE_NAME := slang-backend
HOST_PORT := 80
CONTAINER_PORT := 80
DIST_DIR := dist
VERSION := 0.3.1
WHEEL_FILE := $(DIST_DIR)/slanggen-$(VERSION)-py3-none-any.whl

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
NC := \033[0m # No Color

# Phony targets to prevent conflicts with files of the same name
.PHONY: all build run train check-wheel

# Default target
all: build

# Build Docker image, depends on .whl file
build: check-wheel
	docker build -t $(IMAGE_NAME) .

# Run Docker container
run:
	docker run -p $(HOST_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

# Train the model
train:
	python src/slanggen/main.py

check-wheel: $(WHEEL_FILE)

$(WHEEL_FILE):
	echo -e "$(RED)$(WHEEL_FILE) file not found in $(DIST_DIR). Running 'rye build --clean'...$(NC)"; \
	rye build --clean;
