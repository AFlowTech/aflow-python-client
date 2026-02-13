from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ThirdPartyFlowOnlineReq(BaseModel):
    """
    三方流程定义上线请求
    """

    third_flow_code: str = Field(..., alias="thirdFlowCode", description="三方自己使用的流程编码")
    flow_version: Optional[int] = Field(None, alias="flowVersion", description="流程版本")
    update_desc: Optional[str] = Field(None, alias="updateDesc", description="更新说明")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化
