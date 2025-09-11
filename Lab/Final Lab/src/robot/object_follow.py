import time
import action_ctrl
import video_capture as vc
from simple_pid import PID

pid_x = PID(0.5, 0.01, 0.1, setpoint = 0)
pid_x.output_limits = (-50, 50)

pid_z = PID(0.4, 0.1, 0.05, setpoint = 13)
pid_z.output_limits = (-30, 30)

def chassis_ctrl(ep_chassis):
    global pid_x, pid_z

    while vc.running:
        if action_ctrl.gripper_closed and action_ctrl.arm_lifted:
            ep_chassis.drive_wheels(0, 0, 0, 0)
            break

        if vc.target_x is None:
            ep_chassis.drive_wheels(0, 0, 0, 0)
            time.sleep(0.05)
            continue

        frame_width = 640
        error_x = vc.target_x - (frame_width // 2)

        current_distance = action_ctrl.latest_distance
        distance = current_distance if current_distance is not None else 8848

        if abs(error_x) < 30 and (10 < distance < 45):
            ep_chassis.drive_wheels(0, 0, 0, 0)
        else:
            turn_speed = pid_x(error_x)
            forward_speed = -pid_z(distance)

            w1 = forward_speed + turn_speed  # 右前
            w2 = forward_speed - turn_speed  # 左前
            w3 = forward_speed + turn_speed  # 右后
            w4 = forward_speed - turn_speed  # 左后

            ep_chassis.drive_wheels(w1, w2, w3, w4)

    ep_chassis.drive_wheels(0, 0, 0, 0)