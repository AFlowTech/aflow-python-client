from typing import List
from pydantic import BaseModel, Field, ConfigDict

class SyncFailDetail(BaseModel):
    """
    同步失败详情
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    code: str = Field(..., alias="code", description="错误代码")
    message: str = Field(..., alias="message", description="错误消息")

class SyncResult(BaseModel):
    """
    同步结果
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    success_count: int = Field(..., alias="successCount", description="成功数量")
    fail_count: int = Field(..., alias="failCount", description="失败数量")
    fail_details: List[SyncFailDetail] = Field(..., alias="failDetails", description="失败详情列表")
