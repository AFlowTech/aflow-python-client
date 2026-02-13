from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ThirdPartyFlowUrl(BaseModel):
    """
    三方流程URL配置
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    h5_url: Optional[str] = Field(None, alias="h5Url", description="H5端地址")
    web_url: Optional[str] = Field(None, alias="webUrl", description="PC端地址")


class AllowedApplyRule(BaseModel):
    """
    允许发起/管理规则
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    allowed_apply_type: str = Field(..., alias="allowedApplyType", description="允许发起类型（ALL-全部，CUSTOM-自定义）")
    user_codes: Optional[List[str]] = Field(None, alias="userCodes", description="允许发起的用户编码列表")
    dept_codes: Optional[List[str]] = Field(None, alias="deptCodes", description="允许发起的部门编码列表")
    user_group_codes: Optional[List[str]] = Field(None, alias="userGroupCodes", description="允许发起的用户组编码列表")


class ThirdPartyFlowCreateReq(BaseModel):
    """
    创建三方流程定义请求
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化
    title: str = Field(..., alias="title", description="流程标题")
    external_system_code: Optional[str] = Field("odoo", alias="externalSystemCode",
                                                description="外部系统编码（可选，默认为 odoo）")
    initiate_url: ThirdPartyFlowUrl = Field(..., alias="initiateUrl", description="流程发起页地址")
    detail_url: ThirdPartyFlowUrl = Field(..., alias="detailUrl", description="流程详情页地址")
    category_id: str = Field(..., alias="categoryId", description="分类ID")
    manager_user_code: str = Field(..., alias="managerUserCode", description="流程负责人编码(贵公司-用户编码)")
    operation_user_code: str = Field(..., alias="operationUserCode", description="运营负责人编码(贵公司-用户编码)")
    config_user_code: str = Field(..., alias="configUserCode", description="配置负责人编码(贵公司-用户编码)")
    create_by: str = Field(..., alias="createBy", description="创建人编码(贵公司-用户编码)")
    allowed_apply_terminals: List[str] = Field(..., alias="allowedApplyTerminals", description="允许发起的终端")
    allowed_apply_rule: AllowedApplyRule = Field(..., alias="allowedApplyRule", description="允许发起规则")
    allowed_manage_rule: AllowedApplyRule = Field(..., alias="allowedManageRule", description="允许管理规则")
