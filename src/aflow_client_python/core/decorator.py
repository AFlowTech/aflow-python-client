from typing import Type, Any, Dict, List
from pydantic import BaseModel
from functools import wraps


class ApiRoute:
    """统一的路由装饰器，支持GET/POST等方法"""

    def __init__(self, method: str, path: str, desc: str = ""):
        self.method = method.upper()
        self.path = path
        self.description = desc

    def __call__(self, func):
        func.__api_route__ = {
            "method": self.method,
            "path": self.path,
            "description": self.description,
            "func_name": func.__name__,
        }

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper


# 便捷装饰器
# Get = lambda path: ApiRoute("GET", path)
# Post = lambda path: ApiRoute("POST", path)


class WithModel:
    """参数模型关联装饰器（需与之前定义一致）"""

    def __init__(self, model_class: Type[BaseModel], param_location: str = "auto"):
        self.model_class = model_class
        self.param_location = param_location

    def __call__(self, func):
        func.__param_model__ = {
            "class": self.model_class,
            "location": self.param_location,
        }
        # 自动判断参数位置（GET→query，POST→body）
        if self.param_location == "auto":
            method = getattr(func, "__api_route__", {}).get("method", "GET")
            func.__param_model__["location"] = "query" if method == "GET" else "body"
        return func
