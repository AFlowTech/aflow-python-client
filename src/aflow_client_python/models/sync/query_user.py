from pydantic import Field

from ..base import AFlowBaseModel


class QueryUserParam(AFlowBaseModel):
    """用户详情查询参数"""

    user_code: str = Field(..., alias="userCode", description="AFlow 用户编码")


class QueryUserByEmailParam(AFlowBaseModel):
    """用户邮箱查询参数"""

    email: str = Field(..., description="用户邮箱")
