from typing import Optional

from pydantic import Field

from ..base import AFlowBaseModel


class ThirdPartyFlowOnlineReq(AFlowBaseModel):
    """
    三方流程定义上线请求
    """

    third_flow_code: str = Field(..., alias="thirdFlowCode", description="三方自己使用的流程编码")
    flow_version: Optional[int] = Field(None, alias="flowVersion", description="流程版本")
    update_desc: Optional[str] = Field(None, alias="updateDesc", description="更新说明")
