"""AFlow客户端使用示例 - 基于Pydantic模型"""

import os
from datetime import datetime
from dotenv import load_dotenv
from aflow_client_python import (
    AFlowClient,
    Department,
    User,
    UrlConfig,
    TaskInfo,
    CCUser,
    AllowedRule
)

# 加载环境变量
load_dotenv(".env")
load_dotenv("../.env")

def demo_sync_departments():
    """同步部门示例 - 使用Pydantic模型"""
    client = AFlowClient()
    
    # 使用Pydantic模型创建部门数据
    departments = [
        Department(
            dept_id="0",
            dept_name="根部门",
            order_num=1,
            status=1,
        ),
        Department(
            dept_id="1",
            dept_name="第二个跟部门",
            order_num=2,
            status=1,
        ),
    ]
    
    try:
        result = client.sync_departments(departments)
        print("✅ 同步部门成功:", result)
    except Exception as e:
        print("❌ 同步部门失败:", str(e))

def demo_sync_users():
    """同步用户示例 - 使用Pydantic模型"""
    client = AFlowClient()
    
    # 使用Pydantic模型创建用户数据
    users = [
        User(
            user_id="11000011111",
            user_name="张三",
            real_name="张三",
            email="zhangsan@a.com",
            dept_id="0",
            personnel_type=1,
            direct_supervisor="",
            status=1
        )
    ]
    
    try:
        result = client.sync_users(users)
        print("✅ 同步用户成功:", result)
    except Exception as e:
        print("❌ 同步用户失败:", str(e))

def demo_bind_user():
    """绑定用户示例"""
    client = AFlowClient()
    
    try:
        result = client.bind_user("11000011111", "feishu_user_12345")
        print("✅ 绑定用户成功:", result)
    except Exception as e:
        print("❌ 绑定用户失败:", str(e))

def demo_create_third_party_flow():
    """创建第三方流程示例 - 使用Pydantic模型"""
    client = AFlowClient()
    
    try:
        # 使用Pydantic模型创建URL配置
        initiate_url = UrlConfig(
            h5_url="https://odoo.example.com/h5/sales/apply",
            web_url="https://odoo.example.com/web/sales/apply"
        )
        
        detail_url = UrlConfig(
            h5_url="https://odoo.example.com/h5/sales/detail",
            web_url="https://odoo.example.com/web/sales/detail"
        )
        
        result = client.create_third_party_flow(
            title="销售订单审批流程",
            initiate_url=initiate_url,
            detail_url=detail_url,
            category_id="GROUP001",
            manager_user_code="11000011111",
            operation_user_code="11000011111",
            config_user_code="11000011111",
            create_by="11000011111"
        )
        print("✅ 创建流程成功:", result)
    except Exception as e:
        print("❌ 创建流程失败:", str(e))

def demo_online_third_party_flow():
    """上线第三方流程示例"""
    client = AFlowClient()
    
    try:
        result = client.online_third_party_flow("SALES_ORDER", 1, "初始版本上线")
        print("✅ 上线流程成功:", result)
    except Exception as e:
        print("❌ 上线流程失败:", str(e))

def demo_sync_task():
    """同步任务示例 - 使用Pydantic模型"""
    client = AFlowClient()
    
    # 计算截止时间
    deadline = datetime.now().replace(hour=18, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 使用Pydantic模型创建任务数据
        tasks = [
            TaskInfo(
                third_task_id="TASK001",
                task_name="部门经理审批",
                assignee_user_code=["11000011111"],
                task_status="new",
                task_result="new",
                dead_line=deadline,
                node_type="audit",
                show_pc=True,
                show_mobile=True
            )
        ]
        
        cc_users = [
            CCUser(
                user_code="11000011111",
                cc_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        ]
        
        result = client.sync_task(
            third_order_id=123456,
            order_status="ing",
            order_result="ing",
            initiator="11000011111",
            version=1,
            business_key="SALES_ORDER_20250124001",
            cc_users=cc_users,
            tasks=tasks
        )
        print("✅ 同步任务成功:", result)
    except Exception as e:
        print("❌ 同步任务失败:", str(e))

def demo_model_validation():
    """演示Pydantic模型的验证功能"""
    print("=== Pydantic模型验证演示 ===")
    
    # 正确的数据
    try:
        dept = Department(
            dept_id="0",
            dept_name="测试部门",
            order_num=1,
            status=1
        )
        print("✅ 部门模型验证通过:", dept.dict(by_alias=True))
    except Exception as e:
        print("❌ 部门模型验证失败:", str(e))
    
    # 错误的数据 - 类型不匹配
    try:
        invalid_dept = Department(
            dept_id="0",
            dept_name="测试部门",
            order_num="not_a_number",  # 应该是int类型
            status=1
        )
        print("这行不应该被执行")
    except Exception as e:
        print("✅ 捕获到类型错误:", str(e))
    
    # 错误的数据 - 缺少必填字段
    try:
        incomplete_dept = Department(
            dept_id="0",
            dept_name="测试部门"
            # 缺少order_num和status
        )
        print("这行不应该被执行")
    except Exception as e:
        print("✅ 捕获到缺少必填字段错误:", str(e))

def demo_custom_base_url():
    """自定义基础URL示例"""
    # 可以指定不同的基础URL
    client = AFlowClient(base_url="https://custom-api.aiflow.com")
    
    departments = [
        Department(
            dept_id="0",
            dept_name="测试部门",
            order_num=1,
            status=1,
        )
    ]
    
    try:
        result = client.sync_departments(departments)
        print("✅ 自定义URL同步部门成功:", result)
    except Exception as e:
        print("❌ 自定义URL同步部门失败:", str(e))

if __name__ == '__main__':
    print("🚀 AFlow客户端使用示例 (Pydantic版本)")
    print("=" * 50)
    
    # 运行各个示例
    demo_model_validation()  # 先演示模型验证
    print()
    
    # demo_sync_departments()
    # demo_sync_users()
    # demo_bind_user()
    # demo_create_third_party_flow()
    # demo_online_third_party_flow()
    demo_sync_task()
    # demo_custom_base_url()
    
    print("\n🎉 示例运行完成")