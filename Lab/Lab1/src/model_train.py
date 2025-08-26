import os
from ultralytics import YOLO
import cv2
import torch

# -----------------------------
# 1️⃣ 设备选择
# -----------------------------
device = "mps" if torch.backends.mps.is_available() else "cpu"
print("使用设备:", device)

# -----------------------------
# 2️⃣ 数据集路径
# -----------------------------
dataset_path = "../dataset/mouse"
data_yaml = os.path.join(dataset_path, "data.yaml")

# -----------------------------
# 3️⃣ 初始化模型
# -----------------------------
model = YOLO("yolov8n.pt")  # 官方预训练权重

# -----------------------------
# 4️⃣ 训练模型
# -----------------------------
print("开始训练模型...")
train_results = model.train(
    data=data_yaml,
    epochs=100,
    imgsz=640,
    batch=36,
    name="mouse_model",
    device=device  # 指定使用 MPS GPU
)
print("训练完成!")

# -----------------------------
# 5️⃣ 验证模型
# -----------------------------
best_model_path = os.path.join("runs", "detect", "mouse_model", "weights", "best.pt")
print("开始验证模型...")
model = YOLO(best_model_path)
val_results = model.val(data=data_yaml, device=device)
print("验证完成!")

# -----------------------------
# 6️⃣ 实时视频检测
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开视频流")
    exit()

print("开始实时检测，按 q 键退出...")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 指定 device 使用 MPS
    results = model.predict(frame, conf=0.25, verbose=False, device=device)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 获取框坐标
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]

            # 绘制矩形框和标签
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{cls_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Mouse Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()