# Configuration management

import os
from typing import Optional, Any, Dict, Type
from dataclasses import dataclass, field
from enum import Enum


class Config:
    """Configuration holder for aiflow client"""

    def __init__(self):
        self._config = {
            "aiflow_domain": os.environ.get("AIFLOW_DOMAIN", "https://api.aiflow.fan"),
            "app_name": os.environ.get("APP_NAME", ""),
            "app_cn_name": os.getenv("APP_CN_NAME", ""),
            "app_id": os.getenv("APP_ID", ""),
            "app_secret": os.getenv("APP_SECRET", ""),
            "enterprise_code": os.getenv("ENTERPRISE_CODE", ""),
            "timeout": int(os.getenv("TIMEOUT", "30")),
            "service_domain": os.getenv("SERVICE_DOMAIN", ""),
        }

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)

    def get_credential(self) -> Dict[str, str]:
        """Get credential configuration"""
        return {
            "app_id": self.get("app_id"),
            "app_secret": self.get("app_secret"),
            "enterprise_code": self.get("enterprise_code"),
        }


# Singleton instance
config_manager = Config()





class AServiceType(Enum):
    """服务类型枚举"""

    MQ = "MQ"
    HTTP = "HTTP"


@dataclass
class AServiceRouteContext:
    """
    服务路由上下文对象
    reqParamSchema 例子：
        {"type":"record","required":false,"childrenFields":[{"fieldName":"Aobj","type":"record","required":true,"doc":"对象描述","childrenFields":[{"fieldName":"a","type":"string","required":false,"doc":""}]},{"fieldName":"Alist","type":"array","required":false,"doc":"列表描述","itemType":"string"}]}
    respParamSchema 例子：
        {"type":"record","required":false,"childrenFields":[{"fieldName":"status","type":"int","required":true,"doc":"状态码"},{"fieldName":"data","type":"string","required":false,"doc":"数据"},{"fieldName":"msg","type":"string","required":false,"doc":"错误信息"}]}
    """

    # param: Type  # 参数类型

    enterpriseCode: str  # 企业编码 必填

    name: str  # 名称 重要，使用该字段展示服务名
    serviceName: str  # 服务名称 HTTP时为url地址

    methodType: str # 请求方法类型 GET, POST等
    reqParamSchema: str  # 请求参数schema
    respParamSchema: str  # 响应参数schema
    aServiceType: AServiceType.HTTP.value  # 服务类型， 接口类型传入时，直接使用字符串，例如HTTP即可

    description: Optional[str]  # 描述 可选

    domain: str # 域名信息，支持包含端口号
    ip: str  # IP地址
    port: int  # 端口号
    hostName: str  # 主机名

    appName: Optional[str]  # 应用名称 用于在应用中心注册应用
    appCnName: Optional[str]  # 应用中文名称 用于在应用中心注册应用

    tag: Optional[str]  # 标签 未使用
    topic: Optional[str]  # 主题，仅MQ服务使用
    methodSchema: Optional[str]  # 方法schema， 仅MQ服务使用

if __name__ == '__main__':
    print(AServiceType.HTTP.value)
    print(type(AServiceType.HTTP.value))


