# Video Stream Configuration

from . import conn
from . import logger
import threading
import queue
import cv2

# PyAV 用于 H264 解码
import av


class LiveView(object):

    def __init__(self, robot):
        self._robot = robot

        # 视频流相关
        self._video_stream_conn = conn.StreamConnection()
        self._video_frame_queue = queue.Queue(64)
        self._video_decoder_thread = None
        self._video_display_thread = None
        self._video_streaming = False
        self._displaying = False
        self._video_frame_count = 0

        # 音频流相关（暂不实现）
        self._audio_stream_conn = conn.StreamConnection()
        self._audio_frame_queue = queue.Queue(32)
        self._audio_decoder_thread = None
        self._audio_streaming = False
        self._audio_frame_count = 0

    def __del__(self):
        self.stop()

    def stop(self):
        if self._video_streaming:
            self.stop_video_stream()
        if self._audio_streaming:
            self.stop_audio_stream()

    # ---------------- 视频部分 ---------------- #
    def start_video_stream(self, display=True, addr=None, ip_proto="tcp"):
        try:
            logger.info(f"Liveview: connecting to video addr {addr}, proto={ip_proto}")
            self._video_stream_conn.connect(addr, ip_proto)
            self._video_streaming = True

            # 解码线程
            self._video_decoder_thread = threading.Thread(target=self._video_decoder_task)
            self._video_decoder_thread.start()

            # 显示线程
            if display:
                self._video_display_thread = threading.Thread(target=self._video_display_task)
                self._video_display_thread.start()

        except Exception as e:
            logger.error(f"Liveview: start_video_stream exception {e}")
            return False
        return True

    def stop_video_stream(self):
        try:
            self._video_streaming = False
            self._displaying = False

            if self._video_stream_conn:
                self._video_stream_conn.disconnect()

            # 等待线程结束
            if self._video_display_thread:
                self._video_frame_queue.put(None)
                self._video_display_thread.join()
            if self._video_decoder_thread:
                self._video_decoder_thread.join()

            # 清空队列
            while not self._video_frame_queue.empty():
                self._video_frame_queue.get_nowait()

        except Exception as e:
            logger.error(f"LiveView: stop_video_stream exception {e}")
            return False

        logger.info("LiveView: stop_video_stream finished")
        return True

    def read_video_frame(self, timeout=3, strategy="pipeline"):
        try:
            if strategy == "pipeline":
                return self._video_frame_queue.get(timeout=timeout)
            elif strategy == "newest":
                while self._video_frame_queue.qsize() > 1:
                    self._video_frame_queue.get(timeout=timeout)
                return self._video_frame_queue.get(timeout=timeout)
            else:
                logger.warning(f"LiveView: read_video_frame unsupported strategy {strategy}")
                return None
        except queue.Empty:
            return None

    def _video_decoder_task(self):
        self._video_streaming = True
        logger.info("LiveView: _video_decoder_task started")

        # 用 PyAV 打开网络流
        container = av.open(self._video_stream_conn.get_stream_fd(), format='h264', mode='r')

        for packet in container.demux(video=0):
            if not self._video_streaming:
                break
            for frame in packet.decode():
                img = frame.to_ndarray(format='bgr24')
                try:
                    self._video_frame_count += 1
                    if self._video_frame_count % 30 == 1:
                        logger.info(f"LiveView: decoded video frame {self._video_frame_count}")
                    self._video_frame_queue.put(img, timeout=2)
                except queue.Full:
                    logger.warning("LiveView: video frame queue full, dropping frame")
                    continue

        logger.info("LiveView: _video_decoder_task quit")

    def _video_display_task(self, name="RoboMaster LiveView"):
        self._displaying = True
        logger.info("LiveView: _video_display_task started")

        while self._displaying and self._video_streaming:
            frame = self._video_frame_queue.get()
            if frame is None:
                break
            cv2.imshow(name, frame)
            cv2.waitKey(1)

        logger.info("LiveView: _video_display_task quit")

    # ---------------- 音频部分（占位） ---------------- #
    def start_audio_stream(self, addr=None, ip_proto="tcp"):
        logger.warning("LiveView: audio stream not implemented yet")
        return False

    def stop_audio_stream(self):
        self._audio_streaming = False
        return True

    def read_audio_frame(self, timeout=1):
        return None