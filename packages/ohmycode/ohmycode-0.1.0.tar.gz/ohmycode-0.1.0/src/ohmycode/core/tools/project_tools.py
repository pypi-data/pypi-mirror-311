import logging
import os
import threading
import time
from typing import Any

from ...services.config_service import ConfigService
from ...utils.file_utils import get_file_structure
from ...utils.report_manager import ReportManager
from .base import BaseTool
from .mypy_tool import MypyTool
from .radon_tool import RadonTool
from .ruff_tool import RuffTool


class ToolFactory:
    """工具工厂类"""

    _tools: dict[str, type[BaseTool]] = {
        "mypy": MypyTool,
        "ruff": RuffTool,
        "radon": RadonTool,
    }

    @classmethod
    def create_tool(cls, tool_name: str, project_root: str) -> BaseTool:
        """创建工具实例"""
        tool_class = cls._tools.get(tool_name)
        if not tool_class:
            raise ValueError(f"不支持的工具类型: {tool_name}")

        return tool_class(project_root)


class ProjectTools:
    """项目分析工具主类"""

    def __init__(
        self,
        project_root: str = ".",
        update_interval: int = 3600,
        exclude_patterns: dict[str, set[str]] | None = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.info("初始化项目分析工具...")
        
        self.project_root = os.path.abspath(project_root)
        self.logger.debug(f"项目根目录: {self.project_root}")
        
        # 初始化配置服务
        try:
            ConfigService.initialize(self.project_root)
            self.config_service = ConfigService.get_instance()
            self.logger.info("配置服务初始化成功")
        except Exception as e:
            self.logger.error(f"配置服务初始化失败: {e}")
            raise
        
        self.running = False
        self.update_interval = self.config_service.get_update_interval()
        self.logger.debug(f"更新间隔: {self.update_interval}秒")

        # 获取排除模式
        self.exclude_patterns = self.config_service.get_exclude_patterns()
        if exclude_patterns:
            self.exclude_patterns["directories"].update(exclude_patterns.get("directories", set()))
            self.exclude_patterns["files"].update(exclude_patterns.get("files", set()))
        self.logger.debug(f"排除模式: {self.exclude_patterns}")

        # 使用 create 类方法创建 ReportManager
        try:
            self.history_manager = ReportManager.create()
            self.logger.info("报告管理器初始化成功")
        except Exception as e:
            self.logger.error(f"报告管理器初始化失败: {e}")
            raise

    def start_monitoring(self) -> None:
        """启动持续监控"""
        self.running = True
        self.logger.info("启动项目监控...")

        def monitoring_loop() -> None:
            while self.running:
                try:
                    self.logger.info(f"开始新一轮项目分析: {self.project_root}")
                    self._run_analysis()
                    self.logger.info(f"分析完成，等待 {self.update_interval} 秒后进行下一轮分析")

                    for _ in range(self.update_interval):
                        if not self.running:
                            self.logger.info("监控已停止")
                            break
                        time.sleep(1)

                except Exception as e:
                    self.logger.error(f"分析过程中出错: {e}", exc_info=True)
                    self.logger.info("60秒后重试...")
                    time.sleep(60)

        monitor_thread = threading.Thread(target=monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        self.logger.info("监控线程已启动")

    def _run_analysis(self) -> dict:
        """运行一次完整的项目分析"""
        self.logger.info("开始新一轮项目分析...")
        
        try:
            config = self.config_service.get_config()
            enabled_tools = config.get("tools", {})
            enabled_tool_names = [name for name, tool in enabled_tools.items() if tool.get("enabled", False)]
            self.logger.info(f"已启用的工具: {enabled_tool_names}")

            try:
                self.logger.debug("分析项目结构...")
                structure = get_file_structure(
                    self.project_root,
                    exclude_dirs=self.exclude_patterns["directories"],
                    ignore_patterns=list(self.exclude_patterns["files"]),
                )
                self.logger.debug("项目结构分析完成")
            except Exception as e:
                self.logger.error(f"获取文件结构失败: {e}")
                structure = {"error": f"获取文件结构失败: {str(e)}"}

            results = {}
            for tool_name, tool_config in enabled_tools.items():
                if tool_config.get("enabled", False):
                    self.logger.info(f"运行工具: {tool_name}")
                    try:
                        tool = ToolFactory.create_tool(tool_name, self.project_root)
                        results[tool_name] = tool.run()
                        self.logger.debug(f"{tool_name} 分析完成")
                    except Exception as e:
                        self.logger.error(f"{tool_name} 运行失败: {e}")
                        results[tool_name] = {
                            "status": "error",
                            "message": f"工具运行失败: {str(e)}"
                        }

            analysis_results = {
                "structure": structure,
                "type_check": results.get("mypy", {}),
                "ruff_check": results.get("ruff", {}),
                "complexity": results.get("radon", {}),
                "timestamp": time.time(),
            }

            self.logger.info("保存分析结果...")
            self.history_manager.save_results(analysis_results)
            self.logger.info("分析完成")

            return analysis_results

        except Exception as e:
            self.logger.error(f"项目分析过程中发生错误: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"分析过程中出错: {str(e)}",
                "timestamp": time.time(),
                "structure": {},
                "type_check": {"status": "error", "message": str(e)},
                "complexity": {"status": "error", "message": str(e)},
            }

    def run_analysis(self) -> dict[str, Any]:
        """运行所有工具分析"""
        results = {}
        enabled_tools = self.config_service.get_config().get("tools", {})
        
        for tool_name, tool_config in enabled_tools.items():
            if tool_config.get("enabled", False):
                try:
                    tool = ToolFactory.create_tool(tool_name, self.project_root)
                    if tool.check_installation():
                        results[tool_name] = tool.run()
                    else:
                        results[tool_name] = {
                            "status": "error",
                            "error": f"{tool_name} 工具未安装"
                        }
                except Exception as e:
                    results[tool_name] = {
                        "status": "error",
                        "error": f"{tool_name} 工具运行失败: {str(e)}"
                    }
        return results
