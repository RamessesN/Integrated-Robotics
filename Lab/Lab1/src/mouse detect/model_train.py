from ultralytics import YOLO
from env_config import DATA_YAML, MODEL_NAME, DEVICE

def train_model():
    print("Training model...")

    model = YOLO("../yolov8n.pt")   # Loading Pre-trained model

    results = model.train(
        data=DATA_YAML,
        epochs=100,
        imgsz=640,
        batch=36,
        name=MODEL_NAME,
        device=DEVICE,
        workers=4,
        project="../runs/train",
        exist_ok=False
    )

    print("Training Finished！")

if __name__ == "__main__":
    train_model()