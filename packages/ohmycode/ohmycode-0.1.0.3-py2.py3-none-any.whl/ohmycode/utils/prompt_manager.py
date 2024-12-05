import logging
from pathlib import Path

from ..services.config_service import ConfigService
from .file_utils import get_file_structure

logger = logging.getLogger(__name__)


class PromptManager:
    """Prompt文档生成器"""

    def __init__(self):
        """初始化Prompt文档生成器"""
        self.config_service = ConfigService.get_instance()
        
        # 获取prompt文档模板
        template_path = (
            Path(__file__).parent.parent / "templates" / "prompt_template.md"
        )
        if not template_path.exists():
            logger.warning(f"Prompt模板文件不存在: {template_path}")
        self.template = template_path.read_text() if template_path.exists() else ""

    def generate_prompt_doc(self, project_root: str) -> str:
        """生成Prompt文档
        
        Args:
            project_root: 项目根目录
                
        Returns:
            str: 生成的prompt文档内容
        """
        try:
            # 获取项目结构
            structure = get_file_structure(project_root)
            
            # 从配置服务获取项目信息
            project_info = self.config_service.get_project_info()
            
            # 准备文档内容
            doc_content = {
                "project_description": project_info.get("description", ""),
                
                # 架构概览
                "module_organization": self._analyze_module_organization(structure),
                "key_components": self._format_components(project_info.get("components", {})),
                "dependencies": self._format_dependencies(),
                
                # 代码结构分析
                "project_structure": self._format_structure(structure),
                "structure_evaluation": self._evaluate_structure(structure),
                "organization_suggestions": self._suggest_organization(structure),
                
                # 代码质量分析
                "ruff_status": "pending",
                "ruff_results": "",
                "type_check_status": "pending",
                "type_check_results": "",
                "cyclomatic_complexity": "",
                "maintainability_index": "",
                
                # 改进建议
                "quality_improvements": "待分析",
                "type_safety_improvements": "待分析",
                "complexity_improvements": "待分析",
                "best_practices": self._get_best_practices(),
                
                # 其他信息
                "usage_examples": project_info.get("examples", ""),
                "notes": project_info.get("notes", ""),
                "contribution_guidelines": project_info.get("contribution", ""),
                "version_history": self._format_versions(project_info.get("versions", [])),
            }
            
            # 使用模板生成文档
            return self.template.format(**doc_content)
            
        except Exception as e:
            logger.error(f"生成Prompt文档时发生错误: {e}")
            raise

    def _analyze_module_organization(self, structure: dict) -> str:
        """分析模块组织"""
        try:
            modules = []
            for name, value in structure.items():
                if isinstance(value, dict) and not name.startswith('.'):
                    modules.append(f"- {name}/: {self._guess_module_purpose(name, value)}")
            return "\n".join(modules) if modules else "项目模块分析待完成"
        except Exception:
            return "模块组织分析失败"

    def _guess_module_purpose(self, name: str, structure: dict) -> str:
        """推测模块用途"""
        common_patterns = {
            "core": "核心功能模块",
            "utils": "工具函数模块",
            "services": "服务层模块",
            "models": "数据模型模块",
            "views": "视图层模块",
            "controllers": "控制器模块",
            "tests": "测试模块",
            "config": "配置模块",
            "api": "API接口模块",
            "web": "Web相关模块",
            "templates": "模板文件模块",
            "static": "静态资源模块",
        }
        return common_patterns.get(name, "用途待确认")

    def _format_structure(self, structure: dict) -> str:
        """格式化项目结构为树形显示"""
        def _build_tree(struct: dict, prefix: str = "") -> list[str]:
            lines = []
            items = sorted(struct.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{name}")
                if isinstance(value, dict):
                    extension = "    " if is_last else "│   "
                    lines.extend(_build_tree(value, prefix + extension))
            return lines
        
        return "\n".join(_build_tree(structure))

    def _evaluate_structure(self, structure: dict) -> str:
        """评估项目结构"""
        try:
            evaluation = []
            # 检查基本项目结构
            if "tests" in structure:
                evaluation.append("✓ 包含测试目录")
            if "docs" in structure:
                evaluation.append("✓ 包含文档目录")
            if any(f.endswith('.md') for f in structure):
                evaluation.append("✓ 包含文档文件")
            
            return "\n".join(evaluation) if evaluation else "结构评估待完成"
        except Exception:
            return "结构评估失败"

    def _suggest_organization(self, structure: dict) -> str:
        """提供组织建议"""
        suggestions = []
        
        # 基本目录建议
        if "tests" not in structure:
            suggestions.append("- 建议添加tests目录用于测试代码")
        if "docs" not in structure:
            suggestions.append("- 建议添加docs目录用于项目文档")
        if not any(f.endswith('.md') for f in structure):
            suggestions.append("- 建议添加README.md等说明文档")
            
        return "\n".join(suggestions) if suggestions else "暂无组织建议"

    def _format_components(self, components: dict) -> str:
        """格式化关键组件说明"""
        formatted = []
        for name, details in components.items():
            formatted.append(f"### {name}")
            if isinstance(details, tuple) and len(details) == 2:
                code, desc = details
                formatted.extend([f"```python\n{code}\n```", desc])
            else:
                formatted.append(str(details))
        return "\n".join(formatted)

    def _format_dependencies(self) -> str:
        """格式化依赖关系"""
        try:
            deps = self.config_service.get_dependencies()
            return "\n".join(f"- {name}: {version}" for name, version in deps.items())
        except Exception:
            return "依赖关系分析失败"

    def _get_best_practices(self) -> str:
        """获取最佳实践建议"""
        return """
- 遵循PEP 8编码规范
- 编写完整的单元测试
- 添加类型注解
- 保持函数简单，遵循单一职责原则
- 使用有意义的变量和函数名
- 添加必要的文档注释
"""

    def _format_versions(self, versions: list) -> str:
        """格式化版本历史"""
        formatted = []
        for version in versions:
            if isinstance(version, dict):
                formatted.append(
                    f"### {version.get('version', '')}"
                    f" ({version.get('date', '')})\n"
                    f"{version.get('changes', '')}"
                )
        return "\n".join(formatted)

    def save_prompt(self, content: str, project_root: str) -> None:
        """保存prompt文档到项目根目录
        
        Args:
            content: 文档内容
            project_root: 项目根目录
        """
        try:
            doc_path = Path(project_root) / "code.md"
            doc_path.write_text(content, encoding="utf-8")
            logger.info(f"Prompt文档已保存到: {doc_path}")
        except Exception as e:
            logger.error(f"保存Prompt文档时发生错误: {e}") 