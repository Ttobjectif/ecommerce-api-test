import logging
import os
from datetime import datetime


def get_logger(name="AutoTest"):
    # 1. 确保 logs 文件夹存在（如果不存在就自动创建一个）
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. 生成按日期命名的日志文件名
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"test_{current_date}.log")

    # 3. 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 设置日志级别为 INFO

    # 防止重复添加 Handler
    if not logger.handlers:
        # 4. 定义日志格式：时间 - 级别 - 哪个文件报的 - 具体信息
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

        # 5. 把日志写到文件里
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 6. 同时也把日志打印到控制台（黑框）里
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# 生成一个全局可用的 logger 对象
log = get_logger()
