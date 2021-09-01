import logging
import sys


def log_progress(i: int, max_count: int):
    sys.stdout.write('\r')
    sys.stdout.write("{:.1f}%".format(100 / max([1, (max_count - 1)]) * i))
    sys.stdout.flush()


def init_logging():
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")


log_initialized = False


def log_info(s: str):
    global log_initialized
    if not log_initialized:
        init_logging()
    logging.info(s)


def log_error(s: str):
    global log_initialized
    if not log_initialized:
        init_logging()
    logging.error(s)


def log_critical(s: str):
    global log_initialized
    if not log_initialized:
        init_logging()
    logging.critical(s)
    exit(-1)
