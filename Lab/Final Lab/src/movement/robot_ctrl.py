import cv2, time, threading
from robomaster_ultra import robot
from robomaster_ultra import camera

latest_frame = None

def video_capture(ep_camera):
    global latest_frame
    ep_camera.start_video_stream(display=False, resolution=camera.STREAM_720P)
    while True:
        img = ep_camera.read_cv2_image()
        if img is not None:
            latest_frame = img

def arm_ctrl(ep_arm, dist_front, dist_up):
    ep_arm.move(x = dist_front, y = dist_up).wait_for_completed()

def gripper_ctrl(ep_gripper, status, grip_power):
    if status == "open":
        ep_gripper.open(power = grip_power)
    else:
        ep_gripper.close(power = grip_power)

    time.sleep(1)
    ep_gripper.pause()

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type = "ap")

    ep_camera = ep_robot.camera
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    thread1 = threading.Thread(target = video_capture, args = (ep_camera,)) # 帧采集在子线程1
    thread1.start()

    thread2 = threading.Thread(target = arm_ctrl, args = (ep_arm, 0, 1000)) # 机械臂控制在子线程2
    thread2.start()

    thread3 = threading.Thread(target = gripper_ctrl, args = (ep_gripper, "open", 100)) # 机械爪控制在子线程3
    thread3.start()

    while True: # 视频流呈现在主线程
        if latest_frame is not None:
            cv2.imshow("on Live", latest_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()