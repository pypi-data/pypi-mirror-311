import logging
from typing import Any

from ...utils.shell_utils import execute_bash
from .base import BaseTool


class RuffTool(BaseTool):
    def get_tool_name(self) -> str:
        return "ruff"

    def check_installation(self) -> bool:
        cmd = f"cd {self.project_root} && rye run ruff --version"
        stdout, stderr, code = execute_bash(cmd)
        return code == 0

    def run(self) -> dict[str, Any]:
        """运行 Ruff 代码检查"""
        logger = logging.getLogger(__name__)
        logger.info("开始运行 Ruff 代码检查...")
        
        if not self.check_installation():
            logger.warning("Ruff 未安装，跳过检查")
            return {"status": "skipped", "message": "ruff 未安装"}

        try:
            cmd = f"cd {self.project_root} && rye run {self.build_command()}"
            logger.debug(f"执行命令: {cmd}")
            
            stdout, stderr, code = execute_bash(cmd)
            output = "\n".join(filter(None, [stdout.strip(), stderr.strip()]))
            
            if code == 0:
                logger.info("Ruff 检查完成: 未发现问题")
            else:
                logger.warning("Ruff 检查完成: 发现代码问题")
                logger.debug(f"详细输出:\n{output}")
                
            return {
                "status": "ok" if code == 0 else "error",
                "output": output,
                "message": "代码检查完成" if code == 0 else "代码检查发现问题",
            }
        except Exception as e:
            logger.error(f"Ruff 检查过程中出错: {e}", exc_info=True)
            return {
                "status": "error",
                "output": str(e),
                "message": f"代码检查失败: {e}",
            }
