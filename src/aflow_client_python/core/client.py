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
        OrderListQueryParam,
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
        QueryOrderParam,
        QueryUserParam,
        HandleFlowReq,
        HandleFlowByObjectReq

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
        OrderListQueryParam,
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
        QueryOrderParam,
        QueryUserParam,
        HandleFlowReq,
        HandleFlowByObjectReq
    )
    from aflow_client_python.utils import logger
    from aflow_client_python.utils.sign import ASignature


class AFlowClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("AIFLOW_DOMAIN", "")
        self.sig_generator = ASignature()
        self.logger = logger.get_logger()

    def _make_request(self, url: str, payload: dict, method: str = "POST") -> dict:
        """通用请求方法，处理签名和发送请求"""
        headers = {
            "Content-Type": "application/json",
        }

        self.logger.debug(f"Payload: {payload}")  # 添加这一行用于调试
        try:
            if method == 'POST':
                headers.update({"X-A-Signature": self.sig_generator.create_signature(json.dumps(payload))})
                self.logger.debug(f"Headers: {headers}")  # 添加这一行用于调试
                response = requests.post(url, json=payload, headers=headers)
            else:
                # 注意，对于GET方法，必须要压缩参数，否则由于空格的差异，会导致验签失败
                headers.update({"X-A-Signature": self.sig_generator.create_signature(json.dumps(payload, separators=(',', ':')))})
                self.logger.debug(f"Headers: {headers}")  # 添加这一行用于调试
                response = requests.get(url, params=payload, headers=headers)
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
        payload = {"departments": [self._model_to_dict(dept, by_alias=True) for dept in departments]}
        return self._make_request(url, payload)

    def sync_user(self, users: List[UserSyncItem]) -> dict:
        """同步用户信息"""
        url = f"{self.base_url}/aflow/api/sys/sync/user"
        payload = {"users": [self._model_to_dict(user, by_alias=True) for user in users]}
        return self._make_request(url, payload)

    def bind_user(self, bind_user_req: BindUserReq) -> dict:
        """绑定用户"""
        url = f"{self.base_url}/aflow/api/auth/bind"
        payload = self._model_to_dict(bind_user_req, by_alias=True)
        return self._make_request(url, payload)

    def create_third_party(self, flow_data: ThirdPartyFlowCreateReq) -> dict:
        """创建第三方流程"""
        url = f"{self.base_url}/aflow/api/flow/create_third_party"
        payload = self._model_to_dict(flow_data, by_alias=True)
        return self._make_request(url, payload)

    def online_third_party(self, flow_data: ThirdPartyFlowOnlineReq) -> dict:
        """上线第三方流程"""
        url = f"{self.base_url}/aflow/api/flow/online_third_party"
        payload = self._model_to_dict(flow_data, by_alias=True)
        return self._make_request(url, payload)

    def sync_task(self, task_data: ThirdPartyTaskSyncReq) -> dict:
        """同步任务信息"""
        url = f"{self.base_url}/aflow/api/order/sync/task"
        payload = self._model_to_dict(task_data, by_alias=True)
        return self._make_request(url, payload)

    def query_by_order_id(self, query_order_param: QueryOrderParam) -> dict:
        """同步任务信息"""
        url = f"{self.base_url}/aflow/api/order/open/query_by_order_id"
        payload = self._normalize_get_payload(self._model_to_dict(query_order_param, by_alias=True, exclude_none=True))
        return self._make_request(url, payload, "GET")

    def all_order_list(self, order_list_query: OrderListQueryParam) -> dict:
        """查询全量订单列表"""
        url = f"{self.base_url}/aflow/api/order/open/allList"
        payload = self._normalize_get_payload(self._model_to_dict(order_list_query, by_alias=True, exclude_none=True))
        return self._make_request(url, payload, "GET")

    def query_user_by_user_code(self, query_user_param: QueryUserParam) -> dict:
        """根据用户编码查询用户详情"""
        url = f"{self.base_url}/aflow/api/user/query_by_user_code"
        payload = self._normalize_get_payload(self._model_to_dict(query_user_param, by_alias=True, exclude_none=True))
        return self._make_request(url, payload, "GET")

    def handle_flow(self, handle_flow_req: HandleFlowReq):
        url = f"{self.base_url}/aflow/api/order/open/handle_flow"
        payload = self._model_to_dict(handle_flow_req, by_alias=True)
        return self._make_request(url, payload)

    def handle_flow_by_object(self, handle_flow_by_object_req: HandleFlowByObjectReq):
        url = f"{self.base_url}/aflow/api/order/open/handle_flow_by_object"
        payload = self._model_to_dict(handle_flow_by_object_req, by_alias=True)
        return self._make_request(url, payload)

    def _normalize_get_payload(self, payload: dict) -> dict:
        normalized = {}
        for key, value in payload.items():
            if value is None:
                continue
            if isinstance(value, list):
                normalized[key] = ",".join(str(item) for item in value)
            elif isinstance(value, bool):
                normalized[key] = "true" if value else "false"
            else:
                normalized[key] = str(value)
        return normalized

    def _model_to_dict(self, model, by_alias: bool = True, exclude_none: bool = False) -> dict:
        if hasattr(model, "model_dump"):
            return model.model_dump(by_alias=by_alias, exclude_none=exclude_none)
        if hasattr(model, "dict"):
            return model.dict(by_alias=by_alias, exclude_none=exclude_none)
        raise TypeError(f"Unsupported model type: {type(model)}")


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
