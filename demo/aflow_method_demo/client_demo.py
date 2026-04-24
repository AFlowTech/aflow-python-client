import json
import os
import pprint
from datetime import datetime

from aflow_client_python import AFlowClient
from aflow_client_python.models import (
    DepartmentSyncItem, UserSyncItem, BindUserReq,
    ThirdPartyFlowCreateReq, AllowedApplyRule, ThirdPartyFlowUrl,
    ThirdPartyFlowOnlineReq,
    ThirdPartyTaskSyncReq, ThirdPartyTaskSyncCcUser, ThirdPartyTaskSyncTask,
    QueryOrderParam,
    OrderListQueryParam,
    QueryUserParam,
    HandleFlowReq,
    AHandleParam,
    AValue,
    AFieldValue,
    AFormData,
    PropertyMappingConfig,
    HandleFlowByObjectReq,
)
from aflow_client_python.models.enums import OperateType, ValuePathType
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv("../.env")

aflow_client = AFlowClient()


def sync_department():
    departments = [
        DepartmentSyncItem(
            dept_id="0",
            dept_name="根部门",
            order_num=1,
            status=1
        ),
        DepartmentSyncItem(
            dept_id="1",
            dept_name="第二个跟部门",
            order_num=2,
            status=1,
        ),
    ]
    ret = aflow_client.sync_department(departments)
    pprint.pp(ret)


def sync_user():
    users = [
        UserSyncItem(
            user_id="11000011111",
            user_name="张三",
            real_name="张三",
            mobile="18888888888",
            email="zhangsan@a.com",
            dept_id="0",
            personnel_type=1,
            direct_supervisor="",
            status=1
        ),
    ]

    ret = aflow_client.sync_user(users)
    pprint.pp(ret)


def bind_user():
    bind_user_req = BindUserReq(
        customUserCode="11000011111",  # 贵公司Odoo系统的用户ID
        phone_number="18888888888",  # 和飞书用户ID二选一
    )

    result = aflow_client.bind_user(bind_user_req)
    pprint.pp(result)


def create_third_party():
    third_party_req = ThirdPartyFlowCreateReq(
        title="销售订单审批流程",
        initiateUrl=ThirdPartyFlowUrl(
            h5Url="https://odoo.example.com/h5/sales/apply",
            webUrl="https://odoo.example.com/web/sales/apply"
        ),
        detailUrl=ThirdPartyFlowUrl(
            h5Url="https://odoo.example.com/h5/sales/detail",
            webUrl="https://odoo.example.com/web/sales/detail"
        ),
        categoryId="GROUP001",
        managerUserCode="11000011111",  # 贵公司Odoo系统的用户ID
        operationUserCode="11000011111",  # 贵公司Odoo系统的用户ID
        configUserCode="11000011111",  # 贵公司Odoo系统的用户ID
        createBy="11000011111",  # 贵公司Odoo系统的用户ID
        allowedApplyTerminals=["pc", "mobile"],
        allowedApplyRule=AllowedApplyRule(
            allowedApplyType="all"
        ),
        allowedManageRule=AllowedApplyRule(
            allowedApplyType="all"
        )
    )

    ret = aflow_client.create_third_party(third_party_req)
    pprint.pp(ret)


def online_third_party():
    third_party_online_req = ThirdPartyFlowOnlineReq(
        third_flow_code="SALES_ORDER",
        update_desc="初始版本上线"
    )
    ret = aflow_client.online_third_party(third_party_online_req)
    pprint.pp(ret)


def sync_task():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deadline = (datetime.now().replace(hour=18, minute=0, second=0)).strftime("%Y-%m-%d %H:%M:%S")

    task_sync_req = ThirdPartyTaskSyncReq(
        third_order_id=123456,
        order_status="ing",
        order_result="ing",
        initiator="11000011111",  # 贵公司Odoo系统的用户ID
        version=1,
        business_key="SALES_ORDER_20250124001",
        create_time=now,
        update_time=now,
        cc_users=[
            ThirdPartyTaskSyncCcUser(
                user_code="11000011111",  # 贵公司Odoo系统的用户ID
                cc_time=now
            )
        ],
        tasks=[
            ThirdPartyTaskSyncTask(
                third_task_id="TASK001",
                task_name="部门经理审批",
                assignee_user_code=["11000011111"],  # 贵公司Odoo系统的用户ID
                task_status="new",
                task_result="new",
                dead_line=deadline,
                node_type="audit",
                show_pc=True,
                show_mobile=True
            )
        ]
    )

    ret = aflow_client.sync_task(task_sync_req)
    pprint.pp(ret)


def query_by_order_id():
    query_order_req = QueryOrderParam(
        order_id="2602250000000014"
    )
    ret = aflow_client.query_by_order_id(query_order_req)
    pprint.pp(ret)


def all_order_list():
    order_list_query = OrderListQueryParam(
        page_index=1,
        page_size=10,
        order_status="ing"
    )
    ret = aflow_client.all_order_list(order_list_query)
    pprint.pp(ret)


def query_user_by_user_code():
    query_user_req = QueryUserParam(
        user_code="10016893"
    )
    ret = aflow_client.query_user_by_user_code(query_user_req)
    pprint.pp(ret)


def handle_flow():
    """
    operateType可填类型：
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
    handle_flow_req = HandleFlowReq(
        handle_param=AHandleParam(
            custom_user_code="11000011111",
            order_id="2602250000000053",
            operate_type=OperateType.PASS,
        ),
        form_data=AFormData(
            values=[
                AFieldValue(
                    name="process_001",
                    value=AValue(
                        type="string",
                        data="通过"
                    )
                )
            ]
        ),
    )
    ret = aflow_client.handle_flow(handle_flow_req)
    pprint.pp(ret)


def handle_flow_by_object():
    """
    operateType可填类型：
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
    form_data = {
        "approveResult": "完成",  # 审批
        "approveRemark": "已确认，可以进行"  # 审批意见
    }

    handle_flow_req = HandleFlowByObjectReq(
        handle_param=AHandleParam(
            custom_user_code="11000011111",
            order_id="2602280000000015",
            operate_type=OperateType.PASS,
        ),
        form_data=json.dumps(form_data),
        property_mapping=[
            PropertyMappingConfig.model_construct(
                field_full_name="handleResult",
                field_name="handleResult",
                visible=True,
                value_path=ValuePathType.OPTION_VALUE,
                property_path="approveResult",
                # 不包括全路径、只是对应ValuePathType的属性, 如images.url 、 PropertyPath==images.url ，ValuePropertyPath == url
            ),
            PropertyMappingConfig.model_construct(
                field_full_name="processes",
                field_name="processes",
                visible=True,
                value_path=ValuePathType.NONE_PATH,
                property_path="approveRemark",
                # 不包括全路径、只是对应ValuePathType的属性, 如images.url 、 PropertyPath==images.url ，ValuePropertyPath == url
            )
        ]
    )
    ret = aflow_client.handle_flow_by_object(handle_flow_req)
    pprint.pp(ret)




if __name__ == '__main__':
    # print(os.getenv("APP_ID"))
    # sync_department()
    sync_user()
    # bind_user()
    # create_third_party()
    # online_third_party()
    # sync_task()
    # query_by_order_id()
    # all_order_list()
    # query_user_by_user_code()
    # handle_flow()
    # handle_flow_by_object()
