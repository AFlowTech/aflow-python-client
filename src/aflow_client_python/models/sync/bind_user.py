from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BindUserReq(BaseModel):
    """
    用户绑定信息
    """

    custom_user_code: str = Field(..., alias="customUserCode",
                                  description="必填，自定义的用户编码，即贵公司系统的用户唯一Id")
    link_user_code: Optional[str] = Field(None, alias="linkUserCode",
                                          description="如果需要集成三方办公平台，linkUserCode/phoneNumber必须传一个，优先级 linkUserCode > phoneNumber")
    phone_number: Optional[str] = Field(None, alias="phoneNumber",
                                        description="用户的手机号，和 linkUserCode 二选一，优先级 linkUserCode > phoneNumber")

    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化
