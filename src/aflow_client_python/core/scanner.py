import importlib
import pkgutil
import inspect
from typing import Type, Dict, Any, List, Callable, Optional
from pydantic import BaseModel
import typing
from typing import get_origin, get_args

try:
    from ..utils.logger import get_logger
except ImportError:
    import sys
    import os

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    from aflow_client_python.utils.logger import get_logger

logger = get_logger()


class EnhancedInterfaceScanner:
    """增强版接口扫描器（完整可运行实现）"""

    def __init__(
            self,
    ):
        self.discovered_interfaces: List[Dict[str, Any]] = []  # 存储扫描到的接口信息

    def scan(self, base_package) -> List[Dict[str, Any]]:
        """扫描指定包下所有模块，识别带注解的接口"""
        import os

        try:
            package = importlib.import_module(base_package)
        except ImportError as e:
            logger.error(f"错误：无法导入根包 {base_package}，原因：{e}")
            return self.discovered_interfaces

        # 获取包所在目录路径 - 修正版本
        package_file = getattr(package, "__file__", None)
        if not package_file:
            logger.warning(f"警告：包 {base_package} 无有效文件路径，跳过扫描")
            return self.discovered_interfaces

        # 将文件路径转换为目录路径
        package_path = os.path.dirname(package_file)

        # 遍历包目录下所有模块
        for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
            if is_pkg:  # 跳过子包
                continue
            full_module_name = f"{base_package}.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
                self._scan_module(module)  # 扫描当前模块
            except ImportError as e:
                logger.warning(f"警告：无法导入模块 {full_module_name}，原因：{e}")
                continue

        return self.discovered_interfaces  # 返回扫描结果

    def _scan_module(self, module: Any) -> None:
        """扫描单个模块，识别函数和类方法中的接口注解"""
        # 扫描模块级函数
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isfunction(attr) and self._has_api_annotation(attr):
                self._process_function(attr, module.__name__)

        # 扫描模块内类的静态方法/实例方法
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isclass(attr):
                for method_name, method in inspect.getmembers(attr, inspect.isfunction):
                    if self._has_api_annotation(method):
                        context = f"{module.__name__}.{attr.__name__}"
                        self._process_function(method, context)

    def _has_api_annotation(self, obj: Any) -> bool:
        """检查对象是否有API路由注解（@ApiRoute/@HttpMethod）"""
        return hasattr(obj, "__api_route__") or hasattr(obj, "__http_annotation__")

    def _process_function(self, func: Callable, context: str) -> None:
        """处理单个函数：区分模型注解和旧版参数注解"""
        if hasattr(func, "__param_model__"):
            # 使用统一模型（@WithModel）
            try:
                interface_info = EnhancedInterfaceParser.parse_with_model(func, context)
                self.discovered_interfaces.append(interface_info)
                logger.info(
                    f"扫描到接口：{interface_info['http_method']} {interface_info['path']}（模型：{interface_info['model_class']}）"
                )
            except Exception as e:
                logger.error(f"解析函数 {func.__name__} 失败（模型注解）：{e}")

    def _parse_function_with_model(self, func: Callable, context: str) -> None:
        """（内部方法）处理带@WithModel注解的函数"""
        self._process_function(func, context)


class EnhancedInterfaceParser:
    """增强接口解析器（需与之前定义一致，此处补充必要方法）"""

    @staticmethod
    def parse_with_model(func: Callable, context: str = "") -> Dict[str, Any]:
        """解析带模型的函数（完整实现）"""
        api_info = getattr(func, "__api_route__", {})
        model_info = getattr(func, "__param_model__", {})
        model_class = model_info.get("class")

        if not model_class or not issubclass(model_class, BaseModel):
            raise ValueError(f"函数 {func.__name__} 未关联有效BaseModel")

        # 提取模型字段信息
        parameters = []

        # 兼容 Pydantic V1 和 V2
        try:
            # Pydantic V2
            model_fields = model_class.model_fields
            for field_name, field in model_fields.items():
                field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                parameters.append(field_info)
        except AttributeError:
            # Pydantic V1
            model_fields = model_class.__fields__
            for field_name, field in model_fields.items():
                field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                parameters.append(field_info)

        # 解析返回类型 - 改进版本，支持详细字段信息
        return_type = getattr(func, "__annotations__", {}).get("return")
        return_info = EnhancedInterfaceParser._extract_return_info(return_type)

        return {
            "name": func.__name__,
            "package_path": context,
            "desc": api_info.get("description", ""),  # 添加接口描述
            "http_method": api_info.get("method"),
            "path": api_info.get("path"),
            "parameters": parameters,
            "return_info": return_info,
            "model_class": model_class.__name__,  # 添加缺失的字段
            "original_func": func,  # 保留原函数引用，供框架适配使用
        }

    @staticmethod
    def _extract_field_info(field_name: str, field, context_module=None):
        """提取字段信息，支持嵌套模型"""
        field_info = {
            "name": field_name.split(".")[-1],  # 直接取字段名
            "required": field.is_required(),
            "raw_type": str(field.annotation),
            "type": TypeConverter.convert(field.annotation),
            "default": field.default if not field.is_required() else "",
            "description": field.description if field.description else "",
        }

        # 解析实际类型（处理Optional、前向引用等情况）
        actual_type = EnhancedInterfaceParser._resolve_actual_type(field.annotation, context_module)

        # 检查是否为嵌套的Pydantic模型
        if (actual_type and hasattr(actual_type, '__bases__') and
                BaseModel in actual_type.__mro__):  # 检查是否为BaseModel的子类
            # 递归解析嵌套模型的字段
            nested_parameters = []
            try:
                nested_fields = actual_type.model_fields
                for nested_name, nested_field in nested_fields.items():
                    nested_info = EnhancedInterfaceParser._extract_field_info(
                        f"{field_name}.{nested_name}",
                        nested_field,
                        context_module
                    )
                    nested_parameters.append(nested_info)
            except AttributeError:
                # 兼容Pydantic V1
                nested_fields = actual_type.__fields__
                for nested_name, nested_field in nested_fields.items():
                    nested_info = EnhancedInterfaceParser._extract_field_info(
                        f"{field_name}.{nested_name}",
                        nested_field,
                        context_module
                    )
                    nested_parameters.append(nested_info)

            field_info["nested_fields"] = nested_parameters
            field_info["is_nested"] = True

        return field_info

    @staticmethod
    def _resolve_actual_type(annotation, context_module=None):
        """解析实际类型，处理Optional、Union、前向引用等情况"""
        origin_type = get_origin(annotation)

        if origin_type is typing.Union:
            # 处理Optional[Type] 或 Union[Type, None] 等联合类型
            args = get_args(annotation)
            for arg in args:
                if arg is not type(None):  # 排除None类型
                    return EnhancedInterfaceParser._resolve_actual_type(arg, context_module)
        elif isinstance(annotation, str):
            # 处理字符串前向引用
            if context_module:
                try:
                    actual_type = getattr(context_module, annotation, None)
                    if actual_type is None:
                        # 尝试从globals获取
                        actual_type = globals().get(annotation)
                    return actual_type
                except:
                    pass
        elif hasattr(annotation, '__bases__') and BaseModel in annotation.__mro__:
            # 直接是BaseModel子类
            return annotation
        elif isinstance(annotation, type):
            # 普通类型
            return annotation

        return None

    @staticmethod
    def _extract_return_info(return_type: Type) -> Dict[str, Any]:
        """提取返回值信息，支持复杂类型解析"""
        if return_type is None:
            return {"type": "void"}

        # 获取基本类型信息
        basic_type = TypeConverter.convert(return_type)

        # 初始化返回信息
        return_info = {
            "type": basic_type,
            "raw_type": str(return_type)
        }

        # 如果返回类型是Pydantic模型，解析其字段
        if (hasattr(return_type, '__bases__') and
                BaseModel in return_type.__mro__):
            try:
                # 兼容 Pydantic V2
                model_fields = return_type.model_fields
                fields_info = []
                for field_name, field in model_fields.items():
                    field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                    fields_info.append(field_info)
                return_info["fields"] = fields_info
            except AttributeError:
                # 兼容 Pydantic V1
                model_fields = return_type.__fields__
                fields_info = []
                for field_name, field in model_fields.items():
                    field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                    fields_info.append(field_info)
                return_info["fields"] = fields_info

        # 如果返回类型是包含Pydantic模型的容器类型（如List[Model], Dict[str, Model]）
        origin_type = get_origin(return_type)
        if origin_type is not None:
            args = get_args(return_type)
            if args:
                # 检查泛型参数中是否有Pydantic模型
                for arg in args:
                    if (hasattr(arg, '__bases__') and
                            BaseModel in arg.__mro__):
                        try:
                            # 兼容 Pydantic V2
                            model_fields = arg.model_fields
                            fields_info = []
                            for field_name, field in model_fields.items():
                                field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                                fields_info.append(field_info)
                            return_info["item_fields"] = fields_info
                        except AttributeError:
                            # 兼容 Pydantic V1
                            model_fields = arg.__fields__
                            fields_info = []
                            for field_name, field in model_fields.items():
                                field_info = EnhancedInterfaceParser._extract_field_info(field_name, field)
                                fields_info.append(field_info)
                            return_info["item_fields"] = fields_info
                        break  # 只处理第一个找到的模型类型

        return return_info


class TypeConverter:
    @staticmethod
    def convert(v_type: Type) -> str:
        """
        将Python类型转换为标准字符串格式
        """
        # 特殊处理 typing.Any
        if v_type is typing.Any:
            return "any"

        # 处理typing模块的特殊类型
        origin_type = get_origin(v_type)

        if origin_type is not None:
            # 处理Optional类型 (Union[X, None])
            if origin_type is typing.Union:
                args = get_args(v_type)
                if len(args) == 2 and type(None) in args:
                    non_none_type = args[0] if args[1] is type(None) else args[1]
                    base_type = TypeConverter.convert(non_none_type)
                    return base_type  # 返回非None类型

            # 处理List, Dict等容器类型
            elif origin_type is list or origin_type is typing.List:
                args = get_args(v_type)
                item_type = "any" if not args else TypeConverter.convert(args[0])
                return f"list[{item_type}]"
            elif origin_type is dict or origin_type is typing.Dict:
                args = get_args(v_type)
                key_type = "string" if not args else TypeConverter.convert(args[0])
                val_type = "any" if len(args) < 2 else TypeConverter.convert(args[1])
                return f"dict[{key_type}, {val_type}]"
            elif origin_type is set or origin_type is typing.Set:
                args = get_args(v_type)
                item_type = "any" if not args else TypeConverter.convert(args[0])
                return f"list[{item_type}]"
            else:
                # 其他泛型类型
                base_name = TypeConverter._get_base_type_name(origin_type)
                if base_name:
                    return base_name
                else:
                    return str(origin_type).replace("<class '", "").replace("'>", "")
        else:
            # 处理普通类型
            if v_type == str:
                return "string"
            elif v_type == int:
                return "long"
            elif v_type == float:
                return "double"
            elif v_type == bool:
                return "boolean"
            elif v_type == list:
                return "array"
            elif v_type == dict:
                return "record"
            elif v_type == set:
                return "array"
            elif isinstance(v_type, type):  # 其余默认转为字符串类型
                return "string"
            else:
                # 为其他未知类型提供更通用的处理
                type_str = str(v_type)
                if type_str.startswith("<class '"):
                    return type_str.replace("<class '", "").replace("'>", "").split('.')[-1]
                else:
                    # return "any"  # 对于无法识别的类型，返回通用的 any 类型
                    raise TypeError(f"Unsupported type: {v_type}")

    @staticmethod
    def _get_base_type_name(v_type):
        """获取类型的基名称"""
        if v_type == str:
            return "string"
        elif v_type == int:
            return "long"
        elif v_type == float:
            return "double"
        elif v_type == bool:
            return "boolean"
        elif v_type == list:
            return "array"
        elif v_type == set:
            return "array"
        else:
            return None
