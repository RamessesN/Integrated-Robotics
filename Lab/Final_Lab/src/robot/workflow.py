import Lab.Final_Lab.src.robot.movement.gripper_ctrl as gc
import Lab.Final_Lab.src.robot.movement.chassis_ctrl as cc
import Lab.Final_Lab.src.robot.vision.marker_config as mc
import Lab.Final_Lab.src.robot.vision.video_capture as vc
import Lab.Final_Lab.src.robot.other.distance_sub as ds
import Lab.Final_Lab.src.robot.movement.arm_ctrl as ac

import time, threading

states = {
    "Object_Searching": 0,      # 寻找marker下的物体
    "Object_Approaching": 1,    # 靠近物体
    "Object_Grabbing": 2,       # 抓住物体
    "Object_Lifting": 3,        # 抬起物体
    "Marker_Searching": 4,      # 寻找标签
    "Marker_Approaching": 5,    # 靠近标签
    "Object_Lowering": 6,       # 放下物体
    "Object_Releasing": 7,      # 松开物体
    "Task_Complete": 8          # 任务结束
}

def workflow(current_state, ep_chassis, ep_gripper, ep_arm):
    if current_state == states["Object_Searching"]:
        mc.target_info = "3"
        found = cc.search_marker(ep_chassis, "3")
        if found:
            if mc.object_under_marker("3"):
                return states["Object_Approaching"]
        return states["Object_Searching"]

    elif current_state == states["Object_Approaching"]:
        if ds.target_closed_event.is_set() and ac.arm_aimed_event.is_set():
            ds.target_closed_event.clear()
            ac.arm_aimed_event.clear()
            ac.stop_aimed_event.set() # `停止机械臂对齐`事件设置
            return states["Object_Grabbing"]
        return states["Object_Approaching"]

    elif current_state == states["Object_Grabbing"]:
        gc.gripper_closed_event.clear()
        gc.gripper_ctrl(ep_gripper, "close")
        gc.gripper_closed_event.wait()
        return states["Object_Lifting"]

    elif current_state == states["Object_Lifting"]:
        ac.arm_lifted_event.clear()
        ac.arm_ctrl(ep_arm, "lift")
        ac.arm_lifted_event.wait()
        return states["Marker_Searching"]

    elif current_state == states["Marker_Searching"]:
        mc.marker_info = "heart"
        found = cc.search_marker(ep_chassis, "heart")
        if found:
            return states["Marker_Approaching"]
        return states["Marker_Searching"]

    elif current_state == states["Marker_Approaching"]:
        if cc.marker_closed_event.is_set():
            cc.marker_closed_event.clear()
            return states["Object_Lowering"]
        return states["Marker_Approaching"]

    elif current_state == states["Object_Lowering"]:
        ac.arm_lowered_event.clear()
        ac.arm_ctrl(ep_arm, "lower")
        ac.arm_lowered_event.wait()
        return states["Object_Releasing"]

    elif current_state == states["Object_Releasing"]:
        gc.gripper_opened_event.clear()
        gc.gripper_ctrl(ep_gripper, "open")
        gc.gripper_opened_event.wait()
        return states["Task_Complete"]

    return current_state


def action_ctrl(ep_chassis, ep_arm, ep_gripper):
    current_state = states["Object_Searching"]

    while vc.running and current_state != states["Task_Complete"]:
        if current_state == states["Object_Approaching"]:
            ds.target_closed_event.clear()
            ac.arm_aimed_event.clear()
            ac.stop_aimed_event.clear()

            threading.Thread(
                target = cc.chassis_ctrl, args = (ep_chassis, "object")
            ).start()
            threading.Thread(
                target = ac.arm_ctrl, args = (ep_arm, "aim")
            ).start()

            next_state = states["Object_Grabbing"]
        elif current_state == states["Marker_Approaching"]:
            cc.marker_closed_event.clear()

            cc.chassis_ctrl(ep_chassis, "marker")

            next_state = states["Object_Lowering"]
        else:
            next_state = workflow(current_state, ep_chassis, ep_gripper, ep_arm)

        current_state = next_state
        time.sleep(0.1)