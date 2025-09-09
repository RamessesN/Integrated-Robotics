import time

def arm_ctrl(ep_arm, dist_front, dist_up):
    ep_arm.move(x = dist_front, y = dist_up).wait_for_completed()

def gripper_ctrl(ep_gripper, status, grip_power):
    if status == "open":
        ep_gripper.open(power = grip_power)
    else:
        ep_gripper.close(power = grip_power)

    time.sleep(1)
    ep_gripper.pause()