import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


fh = logging.FileHandler('log.txt', encoding='utf-8', mode='w')
formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')


fh.setFormatter(formatter)
log.addHandler(fh)


def error_log(message):
    log.error(message)


def info_log(message):
    log.info(message)


def warning_log(message):
    log.warning(message)
