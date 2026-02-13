import os
# os.environ["LOG_LEVEL"] = "DEBUG"

import requests
import json
from typing import List

# 尝试相对导入，如果失败则使用绝对导入
try:
    from ..models import (
        DepartmentSyncItem,
        SyncResult,
        SyncFailDetail,
        UserSyncItem,
        BindUserReq,
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
    )
    from ..utils import logger
    from ..utils.sign import ASignature
except ImportError:
    import sys
    import os

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    from aflow_client_python.models import (
        DepartmentSyncItem,
        SyncResult,
        SyncFailDetail,
        UserSyncItem,
        BindUserReq,
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
    )
    from aflow_client_python.utils import logger
    from aflow_client_python.utils.sign import ASignature


class AFlowClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("AIFLOW_DOMAIN", "")
        self.sig_generator = ASignature()
        self.logger = logger.get_logger()

    def _make_request(self, url: str, payload: dict) -> dict:
        """通用请求方法，处理签名和发送请求"""
        headers = {
            "Content-Type": "application/json",
            "X-A-Signature": self.sig_generator.create_signature(json.dumps(payload))
        }
        self.logger.debug(f"Headers: {headers}")  # 添加这一行用于调试
        self.logger.debug(f"Payload: {payload}")  # 添加这一行用于调试
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"请求失败，状态码: {response.status_code}， 响应内容: {response.text}")
                return {}
        except Exception as e:
            self.logger.error(f"请求失败！错误信息: {e}")
            return {}

    def sync_department(self, departments: List[DepartmentSyncItem]) -> dict:
        """同步部门信息"""
        url = f"{self.base_url}/aflow/api/sys/sync/department"
        payload = {"departments": [dept.model_dump(by_alias=True) for dept in departments]}
        return self._make_request(url, payload)

    def sync_user(self, users: List[UserSyncItem]) -> dict:
        """同步用户信息"""
        url = f"{self.base_url}/aflow/api/sys/sync/user"
        payload = {"users": [user.model_dump(by_alias=True) for user in users]}
        return self._make_request(url, payload)

    def bind_user(self, bind_user_req: BindUserReq) -> dict:
        """绑定用户"""
        url = f"{self.base_url}/aflow/api/auth/bind"
        payload = bind_user_req.model_dump(by_alias=True)
        return self._make_request(url, payload)

    def create_third_party(self, flow_data: ThirdPartyFlowCreateReq) -> dict:
        """创建第三方流程"""
        url = f"{self.base_url}/aflow/api/flow/create_third_party"
        payload = flow_data.model_dump(by_alias=True)
        return self._make_request(url, payload)

    def online_third_party(self, flow_data: ThirdPartyFlowOnlineReq) -> dict:
        """上线第三方流程"""
        url = f"{self.base_url}/aflow/api/flow/online_third_party"
        payload = flow_data.model_dump(by_alias=True)
        return self._make_request(url, payload)

    def sync_task(self, task_data: ThirdPartyTaskSyncReq) -> dict:
        """同步任务信息"""
        url = f"{self.base_url}/aflow/api/order/sync/task"
        payload = task_data.model_dump(by_alias=True)
        return self._make_request(url, payload)


if __name__ == '__main__':

    import pprint
    import dotenv
    dotenv.load_dotenv("/Users/aiden/wrk/ad/aflow-client-python/demo/.env")

    aflow_client = AFlowClient()

    third_party_online_req = ThirdPartyFlowOnlineReq(
        third_flow_code="SALES_ORDER",
        update_desc="初始版本上线"
    )
    ret = aflow_client.online_third_party(third_party_online_req)
    pprint.pp(ret)
