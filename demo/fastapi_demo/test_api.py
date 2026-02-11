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
from aflow_client_python import AFlowClient
from aflow_client_python import StartFlowParam

class StartFlowParam(BaseModel):
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

def start_flow(startFlowParam: StartFlowParam) -> None:
    AFlowClient.start_flow(startFlowParam)


# 启动和注册
if __name__ == "__main__":
    start_flow()
