import logging
import os
from datetime import datetime

from utils.path_tool import get_abs_path

# 日志保存的根目录
LOG_ROOT_DIR = get_abs_path("logs")

# 确保日志目录存在
os.makedirs(LOG_ROOT_DIR, exist_ok=True)

# 日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")

def get_logger(
        name: str="agent",
        console_level: int=logging.INFO,
        file_level: int=logging.DEBUG,
        log_file=None
) -> logging.Logger:
    """
    获取日志记录器
    Args:
        name (str): 日志记录器的名称
        console_level (int): 控制台日志级别
        file_level (int): 文件日志级别
        log_file (str): 日志文件路径，如果为 None，则使用默认路径
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置为最低级别，确保所有日志都能被处理

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 文件处理器
    if log_file is None:
        log_file = os.path.join(LOG_ROOT_DIR, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

# 快捷获取日志器
logger = get_logger()

if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")