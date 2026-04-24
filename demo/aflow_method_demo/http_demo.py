import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from aflow_client_python import ASignature
from aflow_client_python.models.enums import OperateType, ValuePathType
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv(".env")
load_dotenv("../.env")

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
        "thirdFlowCode": "SALES_ORDER",
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
        "thirdFlowCode": "SALES_ORDER",
        # "updateDesc": "初始版本上线"
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


def query_by_order_id():
    """
    基于任务单号进行查询
    """
    url = f"{base_url}/aflow/api/order/open/query_by_order_id"

    payload = {"orderId": "2602250000000013"}  # 订单 ID，必填参数

    str_params = json.dumps(payload, separators=(',', ':'))
    print(str_params)
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(str_params),
        # "X-A-Signature": sig_generator.create_signature(str(params.get("orderId"))),
    }

    try:
        print(url)
        ret = requests.get(url, params=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def all_order_list():
    """
    查询全量订单列表
    """
    url = f"{base_url}/aflow/api/order/open/allList"
    payload = {
        "page.index": "1",
        "page.size": "10",
        "orderStatus": "ing"
    }

    str_params = json.dumps(payload, separators=(',', ':'))
    headers = {
        "Content-Type": "application/json",
        "X-A-Signature": sig_generator.create_signature(str_params),
    }

    try:
        ret = requests.get(url, params=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def query_user_by_user_code():
    """
    根据用户编码查询用户详情
    """
    url = f"{base_url}/aflow/api/user/query_by_user_code"
    payload = {"userCode": "10000131"}

    str_params = json.dumps(payload, separators=(',', ':'))
    headers = {
        "Content-Type": "application/json",
        "X-A-Signature": sig_generator.create_signature(str_params),
    }

    try:
        ret = requests.get(url, params=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def handle_flow():
    """
    通过定义标准的formData对任务订单进行处理，formData中根据表单中定义的唯一key进行赋值
    OperateType 可填类型：
    	ACCEPT("accept", "领取"),
        PASS("pass", "处理"),
        TRANSFER("transfer", "转交"),
        REBUT("rebut", "驳回"),
        REJECT("reject", "拒绝"),
        REVOKE("revoke", "撤销"),
        CC("cc", "抄送"),

        URGE("urge", "催办"),
        REMARK("remark", "备注"),
    """
    url = f"{base_url}/aflow/api/order/open/handle_flow"
    # 必填项：handleParam 和 formData
    handle_param = {
        "customUserCode": "11000011111",  # 操作人(贵公司-用户编码)-必传，贵公司Odoo系统的用户ID
        "orderId": "2602250000000052",  # 必填：订单 ID
        # "taskOrderId": 'b604a8ff-7fb6-4c40-9dfa-4b4cbd671660',  # 可选：当用户可能多个任务节点时-必传 ID
        "operateType": OperateType.PASS,  # 必填：操作类型
        "remark": "审批通过",  # 可选：处理备注
        # "acceptUserCode": "user001",  # 可选：转交给谁(贵公司-用户编码)
        # "ccUserCode": ["user002"],  # 可选：抄送人用户编码列表
        # "ccContent": "请知悉",  # 可选：抄送内容
    }

    form_data = {
        "values": [
            {
                "name": "handleResult",
                "value": {
                    "type": "string",
                    "data": "完成"
                },
                "children": []
            },
            {
                "name": "processes",
                "value": {
                    "type": "string",
                    "data": "没什么问题，通过审批"
                }
            }
        ]
    }

    # 构造请求体
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


def handle_flow_by_object():
    """
    通过通用的formData对任务订单进行处理，formData中的字段通过propertyMapping进行映射配置
    OperateType 可填类型：
    	ACCEPT("accept", "领取"),
        PASS("pass", "处理"),
        TRANSFER("transfer", "转交"),
        REBUT("rebut", "驳回"),
        REJECT("reject", "拒绝"),
        REVOKE("revoke", "撤销"),
        CC("cc", "抄送"),
        URGE("urge", "催办"),
        REMARK("remark", "备注"),
    ValuePathType 可填：
    	RANGE_FROM("rangeFrom", "开始时间"),
        RANGE_TO("rangeTo", "结束时间"),
        OPTION_LABEL("optionLabel", "名称"),
        OPTION_VALUE("optionValue", "值"),
        URL_NAME("urlName", "名称"),
        URL_PATH("urlPath", "地址"),
        NONE_PATH("", "无");
    """
    url = f"{base_url}/aflow/api/order/open/handle_flow_by_object"
    # 必填项：handleParam 和 formData
    handle_param = {
        "customUserCode": "11000011111",  # 操作人(贵公司-用户编码)-必传，贵公司Odoo系统的用户ID
        "orderId": 2602280000000014,  # 必填：订单 ID
        # "taskOrderId": 789012,  # 可选：当用户可能多个任务节点时-必传 ID
        "operateType": OperateType.PASS,  # 必填：操作类型
        "remark": "审批通过",  # 可选：处理备注
        # "acceptUserCode": "user001",  # 可选：转交给谁(贵公司-用户编码)
        # "ccUserCode": ["user002"],  # 可选：抄送人用户编码列表
        # "ccContent": "请知悉",  # 可选：抄送内容
        # "userCode": "operator001"  # 必填：操作人(aiFlow用户编码)
    }

    form_data = {
        "approveResult": "完成", # 审批
        "approveRemark": "已确认，可以进行"  # 审批意见
    }

    property_mapping = [  # 可选：字段映射配置
        {
            "fieldFullName": "handleResult",# 必填，简单字段可以和fieldName相同，多级字段的话，需要拼接完整路径
            "fieldName": "handleResult",
            "visible": True,  # 是否可见
            "valuePath": ValuePathType.OPTION_VALUE,  # 可选：字段值路径
            "propertyPath": "approveResult",  # form_data中的key值
            # "valuePropertyPath": "url",
            # 不包括全路径、只是对应ValuePathType的属性, 如images.url 、 PropertyPath==images.url ，ValuePropertyPath == url
        },
        {
            "fieldFullName": "processes",
            "fieldName": "processes",
            "visible": True,  # 是否可见
            "valuePath": ValuePathType.NONE_PATH,  # 可选：字段值路径
            "propertyPath": "approveRemark",  # form_data中的key值
            # "valuePropertyPath": "url",
            # 不包括全路径、只是对应ValuePathType的属性, 如images.url 、 PropertyPath==images.url ，ValuePropertyPath == url
        },
    ]

    # 构造请求体
    payload = {
        "handleParam": handle_param,
        "formData": json.dumps(form_data),
        "propertyMapping": property_mapping
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
    # print(sync_task())
    # print(query_by_order_id())
    # print(all_order_list())
    # print(query_user_by_user_code())
    # print(handle_flow())
    print(handle_flow_by_object())
