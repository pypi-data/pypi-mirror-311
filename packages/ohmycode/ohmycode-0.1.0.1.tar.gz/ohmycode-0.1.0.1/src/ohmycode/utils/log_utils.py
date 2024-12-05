import logging
import sys
from pathlib import Path


def setup_logging(
    log_level: str = "INFO",
    log_file: Path | None = None,
    module_name: str = "ohmyprompt"
) -> None:
    """配置日志系统
    
    Args:
        log_level: 日志级别
        log_file: 日志文件路径
        module_name: 模块名称
    """
    # 创建logger
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器(如果指定了日志文件)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler) 