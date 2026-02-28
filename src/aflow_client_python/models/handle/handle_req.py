from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef


class AHandleParam(BaseModel):
    order_id: int = Field(..., alias="orderId", description="必填，流程订单编码")
    task_order_id: Optional[str] = Field(None, alias="taskOrderId", description="任务ID，当用户可能多个任务节点时必传")
    operate_type: str = Field(..., alias="operateType", description="必填，操作类型，参考：OperateType")
    cc_user_code: Optional[List[str]] = Field(None, alias="ccUserCode", description="抄送给谁（贵公司-用户编码）")
    accept_user_code: Optional[str] = Field(None, alias="acceptUserCode", description="转交给谁（贵公司-用户编码）")
    cc_content: Optional[str] = Field(None, alias="ccContent", description="抄送内容")
    custom_user_code: str = Field(..., alias="customUserCode", description="必填，操作人（贵公司-用户编码）")
    remark: Optional[str] = Field(None, alias="remark", description="处理备注")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


# 使用 ForwardRef 处理循环依赖
AComboxDataGroup = ForwardRef("AComboxDataGroup")


class AValue(BaseModel):
    # AValue 是一个接口，这里用 BaseModel 表示
    type: str = Field(..., description="字段类型")
    data: str = Field(..., description="字段值")


class AFieldValue(BaseModel):
    name: str = Field(..., description="字段名称，用于标识字段")
    state: Optional[str] = Field(None, description="字段状态")
    value: AValue = Field(..., description="字段值")
    children: Optional[List[AComboxDataGroup]] = Field(None, description="子字段")

    def has_children(self) -> bool:
        return self.children is not None and len(self.children) > 0


class AComboxDataGroup(BaseModel):
    name: str = Field(..., description="子字段名称")
    state: Optional[str] = Field(None, description="子字段状态")
    value: AValue = Field(..., description="子字段值")
    children: Optional[List[AComboxDataGroup]] = Field(None, description="嵌套的子字段")

    def has_children(self) -> bool:
        return self.children is not None and len(self.children) > 0


# 更新 ForwardRef 的引用
AComboxDataGroup.update_forward_refs()


class AFormData(BaseModel):
    values: List[AFieldValue] = Field(..., description="全表单字段值")
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


class HandleFlowReq(BaseModel):
    """
    处理标准表单
    """
    handle_param: AHandleParam = Field(..., alias="handleParam", description="基本信息")
    form_data: Optional[AFormData] = Field(None, alias="formData", description="对象或表单数据")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


class PropertyMappingConfig(BaseModel):
    field_full_name: str = Field(..., alias="fieldFullName", description="必填，简单字段与filedName一致，复杂字段需要包含完整路径")
    field_name: str = Field(..., alias="fieldName", description="表单字段名，忽略path部分")
    value_path: Optional[str] = Field(None, alias="valuePath", description="值路径类型，参考：ValuePathType")
    property_path: str = Field(..., alias="propertyPath", description="映射属性formData map中的key")
    value_property_path: Optional[str] = Field(None, alias="valuePropertyPath", description="值属性路径，不包括全路径、只是对应ValuePathType的属性, 如images.url 、 PropertyPath==images.url ，ValuePropertyPath == url")
    visible: bool = Field(..., description="是否可见")
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化


class HandleFlowByObjectReq(BaseModel):
    """
    处理泛型表单
    """

    handle_param: AHandleParam = Field(..., alias="handleParam", description="基本信息")
    form_data: str = Field(..., alias="formData",
                                     description="对象或表单数据")
    property_mapping: List[PropertyMappingConfig] = Field(..., alias="propertyMapping",
                                            description="当使用泛型时，该字段必填")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化
