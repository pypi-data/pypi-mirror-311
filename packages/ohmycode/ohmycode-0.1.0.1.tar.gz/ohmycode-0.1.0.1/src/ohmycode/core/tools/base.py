import logging
from abc import ABC, abstractmethod
from typing import Any

from ...services.config_service import ConfigService

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """工具基类"""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.config_service = ConfigService.get_instance()

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """运行工具分析"""
        pass

    @abstractmethod
    def check_installation(self) -> bool:
        """检查工具是否已安装"""
        pass

    def build_command(self) -> str:
        """构建工具命令"""
        try:
            tool_name = self.get_tool_name()
            tool_config = self.config_service.get_tool_config(tool_name)
            logger = logging.getLogger(__name__)
            
            if "command" not in tool_config:
                raise ValueError(f"工具 {tool_name} 缺少命令配置")
            
            base_command = tool_config["command"]
            options = []

            # 处理选项
            if "options" in tool_config:
                for option_id, option in tool_config["options"].items():
                    # 跳过 paths 选项，因为它是特殊处理的
                    if option_id == "paths":
                        continue

                    if not isinstance(option, dict) or "value" not in option:
                        continue

                    value = option.get("value", {})
                    if not isinstance(value, dict) or "value" not in value:
                        continue

                    actual_value = value.get("value")

                    # 跳过空值参数
                    if actual_value is None or actual_value == "":
                        continue

                    # 根据工具特殊处理
                    if tool_name == "mypy":
                        if isinstance(actual_value, bool) and actual_value:
                            options.append(f"--{option_id}")
                        elif isinstance(actual_value, str | int | float) and actual_value:
                            options.extend([f"--{option_id}", str(actual_value)])
                    elif tool_name == "ruff":
                        if isinstance(actual_value, bool) and actual_value:
                            options.append(f"--{option_id}")
                        elif isinstance(actual_value, str | int | float) and actual_value:
                            options.extend([f"--{option_id}", str(actual_value)])
                        elif isinstance(actual_value, list | tuple) and actual_value:
                            options.extend([f"--{option_id}", ",".join(str(v) for v in actual_value)])
                    elif tool_name == "radon":
                        if isinstance(actual_value, bool) and actual_value:
                            options.append(f"--{option_id}")
                        elif isinstance(actual_value, str | int | float) and actual_value:
                            options.extend([f"--{option_id}", str(actual_value)])

            # 构建完整命令
            cmd_parts = [base_command]
            cmd_parts.extend(options)
            
            # 添加源代码路径
            paths = tool_config.get("options", {}).get("paths", {}).get("value", {}).get("value", "src/")
            cmd_parts.append(paths)

            cmd = " ".join(cmd_parts)
            logger.debug(f"执行命令: {cmd}")
            return cmd
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"构建命令失败: {e}")
            raise ValueError(f"构建命令失败: {e}") from e  # 使用 from e 来保留原始异常

    @abstractmethod
    def get_tool_name(self) -> str:
        """获取工具名称"""
        pass
