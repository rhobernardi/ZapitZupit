import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

logging.basicConfig(filename=f"./log/bot.log", level=INFO, format='%(asctime)s %(levelname)7s %(funcname)20s(): %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def log(string: str, funcname="main", line="", type=INFO) -> str:
    log = ""
    if type == CRITICAL:
        log = logging.critical(string, extra={'funcname': funcname})
    if type == ERROR:
        log = logging.error(string, extra={'funcname': funcname})
    if type == WARNING:
        log = logging.warning(string, extra={'funcname': funcname})
    if type == INFO:
        log = logging.info(string, extra={'funcname': funcname})
    if type == DEBUG:
        log = logging.debug(string, extra={'funcname': funcname})
    return