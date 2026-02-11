import os

from aflow_client_python import ASignature
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv(".env")

sig_generator = ASignature()
base_url = os.getenv("AIFLOW_DOMAIN", "")


def sync_department():
    url = f"{base_url}/aflow/api/sys/sync/department"
    payload = {"departments": [
        dict(
            deptId="0",
            deptName="根部门",
            orderNum=1,
            status=1,
        ),
        dict(
            deptId="1",
            deptName="第二个跟部门",
            orderNum=2,
            status=1,
        ),
    ]}

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def sync_user():
    url = f"{base_url}/aflow/api/sys/sync/user"
    payload = {
        "users": [
            {
                "userId": "11000011111",
                "userName": "张三",
                "realName": "张三",
                "email": "zhangsan@a.com",
                "deptId": "0",
                "personnelType": 1,
                "directSupervisor": "",
                "status": 1
            }
        ]
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def bind_user():
    url = f"{base_url}/aflow/api/auth/bind"
    payload = {
        "customUserCode": "11000011111",  # 贵公司Odoo系统的用户ID
        "phoneNumber": "18888888888",  # 和飞书用户ID二选一
        # "linkUserCode": "feishu_user_12345"  # 飞书用户ID（如果已集成飞书）
    }

    print(json.dumps(payload, ensure_ascii=False))

    headers = {
        "Content-Type": "application/json",
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload))
    }
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.text


def create_third_party():
    url = f"{base_url}/aflow/api/flow/create_third_party"
    payload = {
        "title": "销售订单审批流程",
        "initiateUrl": {
            "h5Url": "https://odoo.example.com/h5/sales/apply",
            "webUrl": "https://odoo.example.com/web/sales/apply"
        },
        "detailUrl": {
            "h5Url": "https://odoo.example.com/h5/sales/detail",
            "webUrl": "https://odoo.example.com/web/sales/detail"
        },
        "categoryId": "GROUP001",
        "managerUserCode": "11000011111",  # 贵公司Odoo系统的用户ID
        "operationUserCode": "11000011111",  # 贵公司Odoo系统的用户ID
        "configUserCode": "11000011111",  # 贵公司Odoo系统的用户ID
        "createBy": "11000011111",  # 贵公司Odoo系统的用户ID
        "allowedApplyTerminals": ["pc", "mobile"],
        "allowedApplyRule": {
            "allowedApplyType": "all"
        },
        "allowedManageRule": {
            "allowedApplyType": "all"
        }
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def online_third_party():
    url = f"{base_url}/aflow/api/flow/online_third_party"
    payload = {
        "flowCode": "SALES_ORDER",
        "flowVersion": 1,
        "updateDesc": "初始版本上线"
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def sync_task():
    url = f"{base_url}/aflow/api/order/sync/task"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deadline = (datetime.now().replace(hour=18, minute=0, second=0)).strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "thirdOrderId": 123456,
        "thirdFlowCode": "SALES_ORDER",
        "orderStatus": "ing",
        "orderResult": "ing",
        "initiator": "11000011111",  # 贵公司Odoo系统的用户ID
        "version": 1,
        "businessKey": "SALES_ORDER_20250124001",
        "createTime": now,
        "updateTime": now,
        "ccUsers": [
            {
                "userCode": "11000011111",  # 贵公司Odoo系统的用户ID
                "ccTime": now
            }
        ],
        "tasks": [
            {
                "thirdTaskId": "TASK001",
                "taskName": "部门经理审批",
                "assigneeUserCode": ["11000011111"],  # 贵公司Odoo系统的用户ID
                "taskStatus": "new",
                "taskResult": "new",
                "deadLine": deadline,
                "nodeType": "audit",
                "showPc": True,
                "showMobile": True
            }
        ]
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def handle_flow():
    url = f"{base_url}/aflow/api/order/open/handle_flow"

    # 构造请求参数
    handle_param = {
        "orderId": 123456789,  # 流程订单编码
        "taskOrderId": "TASK_001",  # 任务ID
        "operateType": "pass",  # 操作类型，参考 AFlowOperatorType 枚举
        "customUserCode": "USER_001",  # 操作人编码
        "remark": "处理备注信息"  # 处理备注
    }

    form_data = {
        "values": [
            {"fieldId": "field1", "value": "value1"},
            {"fieldId": "field2", "value": "value2"}
        ]
    }

    payload = {
        "handleParam": handle_param,
        "formData": form_data
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    if not os.getenv("APP_ID", ""):
        raise Exception("未能从系统变量中加载必要参数，请检查后再试")
    # print(sync_department())
    # print(sync_user())
    # print(bind_user())
    # print(create_third_party())
    # print(online_third_party())
    print(sync_task())
