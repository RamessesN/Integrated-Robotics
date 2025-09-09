from ultralytics import YOLO
from env_config import BOTTLE_DATA_YAML, BOTTLE_MODEL_NAME, DEVICE

def train_model():
    print("Training model...")

    model = YOLO("./weight/yolo11n.pt")   # Loading Pre-trained model

    results = model.train(
        data = BOTTLE_DATA_YAML,              # Dataset configuration file
        epochs = 100,                         # Number of training rounds
        imgsz = 640,                          # Size of the training image
        batch = 32,                           # ADJUST WITH VRAM
        name = BOTTLE_MODEL_NAME,             # Model name
        device = DEVICE,                      # Running device
        workers = 2,                          # ADJUST WITH CORE NUM
        project = "./runs/train_bottle",      # Save model
        exist_ok = False,                     # Overwrite same name experi
        max_det = 300,
        conf = 0.5,
        iou = 0.6,
        plots = True,
        save_period = 10
    )

    print("Training Finished！")

if __name__ == "__main__":
    train_model()