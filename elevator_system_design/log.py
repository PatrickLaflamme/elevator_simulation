import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
root = logging.getLogger()
root.setLevel(logging.INFO)
logger = logging.getLogger("elevator_controller")
