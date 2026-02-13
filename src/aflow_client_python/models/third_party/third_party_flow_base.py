from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ThirdPartyFlowBase(BaseModel):
    """
    三方流程基础信息响应
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    flow_code: str = Field(..., alias="flowCode", description="流程编码")
    flow_name: str = Field(..., alias="flowName", description="流程名称")
    flow_version: int = Field(..., alias="flowVersion", description="流程版本")
    create_type: str = Field(..., alias="createType", description="创建类型(create/import/third_party)")
    import_ref: Optional[str] = Field(None, alias="importRef", description="引用模板流程编码")
