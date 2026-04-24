from typing import List, Optional

from pydantic import Field

from ..base import AFlowBaseModel


class OrderListQueryParam(AFlowBaseModel):
    """订单列表查询参数"""

    key: Optional[str] = Field(None, alias="key", description="搜索关键字")
    flow_code: Optional[str] = Field(None, alias="flowCode", description="流程编码")
    flow_codes: Optional[List[str]] = Field(None, alias="flowCodes", description="流程编码列表")
    user_code: Optional[str] = Field(None, alias="userCode", description="用户编码")
    user_codes: Optional[List[str]] = Field(None, alias="userCodes", description="用户编码列表")
    start_time: Optional[str] = Field(None, alias="startTime", description="开始日期，格式 yyyy-MM-dd")
    end_time: Optional[str] = Field(None, alias="endTime", description="结束日期，格式 yyyy-MM-dd")
    list_type: Optional[str] = Field(None, alias="listType", description="列表类型")
    task_view_type: Optional[str] = Field(None, alias="taskViewType", description="视图类型")
    order_status: Optional[str] = Field(None, alias="orderStatus", description="订单状态")
    order_result: Optional[str] = Field(None, alias="orderResult", description="订单结果")
    supervision: Optional[bool] = Field(None, alias="supervision", description="是否督办")
    overdue: Optional[bool] = Field(None, alias="overdue", description="是否超时")
    soon_overdue: Optional[bool] = Field(None, alias="soonOverdue", description="是否即将超时")
    urge: Optional[bool] = Field(None, alias="urge", description="是否催办")
    flow_order_id: Optional[int] = Field(None, alias="flowOrderId", description="流程单号")
    with_user_code: Optional[bool] = Field(None, alias="withUserCode", description="是否强制按用户编码查询")
    over_time_range_key: Optional[str] = Field(None, alias="overTimeRangeKey", description="超时时间范围")
    supervision_page: Optional[bool] = Field(None, alias="supervisionPage", description="是否督办页面")
    sort_type: Optional[str] = Field(None, alias="sortType", description="排序方式")
    page_index: Optional[int] = Field(None, alias="page.index", description="页码，从1开始")
    page_size: Optional[int] = Field(None, alias="page.size", description="每页数量")
