from typing import cast

from fastapi import APIRouter, HTTPException

from ...services.config_service import ConfigService
from ...web.config import Config, ExcludePatterns
from ..api.config import ConfigResult

router = APIRouter()


@router.get("")
async def get_exclude_patterns() -> ExcludePatterns:
    """获取排除模式"""
    try:
        config_service = ConfigService.get_instance()
        exclude_patterns = config_service.get_exclude_patterns()
        
        # 转换 set 为 list，以符合 ExcludePatterns 类型
        return cast(ExcludePatterns, {
            "directories": list(exclude_patterns["directories"]),
            "files": list(exclude_patterns["files"]),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
async def update_exclude_patterns(config: dict) -> ConfigResult:
    """更新排除模式"""
    try:
        config_service = ConfigService.get_instance()
        config_service._config.update(cast(Config, config))  # 更新配置
        config_service.save_config()  # 不需要传参数
        return {"status": "success", "message": "排除模式已更新"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
