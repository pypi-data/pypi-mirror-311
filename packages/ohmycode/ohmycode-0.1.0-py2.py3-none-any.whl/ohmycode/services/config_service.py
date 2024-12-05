import logging
from typing import Any, ClassVar, cast

from ..web.config import DEFAULT_CONFIG, Config, ExcludePatterns, Tools
from ..web.config.manager import ConfigManagerSingleton

logger = logging.getLogger(__name__)


class ConfigService:
    """配置服务单例类"""

    _instance: ClassVar["ConfigService | None"] = None
    _initialized = False

    def __init__(self):
        """私有构造函数"""
        if not ConfigService._initialized:
            raise RuntimeError("请使用 initialize() 方法初始化配置服务")
        self.logger = logging.getLogger(__name__)
        self._config: Config = {}
        self._config_manager = ConfigManagerSingleton.get_instance()

    @classmethod
    def get_instance(cls) -> "ConfigService":
        """获取配置服务实例"""
        if not cls._instance:
            raise RuntimeError("配置服务未初始化")
        return cls._instance

    @classmethod
    def initialize(cls, project_root: str) -> None:
        """初始化配置服务"""
        if cls._initialized:
            return

        # 初始化 Web 配置管理器
        ConfigManagerSingleton.init(project_root)
        
        cls._instance = cls.__new__(cls)
        cls._instance.logger = logging.getLogger(__name__)
        cls._instance._config_manager = ConfigManagerSingleton.get_instance()
        cls._instance._load_config()
        cls._initialized = True

    def _load_config(self) -> None:
        """加载配置"""
        if not self._config_manager:
            raise RuntimeError("配置管理器未初始化")

        try:
            config = self._config_manager.load_config()
            if not config:
                self.logger.info("未找到现有配置，使用默认配置")
                self._config = cast(Config, DEFAULT_CONFIG.copy())
                self._config_manager.save_config(self._config)
            else:
                self.logger.debug("已加载现有配置")
                self._config = cast(Config, config)
        except Exception as e:
            self.logger.error(f"加载配置失败: {e}")
            raise

    def get_config(self) -> dict[str, Any]:
        """获取完整配置"""
        return self._config

    def get_tool_config(self, tool_name: str) -> dict[str, Any]:
        """获取指定工具的配置"""
        tools = cast(Tools, self._config.get("tools", {}))
        result = tools.get(tool_name, {})
        return cast(dict[str, Any], result)

    def get_exclude_patterns(self) -> dict[str, set[str]]:
        """获取排除模式"""
        patterns = cast(ExcludePatterns, self._config.get("exclude_patterns", DEFAULT_CONFIG["exclude_patterns"]))
        return {
            "directories": set(patterns["directories"]),
            "files": set(patterns["files"])
        }

    def get_update_interval(self) -> int:
        """获取更新间隔"""
        return cast(int, self._config.get("update_interval", DEFAULT_CONFIG["update_interval"]))

    def get_dependencies(self) -> dict[str, str]:
        """获取项目依赖"""
        try:
            with open("pyproject.toml") as f:
                import toml

                pyproject = toml.load(f)
                return pyproject.get("project", {}).get("dependencies", {})
        except Exception:
            try:
                with open("requirements.txt") as f:
                    deps = {}
                    for line in f:
                        if line.strip() and not line.startswith("#"):
                            name = line.split("==")[0].strip()
                            version = (
                                line.split("==")[1].strip()
                                if "==" in line
                                else "latest"
                            )
                            deps[name] = version
                    return deps
            except Exception:
                return {}

    def get_project_info(self) -> dict[str, Any]:
        """获取项目信息"""
        try:
            # 尝试从 pyproject.toml 读取
            with open("pyproject.toml") as f:
                import toml

                pyproject = toml.load(f)
                project = pyproject.get("project", {})
                return {
                    "description": project.get("description", ""),
                    "version": project.get("version", ""),
                    "features": [],  # 这些信息需要手动维护
                    "modules": {},
                    "components": {},
                    "examples": "",
                    "notes": "",
                    "contribution": "",
                    "versions": [],
                }
        except Exception:
            # 如果没有 pyproject.toml，返回默认值
            return {
                "description": "",
                "version": "",
                "features": [],
                "modules": {},
                "components": {},
                "examples": "",
                "notes": "",
                "contribution": "",
                "versions": [],
            }

    def save_config(self) -> None:
        """保存配置"""
        if self._config_manager:
            # 转换 set 为 list
            config_copy = cast(Config, self._config.copy())
            if "exclude_patterns" in config_copy:
                patterns = cast(ExcludePatterns, config_copy["exclude_patterns"])
                patterns["directories"] = list(patterns["directories"])
                patterns["files"] = list(patterns["files"])
            self._config_manager.save_config(config_copy)
