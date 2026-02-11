from pydantic import BaseModel, Field
from typing import List


class Department(BaseModel):
    """部门信息模型"""
    dept_id: str = Field(..., alias="deptId", description="部门ID")
    dept_name: str = Field(..., alias="deptName", description="部门名称")
    order_num: int = Field(..., alias="orderNum", description="排序号")
    status: int = Field(..., description="状态(1:启用, 0:禁用)")
