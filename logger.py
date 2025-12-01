import logging
import os
from datetime import datetime


def create_logger():
    # 创建 logs 目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件名
    log_file = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d}.log")

    # 创建 logger
    logger = logging.getLogger("ui_test")
    logger.setLevel(logging.INFO)

    # 防止重复添加 handler
    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        sh = logging.StreamHandler()

        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        )

        fh.setFormatter(fmt)
        sh.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger
