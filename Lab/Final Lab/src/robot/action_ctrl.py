import time
from collections import deque

gripper_closed = False
arm_lifted = False
latest_distance: float | None = None

def arm_ctrl(ep_arm):
    """
    Controls the robot arm
    :param ep_arm: the object of the robot arm
    """
    global gripper_closed, arm_lifted

    while not arm_lifted:
        if gripper_closed:
            ep_arm.move(x = 50, y = 150).wait_for_completed()
            arm_lifted = True
        time.sleep(0.05)

def gripper_ctrl(ep_gripper):
    """
    Controls the robot gripper
    :param ep_gripper: the object of the robot gripper
    """
    global gripper_closed

    ep_gripper.sub_status(freq = 5, callback = sub_data_handler_gripper)

    dist_queue = deque(maxlen = 15) # 连续帧记录

    while not gripper_closed:
        if latest_distance is not None:
            valid_distance = latest_distance if latest_distance >= 13 else None

            if valid_distance is not None:
                dist_queue.append(valid_distance < 46)
                if len(dist_queue) == 15 and all(dist_queue): # 连续15帧距离数据都小于阈值时触发
                    ep_gripper.close()
                    time.sleep(3)
                    gripper_closed = True

        time.sleep(0.05)

def sub_data_handler_gripper(sub_info):
    """
    Callback function to receive the data from the gripper
    :param sub_info: the status of the gripper
    """
    global gripper_status
    gripper_status = sub_info

def get_distance(ep_sensor):
    """
    Subscribe the distance information from the distance sensor
    :param ep_sensor: the object of the distance sensor
    """
    ep_sensor.sub_distance(freq = 5, callback = sub_data_handler_distance)
    while True:
        time.sleep(0.1)

def sub_data_handler_distance(sub_info):
    """
    Callback function to receive the data from the distance sensor
    :param sub_info: the distance info from the distance sensor
    """
    global latest_distance
    latest_distance = sub_info[0]