import contextlib
import copy
import json
import logging
import platform
import sys
from enum import Enum
from pathlib import Path
from typing import Any

from ..web.config_types import ToolOptionType


def get_python_version() -> str:
    """获取当前 Python 版本

    返回两种格式:
    1. 用于 mypy 的格式: X.Y (例如: 3.12)
    2. 用于 ruff 的格式: pyXYZ (例如: py312)
    """
    try:
        # 获取完整的 Python 版本号 (例如: 3.12.5)
        full_version = platform.python_version()
        # 只取主版本号和次版本号 (例如: 3.12)
        major_minor = ".".join(full_version.split(".")[:2])
        return major_minor
    except Exception as e:
        print(f"获取 Python 版本失败: {e}")
        return "3.8"  # 默认返回 3.8


def get_platform() -> str:
    """获取当前操作系统平台

    返回值:
    - "linux": Linux系统
    - "darwin": macOS系统
    - "win32": Windows系统
    """
    return sys.platform


class EnumEncoder(json.JSONEncoder):
    """用于序列化枚举类型的 JSON 编码器"""

    def default(self, obj):
        if isinstance(obj, Enum | ToolOptionType):
            return str(obj)
        return super().default(obj)


class ConfigManager:
    """配置管理器"""

    def __init__(self, root_path: str):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"初始化配置管理器，项目根目录: {root_path}")
        self.project_root = Path(root_path)
        self.config_dir = self.project_root / ".ohmyprompt"
        self.config_file = self.config_dir / "config.json"
        self.history_path = self.config_dir / "history"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.history_path.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> dict[str, Any] | None:
        """加载配置"""
        try:
            if not self.config_file.exists():
                return None

            config = json.loads(self.config_file.read_text())
            
            # 如果配置为空，返回 None
            if not config:
                return None

            # 转换字符串回枚举类型
            def convert_enums(obj: Any) -> Any:
                if isinstance(obj, dict):
                    if "type" in obj and isinstance(obj["type"], str):
                        with contextlib.suppress(ValueError):
                            obj["type"] = ToolOptionType(obj["type"])
                    return {k: convert_enums(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_enums(item) for item in obj]
                return obj

            return convert_enums(config)
        except Exception as e:
            self.logger.error(f"加载配置出错: {e}")
            return None

    def save_config(self, config: dict[str, Any]) -> None:
        """保存配置"""
        try:
            # 深拷贝配置以避免修改原始数据
            config_copy = copy.deepcopy(config)
            
            # 递归转换所有的 set 为 list
            def convert_sets(obj: Any) -> Any:
                if isinstance(obj, set):
                    return list(obj)
                elif isinstance(obj, dict):
                    return {k: convert_sets(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_sets(item) for item in obj]
                elif isinstance(obj, Enum | ToolOptionType):
                    return str(obj)
                return obj
            
            config_copy = convert_sets(config_copy)
            
            config_str = json.dumps(
                config_copy,
                indent=2,
                cls=EnumEncoder,
                ensure_ascii=False
            )
            self.config_file.write_text(config_str, encoding="utf-8")
            self.logger.debug(f"配置已保存到: {self.config_file}")
        except Exception as e:
            self.logger.error(f"保存配置出错: {e}")
            raise

    def get_history_path(self) -> Path:
        """获取历史记录目录"""
        return self.history_path
