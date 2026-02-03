# Service reporter for sending service information to aiflow

import requests
from typing import Optional
from threading import Thread, Timer
from typing import Dict, List, Any
import json
import re
import time

# 尝试相对导入，如果失败则使用绝对导入
try:
    from ..utils.sign import ASignature
    from ..utils.logger import get_logger
    from .config import config_manager, AServiceRouteContext, AServiceType
    from .scanner import EnhancedInterfaceScanner
except ImportError:
    import sys
    import os

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    from aflow_client_python.utils.sign import ASignature
    from aflow_client_python.utils.logger import get_logger
    from aflow_client_python.core.config import config_manager, AServiceRouteContext, AServiceType
    from aflow_client_python.core.scanner import EnhancedInterfaceScanner

logger = get_logger()

class FieldAdapter:

    @staticmethod
    def adapter(param_schema: dict) -> dict:
        """
        将python解析出来的内容，处理为注册需要的内容格式

        字段基本信息
        {
          "fieldName": "Alist",     # 字段名称
          "type": "array",          # 字段类型
          "required": false,        # 是否必填
          "doc": "列表描述",         # 描述信息
          "itemType": "string",     # 子字段类型，arrary使用
          "childrenFields": [],     # 子字段信息，record使用
        }
        """
        result = {}
        if param_schema.get("is_nested", False):
            result["fieldName"] = param_schema.get("name", '')
            result["type"] = "record"
            result["required"] = param_schema.get("required", False)
            result["doc"] = param_schema.get("description", "")
            result["childrenFields"] = [
                FieldAdapter.adapter(field) for field in param_schema.get("nested_fields", [])
            ]
        elif param_schema.get("type", '').startswith("list") \
                or param_schema.get("type", '').startswith("array"):
            result["fieldName"] = param_schema.get("name", '')
            result["type"] = "array"
            result["required"] = param_schema.get("required", False)
            result["doc"] = param_schema.get("description", "")

            try:
                raw_type_value = param_schema.get("type", '') if param_schema is not None else ''
                if isinstance(raw_type_value, str):
                    match = re.search(r'\[(.*?)\]', raw_type_value)
                    item_type = match.group(1) if match and match.group(1) else "any"
                else:
                    item_type = "string"
            except (AttributeError, TypeError, re.error):
                item_type = "string"
            result["itemType"] = item_type
        else:
            result["fieldName"] = param_schema.get("name", '')
            result["type"] = param_schema.get("type", '')
            result["required"] = param_schema.get("required", False)
            result["doc"] = param_schema.get("description", "")
        return result


class EnhancedServiceRegistrar:

    def __init__(
            self,
            package_list: Optional[List[str]] = None,
            async_register: bool = True,
            max_retries: int = 3,
            retry_delay: int = 5
    ):
        # 没有提供那么使用线上地址
        self.base_domain: str = config_manager.get("aiflow_domain").strip().rstrip("/")

        self.enterprise_code: str = config_manager.get("enterprise_code")
        self.app_name: str = config_manager.get("app_name")
        self.app_cn_name: str = config_manager.get("app_cn_name")
        self.service_domain: str = config_manager.get("service_domain")
        self.timeout: int = config_manager.get("timeout")
        self.credential: Optional[Dict[str, str]] = config_manager.get_credential()

        self.total_time = 0
        self.total_beans = 0
        self.context_map: Dict[str, AServiceRouteContext] = {}
        self.base_url = "{}/{}".format(self.base_domain, "aflow/api/center/register")
        self.ip = self._get_local_ip()
        self.host_name = self._get_host_name()
        # self.port = config_manager.get("port") # 端口不使用，且可能存在相同服务端口不一致的情况，忽略配置

        self.a_signature = ASignature()
        self.async_register = async_register
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # 异步执行注册
        if async_register:
            try:
                thread = Thread(target=self._async_register, args=(package_list,), daemon=True)
                thread.start()
            except Exception as e:
                logger.error(f"启动异步注册线程失败: {e}")
        else:
            # 同步执行注册
            try:
                self._sync_register(package_list)
            except Exception as e:
                logger.error(f"同步注册失败: {e}")

    def _sync_register(self, package_list: Optional[List[str]]):
        """同步执行注册"""
        try:
            scanner = EnhancedInterfaceScanner()
            for package in package_list or []:
                try:
                    self.register(scanner.scan(package))
                except Exception as e:
                    logger.error(f"注册包 {package} 时发生错误: {e}")
                    continue  # 继续处理其他包
        except Exception as e:
            logger.error(f"同步注册过程中发生严重错误: {e}")

    def _async_register(self, package_list: Optional[List[str]]):
        """异步执行注册，包含重试机制"""
        for package in package_list or []:
            try:
                scanner = EnhancedInterfaceScanner()
                interfaces = scanner.scan(package)

                # 重试机制
                for attempt in range(self.max_retries):
                    try:
                        self.register(interfaces)
                        break
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            logger.error(f"服务注册最终失败 after {self.max_retries} attempts: {e}")
                        else:
                            logger.warning(f"服务注册尝试 #{attempt + 1} 失败: {e}, {self.retry_delay}s后重试")
                            time.sleep(self.retry_delay)
            except Exception as e:
                logger.error(f"扫描包 {package} 时发生错误: {e}")

    def _get_local_ip(self) -> str:
        """获取本地IP地址"""
        import socket

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _convert_to_schema(self, param_schema_list: list) -> list:
        """将python接口获取的信息转为标准格式"""
        converted_list = []
        for param in param_schema_list:
            converted_list.append(FieldAdapter.adapter(param))
        return converted_list

    def register(self, interfaces: List[Dict[str, Any]]):
        final_payload = []
        base_payload = {
            "appName": self.app_name,
            "appCnName": self.app_cn_name,
            "ip": self.ip,
            "hostName": self.host_name,
            "aserviceType": AServiceType.HTTP.value, # 注意，这里key需要使用aserviceType来映射到AServiceType
        }
        """向注册中心注册服务实例及增强的接口信息"""
        # 提取所有接口的模型信息
        for context in interfaces:

            payload = {
                "name": context.get("name"),  # 服务名
                "serviceName": context.get("path"),  # url path地址
                "description": context.get("desc", ""),
                "methodType": context.get("http_method", "").upper(),  # 全部转大写
                "reqParamSchema": json.dumps(self._convert_to_schema(context.get("parameters", [])),
                                             separators=(',', ':'), # 紧凑型
                                             ensure_ascii=False),
                "respParamSchema": json.dumps(self._convert_to_schema(context.get("return_info", {}).get("fields", [])),
                                              separators=(',', ':'),  # 紧凑型
                                              ensure_ascii=False),
            }
            payload.update(base_payload)
            final_payload.append(payload)

        str_final_payload = json.dumps(final_payload, separators=(',', ':'), ensure_ascii=False)
        # 批量调用
        try:
            # 生成签名
            signature = self.a_signature.generate_signature(
                self.credential,
                str_final_payload,
            )
            headers = {
                "Content-Type": "application/json",
                "X-A-Signature": signature,
            }

            self._register_to_custom_registry(headers, str_final_payload)
        except requests.exceptions.RequestException as e:
            logger.error(f"连接注册中心失败: {e}, payload: {final_payload}")

    def _register_to_custom_registry(self, headers, payload: str):
        """注册到自定义注册中心"""
        logger.debug(f'''
url: {self.base_url}
header: {headers}
payload: {payload}''')
        try:
            response = requests.post(self.base_url, data=payload, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                if response.json().get("status") == 0:
                    logger.info(f"服务 {self.app_name} 成功注册到自定义注册中心。")
                else:
                    logger.error(f"服务 {self.app_name} 注册失败，错误信息: {response.text}")
            else:
                logger.error(
                    f"服务 {self.app_name} 注册到自定义注册中心失败，状态码: {response.status_code}, 错误信息: {response.text}"
                )
        except requests.exceptions.Timeout:
            logger.error(f"服务注册超时: {self.base_url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"无法连接到注册中心: {self.base_url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"服务注册请求异常: {e}")

    def _get_host_name(self) -> str:
        """获取主机名"""
        import socket
        try:
            return socket.gethostname()
        except Exception:
            return "localhost"


if __name__ == "__main__":
    registrar = EnhancedServiceRegistrar()
