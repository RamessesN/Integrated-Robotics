import os
import torch

# dataset
MOUSE_DATASET_PATH = "../dataset/mouse"
KEYBOARD_DATASET_PATH = "../dataset/keyboard"
CAN_DATASET_PATH = "../dataset/can"

# data yaml
MOUSE_DATA_YAML = os.path.join(MOUSE_DATASET_PATH, "data.yaml")
KEYBOARD_DATA_YAML = os.path.join(KEYBOARD_DATASET_PATH, "data.yaml")
CAN_DATA_YAML = os.path.join(CAN_DATASET_PATH, "data.yaml")

# model
MOUSE_MODEL_NAME = "mouse_detection_v1"
KEYBOARD_MODEL_NAME = "keyboard_detection_v1"
CAN_MODEL_NAME = "can_detection_v1"

# device configuration
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# best model
MOUSE_BEST_MODEL_PATH = os.path.join("weight", "mouse.pt") # step1: mouse
CAN_BEST_MODEL_PATH = os.path.join("weight", "can.pt") # step2: can
KEYBOARD_BEST_MODEL_PATH = os.path.join("weight", "keyboard.pt") # step3: keyboard