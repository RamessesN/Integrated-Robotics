import threading

import movement.gripper_ctrl as gc
import movement.chassis_ctrl as cc
import vision.marker_config as mc
import movement.arm_ctrl as ac
import main

def workflow(ep_chassis, ep_gripper, ep_arm):
    main.robot_initialized_event.wait() # 等待机器人初始化完毕

    # 先检测有没有marker-3，如果有的话去靠近其下方的object，并抓取抬起，
    # 然后加一个marker_lost去检测有没有marker-heart，有的话先靠近marker-heart，然后落下机械臂并将机械爪张开

    if mc.object_under_marker("3"):
        cc.object_closed_event.clear()
        ac.arm_aimed_event.clear()
        gc.gripper_closed_event.clear()
        ac.arm_lifted_event.clear()
        cc.marker_closed_event.clear()
        ac.arm_lowered_event.clear()
        gc.gripper_opened_event.clear()

        chassis_thread = threading.Thread(
            target=cc.chassis_ctrl, args=(ep_chassis, "object"), daemon=True
        )
        chassis_thread.start()

        arm_thread = threading.Thread(
            target=ac.arm_aim, args=(ep_arm,), daemon=True
        )
        arm_thread.start()

        cc.object_closed_event.wait() # 等待靠近物体
        ac.arm_aimed_event.wait() # 等待机械臂对齐

        gc.gripper_ctrl(ep_gripper, "close")
        gc.gripper_closed_event.wait() # 等待机械爪闭合
        ac.arm_ctrl(ep_arm, "lift")
        ac.arm_lifted_event.wait() # 等待机械臂抬起

        cc.search_marker(ep_chassis, "heart")
        mc.target_info = "heart"
        chassis_thread2 = threading.Thread(
            target = cc.chassis_ctrl, args = (ep_chassis, "marker"), daemon = True
        )
        chassis_thread2.start()
        cc.marker_closed_event.wait() # 等待靠近marker

        ac.arm_ctrl(ep_arm, "lower")
        ac.arm_lowered_event.wait() # 等待机械臂放下
        gc.gripper_ctrl(ep_gripper, "open")
        gc.gripper_opened_event.wait() # 等待机械爪张开

        cc.object_closed_event.clear()
        ac.arm_aimed_event.clear()
        cc.marker_closed_event.clear()