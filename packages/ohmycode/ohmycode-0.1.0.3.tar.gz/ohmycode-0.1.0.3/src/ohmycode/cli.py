import logging
import os
import socket
from pathlib import Path

import click
import uvicorn

from .core.tools.project_tools import ProjectTools
from .utils.log_utils import setup_logging


def find_free_port(start_port: int = 8000, max_tries: int = 100) -> int | None:
    """查找可用端口"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    return None


@click.command()
@click.option("--path", "-p", default=".", help="项目路径，默认为当前目录")
@click.option("--log-level", default="INFO", help="日志级别: DEBUG, INFO, WARNING, ERROR")
@click.option("--log-file", help="日志文件路径")
def cli(path: str, log_level: str, log_file: str | None):
    """ohmycode - Python项目分析工具"""
    # 配置日志
    log_path = Path(log_file) if log_file else None
    setup_logging(log_level=log_level, log_file=log_path)
    
    logger = logging.getLogger(__name__)
    
    # 获取项目的绝对路径
    project_root = os.path.abspath(path)
    logger.info(f"开始分析项目: {project_root}")

    # 启动 Web 服务
    port = find_free_port()
    if not port:
        logger.error("无法找到可用端口")
        return

    logger.info(f"Web界面将启动在: http://127.0.0.1:{port}")

    # 在后台启动项目分析
    tools = ProjectTools(project_root=project_root)
    tools.start_monitoring()

    # 设置环境变量
    os.environ["PROJECT_ROOT"] = project_root
    
    try:
        # 启动 Web 服务，关闭热重载和访问日志
        uvicorn.run(
            "ohmycode.web.app:app",
            host="127.0.0.1",
            port=port,
            reload=False,
            access_log=False,
            log_level="error",
        )
    except Exception as e:
        logger.error(f"启动Web服务失败: {e}")
        raise


def main():
    """CLI入口函数"""
    cli()


if __name__ == "__main__":
    main()
