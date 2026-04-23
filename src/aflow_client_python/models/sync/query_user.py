from pydantic import BaseModel, Field, ConfigDict


class QueryUserParam(BaseModel):
    """用户详情查询参数"""
    model_config = ConfigDict(populate_by_name=True)

    user_code: str = Field(..., alias="userCode", description="AFlow 用户编码")
