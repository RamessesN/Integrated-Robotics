import os
import torch

# dataset
COMBINED_DATASET_PATH: str = "../dataset/combined"

# data yaml
COMBINED_DATA_YAML = os.path.join(COMBINED_DATASET_PATH, "data.yaml")

# model
COMBINED_MODEL_NAME: str = "combined_detection_v1"

# device configuration
DEVICE: str = (
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.mps.is_available() else
    "xpu" if torch.xpu.is_available() else
    "cpu"
)

# result model (weight file)
COMBINED_BEST_MODEL_PATH = os.path.join("weight", "combined_v1.pt") # combination(mouse & can & keyboard)