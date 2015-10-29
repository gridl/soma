import logging
import sys




ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

root = logging.getLogger('kafka.client')
# root.addHandler(ch)
# root.setLevel(logging.DEBUG)

logger = logging.getLogger('SOMA')
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)
