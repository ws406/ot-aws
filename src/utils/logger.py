import logging
import psutil
import os


class OtLogger:
    def __init__(self, log_file_path):

        logger = logging.getLogger('ot-logger')
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=log_file_path,
                            filemode='w'
                            )

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

    def exception (self, msg, ps_info = False):
        output = msg if ps_info is False else (msg + ' - ' + str (psutil.virtual_memory ()))
        self.ot_logger.exception(output)

    def log(self, msg, ps_info = False):
        output = msg if ps_info is False else (msg + ' - ' + str (psutil.virtual_memory ()))
        self.ot_logger.info(output)
