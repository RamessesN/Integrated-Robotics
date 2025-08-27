from ultralytics import YOLO
from env_config import COMBINED_DATA_YAML, COMBINED_MODEL_NAME, DEVICE

def train_model():
    print("Training model...")

    model = YOLO("weight/yolov8n.pt")   # Loading Pre-trained model

    results = model.train(
        data = COMBINED_DATA_YAML,
        epochs = 100,
        imgsz = 640,
        batch = 36,
        name = COMBINED_MODEL_NAME,
        device = DEVICE,
        workers = 4,
        project = "./runs/train_combined",
        exist_ok = False
    )

    print("Training Finished！")

if __name__ == "__main__":
    train_model()