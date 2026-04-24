from pydantic import Field

from ..base import AFlowBaseModel


class QueryOrderParam(AFlowBaseModel):
    """部门信息模型"""

    order_id: str = Field(..., alias="orderId", description="任务订单ID")
