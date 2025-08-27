import os
import torch

# dataset
MOUSE_DATASET_PATH = "../dataset/mouse"
KEYBOARD_DATASET_PATH = "../dataset/keyboard"
CAN_DATASET_PATH = "../dataset/can"
COMBINED_DATASET_PATH = "../dataset/combined"

# data yaml
MOUSE_DATA_YAML = os.path.join(MOUSE_DATASET_PATH, "data.yaml")
KEYBOARD_DATA_YAML = os.path.join(KEYBOARD_DATASET_PATH, "data.yaml")
CAN_DATA_YAML = os.path.join(CAN_DATASET_PATH, "data.yaml")
COMBINED_DATA_YAML = os.path.join(COMBINED_DATASET_PATH, "data.yaml")

# model
MOUSE_MODEL_NAME = "mouse_detection_v1"
KEYBOARD_MODEL_NAME = "keyboard_detection_v1"
CAN_MODEL_NAME = "can_detection_v1"
COMBINED_MODEL_NAME = "combined_detection_v1"

# device configuration
DEVICE = (
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)
print(f"Using device: {DEVICE}")

# result model (weight file)
MOUSE_BEST_MODEL_PATH = os.path.join("weight", "mouse.pt") # mouse
CAN_BEST_MODEL_PATH = os.path.join("weight", "can.pt") # can
KEYBOARD_BEST_MODEL_PATH = os.path.join("weight", "keyboard.pt") # keyboard
COMBINED_BEST_MODEL_PATH = os.path.join("weight", "combined.pt") # combination(mouse & can & keyboard)