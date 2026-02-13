from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ThirdPartyTaskSyncTask(BaseModel):
    """
    三方任务同步任务项
    """

    third_task_id: str = Field(..., alias="thirdTaskId", description="任务ID（外部系统）")
    task_name: str = Field(..., alias="taskName", description="任务名称")
    assignee_user_code: List[str] = Field(..., alias="assigneeUserCode", description="处理人编码列表（可能有多个）")
    task_status: str = Field("ing", alias="taskStatus", description="任务状态：new-新建，ing-处理中，over-完成（默认ing）")
    task_result: str = Field(..., alias="taskResult",
                             description="任务处理结果：new-新建，accept-领取，pass-通过，reject-拒绝，revoke-撤销，rebut-驳回")
    dead_line: Optional[str] = Field(None, alias="deadLine", description="处理截止时间（格式：yyyy-MM-dd HH:mm:ss）")
    node_type: str = Field("audit", alias="nodeType",
                           description="节点类型：handle-执行，audit-审批，notify-知悉（默认audit）")
    create_time: Optional[str] = Field(None, alias="createTime", description="创建时间（格式：yyyy-MM-dd HH:mm:ss）")
    handle_time: Optional[str] = Field(None, alias="handleTime",
                                       description="处理时间（格式：yyyy-MM-dd HH:mm:ss，处理完成后必填）")
    show_pc: Optional[bool] = Field(None, alias="showPc", description="PC是否展示")
    show_mobile: Optional[bool] = Field(None, alias="showMobile", description="手机是否展示")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


class ThirdPartyTaskSyncCcUser(BaseModel):
    """
    三方任务同步抄送人
    """

    user_code: str = Field(..., alias="userCode", description="抄送人编码(贵公司-用户编码)")
    cc_time: Optional[str] = Field(None, alias="ccTime", description="抄送时间（格式：yyyy-MM-dd HH:mm:ss）")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


class ThirdPartyTaskSyncReq(BaseModel):
    """
    三方任务同步请求
    """

    third_order_id: int = Field(..., alias="thirdOrderId", description="流程订单号（外部系统）")
    order_status: str = Field("ing", alias="orderStatus", description="订单状态：new-新建，ing-处理中，over-完成（默认ing）")
    order_result: str = Field(..., alias="orderResult",
                              description="订单结果：ing-处理中，pass-已完成，reject-已拒绝，revoke-已撤销，delete-已删除")
    initiator: str = Field(..., alias="initiator", description="发起人编号")
    version: Optional[int] = Field(None, alias="version", description="订单版本（有就传，没有可以不传）")
    parent_order_id: Optional[int] = Field(None, alias="parentOrderId", description="父订单号（有就传，没有可以不传）")
    parent_task_order_id: Optional[str] = Field(None, alias="parentTaskOrderId",
                                                description="父任务订单号（有就传，没有可以不传）")
    business_key: Optional[str] = Field(None, alias="businessKey",
                                        description="业务编码，用于记录三方系统跟流程引擎对接的唯一映射Key")
    create_time: Optional[str] = Field(None, alias="createTime",
                                       description="流程订单创建时间（格式：yyyy-MM-dd HH:mm:ss）")
    update_time: Optional[str] = Field(None, alias="updateTime",
                                       description="流程订单更新时间（格式：yyyy-MM-dd HH:mm:ss）")
    third_flow_code: Optional[str] = Field(None, alias="thirdFlowCode", description="三方流程编码（新建订单时必填）")
    cc_users: Optional[List[ThirdPartyTaskSyncCcUser]] = Field(None, alias="ccUsers",
                                                               description="抄送人列表（非必传，有就传，没有就不传）")
    tasks: List[ThirdPartyTaskSyncTask] = Field(..., alias="tasks", description="任务列表（包含待办和已完成任务）")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化
