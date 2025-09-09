from robomaster_ultra import camera

latest_frame = None

def video_capture(ep_camera):
    global latest_frame
    ep_camera.start_video_stream(display=False, resolution=camera.STREAM_720P)
    while True:
        img = ep_camera.read_cv2_image()
        if img is not None:
            latest_frame = img