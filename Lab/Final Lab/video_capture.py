import cv2
from robomaster_ultra import robot
from robomaster_ultra import camera

def video_capture(ep_camera):
    # Start Video Stream
    ep_camera.start_video_stream(
        display=False,
        resolution=camera.STREAM_720P
    )

    while True:
        img = ep_camera.read_cv2_image()
        if img is None:
            continue

        cv2.imshow("on Live", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_camera = ep_robot.camera

    video_capture(ep_camera)

    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()