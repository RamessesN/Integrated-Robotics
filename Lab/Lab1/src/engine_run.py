import cv2
from ultralytics import YOLO

def load_trt_model():
    print("Loading TensorRT Engine...")

    # Load TensorRT engine
    model = YOLO("./mlmodel/engine/combined_v1.engine")

    return model

def detect_from_video(model, video_path="./video/input_360p.mp4", output_path="./video/output_trt.mp4"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {video_path}")
        return

    # Video config
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video resolution: {width}x{height}, FPS: {fps_input}")

    prev_time = cv2.getTickCount()

    win_name = "TensorRT Inference"
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)

    screen_width = 1512
    screen_height = 982
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    cv2.moveWindow(win_name, int(x), int(y))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps_input if fps_input > 0 else 30, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to read frame")
            break

        results = model.predict(frame, conf=0.25, device=0, verbose=False)
        annotated_frame = results[0].plot()

        current_time = cv2.getTickCount()
        fps = cv2.getTickFrequency() / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(annotated_frame, f"Res: {width}x{height}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow(win_name, annotated_frame)
        out.write(annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Saved result video to: {output_path}")


if __name__ == "__main__":
    model = load_trt_model()
    detect_from_video(
        model,
        "./video/input_360p.mp4",
        "./video/output_trt.mp4"
    )