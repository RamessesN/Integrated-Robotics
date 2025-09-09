import os
import torch

# dataset
BOTTLE_DATASET_PATH: str = "./dataset/cola_can"

# data yaml
BOTTLE_DATA_YAML = os.path.join(BOTTLE_DATASET_PATH, "data.yaml")

# model
BOTTLE_MODEL_NAME: str = "bottle_detection_v1"

# device configuration
DEVICE: str = (
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.mps.is_available() else
    "xpu" if torch.xpu.is_available() else
    "cpu"
)

# result model (weight file)
COMBINED_BEST_MODEL_PATH = os.path.join("weight", "bottle_v1.pt")