import logging
from typing import Any

from ...utils.shell_utils import execute_bash
from .base import BaseTool


class MypyTool(BaseTool):
    def get_tool_name(self) -> str:
        return "mypy"

    def check_installation(self) -> bool:
        logger = logging.getLogger(__name__)
        cmd = f"cd {self.project_root} && rye run mypy --version"
        stdout, stderr, code = execute_bash(cmd)
        
        if code == 0:
            logger.debug(f"Mypy 已安装: {stdout.strip()}")
        else:
            logger.warning(f"Mypy 未安装或安装异常: {stderr.strip()}")
            
        return code == 0

    def run(self) -> dict[str, Any]:
        """运行类型检查"""
        logger = logging.getLogger(__name__)
        logger.info("开始运行 Mypy 类型检查...")
        
        if not self.check_installation():
            logger.warning("Mypy 未安装，跳过检查")
            return {"status": "skipped", "message": "mypy 未安装"}

        try:
            cmd = f"cd {self.project_root} && rye run {self.build_command()}"
            logger.debug(f"执行命令: {cmd}")
            
            stdout, stderr, code = execute_bash(cmd)
            output = stdout.strip() or stderr.strip()
            
            if code == 0:
                logger.info("Mypy 类型检查完成: 未发现问题")
            else:
                logger.warning("Mypy 类型检查完成: 发现类型问题")
                logger.debug(f"详细输出:\n{output}")
                
            return {
                "status": "ok" if code == 0 else "error",
                "output": output,
                "message": "类型检查完成" if code == 0 else "类型检查发现错误",
            }
        except Exception as e:
            logger.error(f"Mypy 类型检查过程中出错: {e}", exc_info=True)
            return {
                "status": "error",
                "output": str(e),
                "message": f"类型检查失败: {e}",
            }
