# aflow-client-python
# A Python library for registering services to aiflow via annotations

from .core.decorator import ApiRoute, WithModel
from .core.scanner import EnhancedInterfaceScanner
from .core.register import EnhancedServiceRegistrar
from .core.config import config_manager
from .utils.sign import ASignature
from .client import (
    AFlowClient, 
    AFlowAPIClient,
    Department,
    User,
    UrlConfig,
    TaskInfo,
    CCUser,
    AllowedRule
)

__all__ = [
    "ApiRoute",
    "WithModel",
    "EnhancedInterfaceScanner",
    "EnhancedServiceRegistrar",
    "config_manager",
    "ASignature",
    "AFlowClient",
    "AFlowAPIClient",
    "Department",
    "User",
    "UrlConfig",
    "TaskInfo",
    "CCUser",
    "AllowedRule",
]