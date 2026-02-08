# app/routers/user_controller.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from loguru import logger
import json
import dotenv

logger.add("demo.log")
"""
# 在.env中加载对应环境变量， 示例如下
AIFLOW_DOMAIN="私有化部署的aiflow接口域名，如果使用Saas那么不需要配置此项"
APP_NAME="fastApi demo"
APP_CN_NAME="fastApi例子"
APP_ID="从aiflow后台查询企业的app_id信息"
APP_SECRET="从aiflow后台查询企业的app_id信息"
ENTERPRISE_CODE="从aiflow后台查询企业代码"
SERVICE_DOMAIN="http服务对应的域名地址，需要确保私有化部署或者saas部署的aiflow可以访问到"
"""
dotenv.load_dotenv(".env")
from aflow_client_python import EnhancedServiceRegistrar
from aflow_client_python import ApiRoute
from aflow_client_python import WithModel

from fastapi import FastAPI

# 1. 创建FastAPI应用
app = FastAPI(title="统一模型API服务")


# 所有要暴露的http接口，使用到的入参和出参，必须要使用BaseModel定义
# 所有字段，请务必提供对应的类型信息，否则使用str作为默认值
# 目前支持的类型为 int, float, str, bool, list, set. 当需要使用dict, 使用对象来定义
# GET请求参数模型
class UserSearchQuery(BaseModel):
    keyword: Optional[str] = Field(None, min_length=2, description="搜索关键词")
    status: Optional[str] = Field(None, description="用户状态")
    created_after: Optional[datetime] = Field(None, description="创建时间之后")
    limit: int = Field(20, ge=1, le=100, description="返回数量限制")
    offset: int = Field(0, ge=0, description="偏移量")

    @field_validator("keyword")
    def keyword_not_empty(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("关键词不能为空字符串")
        return v


# 嵌套模型
class UserProfile(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    bio: Optional[str] = Field(None, max_length=500)
    # interests: List[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)


# POST请求参数模型
class UserCreateModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="用户邮箱")
    # profile: Optional["UserProfile"] = None
    profile: Optional[UserProfile]

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "profile": {"age": 30, "bio": "Software developer"},
            }
        }
    )

# 自定义标准返回接口示例，用户可以自行修改
class StandardResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: Optional[str] = Field(None, description="请求结果数据")
    message: Optional[str] = Field(None, description="请求结果信息")

# 如果data为自定义模型，则需要通过继承StandardResponse
class StdRespUser(StandardResponse):
    data: Optional[UserCreateModel]


# 注册嵌套模型（解决前向引用）
# UserCreateModel.model_rebuild()
# StandardResponse.model_rebuild()


# GET接口
@app.get("/api/v1/users/search", response_model=StandardResponse)
# ApiRoute用于描述接口信息
@ApiRoute("GET", "/api/v1/users/search", desc="搜索用户接口")
# WithModel用于描述接口参数和返回值
@WithModel(UserSearchQuery)
def search_users(query: UserSearchQuery) -> StandardResponse:
    """搜索用户 - 使用BaseModel定义所有查询参数"""
    # query参数已自动验证和转换类型
    # results = f"Hello World: {json.dumps(query.model_dump_json())}"
    results = f"Hello World: {query.keyword}"
    logger.info(f"search_users resp: {results}")
    return StandardResponse(success=True, data=results)


# POST接口
@app.post("/api/v1/users", response_model=StdRespUser)
@ApiRoute("POST", "/api/v1/users", desc="创建用户接口")
@WithModel(UserCreateModel)
def create_user(user_data: UserCreateModel) -> StdRespUser:
    """创建新用户 - 使用BaseModel定义所有请求体参数"""
    # user_data已自动验证和转换类型
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "profile": user_data.profile.model_dump(),
        "id": 12345,
    }
    logger.info(f"create user: {user}")
    return StdRespUser(success=True, data=user)


# 启动和注册
if __name__ == "__main__":
    # 注册服务到注册中心, 启动后直接注册, 参数为需要扫描的包路径
    EnhancedServiceRegistrar(
        package_list=["fastapi_demo"]
    )

    # 启动服务
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
