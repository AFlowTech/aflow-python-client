from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class QueryOrderParam(BaseModel):
    """部门信息模型"""
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    order_id: str = Field(..., alias="orderId", description="任务订单ID")