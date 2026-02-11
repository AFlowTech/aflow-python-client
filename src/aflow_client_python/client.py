"""AFlow API Client - 基于Pydantic的现代化API客户端"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from .utils.sign import ASignature
from .core.config import config_manager


# ==================== 数据模型定义 ====================

class Department(BaseModel):
    """部门信息模型"""
    dept_id: str = Field(..., alias="deptId", description="部门ID")
    dept_name: str = Field(..., alias="deptName", description="部门名称")
    order_num: int = Field(..., alias="orderNum", description="排序号")
    status: int = Field(..., description="状态(1:启用, 0:禁用)")


class User(BaseModel):
    """用户信息模型"""
    user_id: str = Field(..., alias="userId", description="用户ID")
    user_name: str = Field(..., alias="userName", description="用户名")
    real_name: str = Field(..., alias="realName", description="真实姓名")
    email: str = Field(..., description="邮箱地址")
    dept_id: str = Field(..., alias="deptId", description="所属部门ID")
    personnel_type: int = Field(..., alias="personnelType", description="人员类型")
    direct_supervisor: str = Field(..., alias="directSupervisor", description="直接上级")
    status: int = Field(..., description="状态(1:启用, 0:禁用)")


class UrlConfig(BaseModel):
    """URL配置模型"""
    h5_url: str = Field(..., alias="h5Url", description="H5页面URL")
    web_url: str = Field(..., alias="webUrl", description="Web页面URL")


class AllowedRule(BaseModel):
    """权限规则模型"""
    allowed_apply_type: str = Field("all", alias="allowedApplyType", description="允许申请类型")


class TaskInfo(BaseModel):
    """任务信息模型"""
    third_task_id: str = Field(..., alias="thirdTaskId", description="第三方任务ID")
    task_name: str = Field(..., alias="taskName", description="任务名称")
    assignee_user_code: List[str] = Field(..., alias="assigneeUserCode", description="处理人用户编码列表")
    task_status: str = Field(..., alias="taskStatus", description="任务状态")
    task_result: str = Field(..., alias="taskResult", description="任务结果")
    dead_line: str = Field(..., alias="deadLine", description="截止时间")
    node_type: str = Field(..., alias="nodeType", description="节点类型")
    show_pc: bool = Field(True, alias="showPc", description="是否显示PC端")
    show_mobile: bool = Field(True, alias="showMobile", description="是否显示移动端")


class CCUser(BaseModel):
    """抄送用户模型"""
    user_code: str = Field(..., alias="userCode", description="用户编码")
    cc_time: str = Field(..., alias="ccTime", description="抄送时间")


# ==================== 客户端核心类 ====================

class AFlowClient:
    """AFlow API客户端，基于Pydantic模型的现代化实现"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        """
        初始化AFlow客户端
        
        Args:
            base_url: AFlow服务的基础URL，如果为None则从环境变量读取
            timeout: 请求超时时间(秒)
        """
        self.base_url = base_url or config_manager.get("aiflow_domain")
        self.timeout = timeout
        self.sig_generator = ASignature()
        
    def _make_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送带签名的API请求
        
        Args:
            method: HTTP方法 ('POST')
            endpoint: API端点路径
            payload: 请求载荷
            
        Returns:
            API响应结果
            
        Raises:
            requests.RequestException: 网络请求异常
            ValueError: 响应格式错误
        """
        url = f"{self.base_url}{endpoint}"
        payload_json = json.dumps(payload, separators=(',', ':'))
        
        headers = {
            "Content-Type": "application/json",
            "X-A-Signature": self.sig_generator.create_signature(payload_json),
        }
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
                
            if response.status_code == 200:
                return response.json()
            else:
                raise requests.RequestException(f"API调用失败: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            raise requests.RequestException(f"AFlow API请求失败: {str(e)}")
    
    def sync_departments(self, departments: List[Department]) -> Dict[str, Any]:
        """
        同步部门信息
        
        Args:
            departments: 部门信息列表
            
        Returns:
            API响应结果
            
        Example:
            departments = [
                Department(
                    dept_id="0",
                    dept_name="根部门",
                    order_num=1,
                    status=1
                )
            ]
            client.sync_departments(departments)
        """
        # 转换为字典格式
        payload = {"departments": [dept.dict(by_alias=True) for dept in departments]}
        return self._make_request("POST", "/aflow/api/sys/sync/department", payload)
    
    def sync_users(self, users: List[User]) -> Dict[str, Any]:
        """
        同步用户信息
        
        Args:
            users: 用户信息列表
            
        Returns:
            API响应结果
            
        Example:
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
            client.sync_users(users)
        """
        payload = {"users": [user.dict(by_alias=True) for user in users]}
        return self._make_request("POST", "/aflow/api/sys/sync/user", payload)
    
    def bind_user(self, custom_user_code: str, link_user_code: Optional[str] = None) -> Dict[str, Any]:
        """
        绑定用户关系
        
        Args:
            custom_user_code: 自定义用户编码(如Odoo系统用户ID)
            link_user_code: 关联用户编码(如飞书用户ID，可选)
            
        Returns:
            API响应结果
            
        Example:
            client.bind_user("11000011111", "feishu_user_12345")
        """
        payload = {"customUserCode": custom_user_code}
        if link_user_code:
            payload["linkUserCode"] = link_user_code
            
        return self._make_request("POST", "/aflow/api/auth/bind", payload)
    
    def create_third_party_flow(self, 
                              title: str,
                              initiate_url: UrlConfig,
                              detail_url: UrlConfig,
                              category_id: str,
                              manager_user_code: str,
                              operation_user_code: str,
                              config_user_code: str,
                              create_by: str,
                              allowed_apply_terminals: List[str] = None,
                              allowed_apply_rule: Optional[AllowedRule] = None,
                              allowed_manage_rule: Optional[AllowedRule] = None) -> Dict[str, Any]:
        """
        创建第三方流程
        
        Args:
            title: 流程标题
            initiate_url: 发起页面URL配置
            detail_url: 详情页面URL配置
            category_id: 分类ID
            manager_user_code: 管理员用户编码
            operation_user_code: 运营用户编码
            config_user_code: 配置用户编码
            create_by: 创建人编码
            allowed_apply_terminals: 允许发起的终端(['pc', 'mobile'])
            allowed_apply_rule: 允许发起规则
            allowed_manage_rule: 允许管理规则
            
        Returns:
            API响应结果
            
        Example:
            client.create_third_party_flow(
                title="销售订单审批流程",
                initiate_url=UrlConfig(
                    h5_url="https://odoo.example.com/h5/sales/apply",
                    web_url="https://odoo.example.com/web/sales/apply"
                ),
                detail_url=UrlConfig(
                    h5_url="https://odoo.example.com/h5/sales/detail",
                    web_url="https://odoo.example.com/web/sales/detail"
                ),
                category_id="GROUP001",
                manager_user_code="11000011111",
                operation_user_code="11000011111",
                config_user_code="11000011111",
                create_by="11000011111"
            )
        """
        payload = {
            "title": title,
            "initiateUrl": initiate_url.dict(by_alias=True),
            "detailUrl": detail_url.dict(by_alias=True),
            "categoryId": category_id,
            "managerUserCode": manager_user_code,
            "operationUserCode": operation_user_code,
            "configUserCode": config_user_code,
            "createBy": create_by,
            "allowedApplyTerminals": allowed_apply_terminals or ["pc", "mobile"],
            "allowedApplyRule": allowed_apply_rule.dict(by_alias=True) if allowed_apply_rule else {"allowedApplyType": "all"},
            "allowedManageRule": allowed_manage_rule.dict(by_alias=True) if allowed_manage_rule else {"allowedApplyType": "all"}
        }
        
        return self._make_request("POST", "/aflow/api/flow/create_third_party", payload)
    
    def online_third_party_flow(self, flow_code: str, flow_version: int, update_desc: str = "") -> Dict[str, Any]:
        """
        上线第三方流程
        
        Args:
            flow_code: 流程编码
            flow_version: 流程版本号
            update_desc: 更新描述
            
        Returns:
            API响应结果
            
        Example:
            client.online_third_party_flow("SALES_ORDER", 1, "初始版本上线")
        """
        payload = {
            "flowCode": flow_code,
            "flowVersion": flow_version,
            "updateDesc": update_desc
        }
        
        return self._make_request("POST", "/aflow/api/flow/online_third_party", payload)
    
    def sync_task(self,
                  third_order_id: Union[int, str],
                  order_status: str,
                  order_result: str,
                  initiator: str,
                  version: int,
                  business_key: str,
                  create_time: Optional[str] = None,
                  update_time: Optional[str] = None,
                  cc_users: Optional[List[CCUser]] = None,
                  tasks: Optional[List[TaskInfo]] = None) -> Dict[str, Any]:
        """
        同步任务信息
        
        Args:
            third_order_id: 第三方订单ID
            order_status: 订单状态
            order_result: 订单结果
            initiator: 发起人编码
            version: 版本号
            business_key: 业务键
            create_time: 创建时间(格式: YYYY-MM-DD HH:MM:SS)
            update_time: 更新时间(格式: YYYY-MM-DD HH:MM:SS)
            cc_users: 抄送用户列表
            tasks: 任务列表
            
        Returns:
            API响应结果
            
        Example:
            from datetime import datetime
            
            deadline = datetime.now().replace(hour=18, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
            
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
            
            client.sync_task(
                third_order_id=123456,
                order_status="ing",
                order_result="ing",
                initiator="11000011111",
                version=1,
                business_key="SALES_ORDER_20250124001",
                tasks=tasks
            )
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_time = create_time or now
        update_time = update_time or now
        
        payload = {
            "thirdOrderId": third_order_id,
            "orderStatus": order_status,
            "orderResult": order_result,
            "initiator": initiator,
            "version": version,
            "businessKey": business_key,
            "createTime": create_time,
            "updateTime": update_time,
            "ccUsers": [cc.dict(by_alias=True) for cc in cc_users] if cc_users else [],
            "tasks": [task.dict(by_alias=True) for task in tasks] if tasks else []
        }
        
        return self._make_request("POST", "/aflow/api/order/sync/task", payload)


# 为了向后兼容，保留原来的类名
AFlowAPIClient = AFlowClient