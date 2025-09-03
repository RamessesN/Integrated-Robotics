import sys
if sys.version_info < (3, 6, 5) or sys.version_info >= (3, 11, 0):
    sys.exit('RoboMaster-SDK-Ultra requires Python 3.6.5 to Python 3.11.0')

import logging
import time

logger_name = "SDK-Ultra"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.ERROR)

fmt = "%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d %(message)s"
formatter = logging.Formatter(fmt)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)


def enable_logging_to_file():
    logger.setLevel(logging.INFO)
    filename = "RoboMaster-SDK-Ultra_{0}_log.txt".format(
        time.strftime("%Y%m%d%H%M%S", time.localtime())
    )
    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# Open API
__all__ = ['logger', 'protocol', 'config', 'version', 'action', 'conn', 'client', 'module',
           'robot', 'gimbal', 'chassis', 'gripper', 'blaster', 'camera', 'media', 'flight',
           'led', 'robotic_arm', 'vision', 'sensor', 'ai_module']
