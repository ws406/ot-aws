import logging
import psutil

class OtLogger:
    def __init__(self):
        logger = logging.getLogger('ot')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        self.ot_logger = logger

    def debug(self, msg, ps_info = False):
        output = msg if ps_info is False else (msg + ' - ' + str(psutil.virtual_memory()))
        self.ot_logger.debug(output)