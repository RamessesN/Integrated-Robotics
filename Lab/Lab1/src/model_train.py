from ultralytics import YOLO
from env_config import CAN_DATA_YAML, CAN_MODEL_NAME, DEVICE

def train_model():
    print("Training model...")

    model = YOLO("weight/can.pt")   # Loading Pre-trained model

    results = model.train(
        data = CAN_DATA_YAML,
        epochs = 100,
        imgsz = 640,
        batch = 36,
        name = CAN_MODEL_NAME,
        device = DEVICE,
        workers = 4,
        project = "./runs/train_keyboard",
        exist_ok = False
    )

    print("Training Finished！")

if __name__ == "__main__":
    train_model()