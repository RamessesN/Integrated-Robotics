import threading, cv2
import video_capture

from action_ctrl import *
from robomaster_ultra import robot

def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_camera = ep_robot.camera
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    thread1 = threading.Thread(target = video_capture.video_capture, args = (ep_camera,))  # 帧采集在子线程1
    thread1.start()

    thread2 = threading.Thread(target = arm_ctrl, args = (ep_arm, 0, 500))  # 机械臂控制在子线程2
    thread2.start()

    thread3 = threading.Thread(target = gripper_ctrl, args = (ep_gripper, "close", 40))  # 机械爪控制在子线程3
    thread3.start()

    while True:  # 视频流呈现在主线程
        if video_capture.latest_frame is not None:
            cv2.imshow("on Live", video_capture.latest_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()

if __name__ == '__main__':
    main()