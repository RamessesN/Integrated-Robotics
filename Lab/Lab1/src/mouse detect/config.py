import os
import torch

DATASET_PATH = "../../dataset/mouse"
DATA_YAML = os.path.join(DATASET_PATH, "data.yaml")

MODEL_NAME = "mouse_detection_v12"

DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {DEVICE}")

BEST_MODEL_PATH = os.path.join("../..", "runs", "train", MODEL_NAME, "weights", "best.pt")