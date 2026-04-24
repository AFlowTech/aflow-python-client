from typing import Optional

from pydantic import Field

from ..base import AFlowBaseModel


class DepartmentSyncItem(AFlowBaseModel):
    """部门信息模型"""

    dept_id: str = Field(..., alias="deptId", description="部门ID")
    dept_name: str = Field(..., alias="deptName", description="部门名称")
    parent_id: Optional[str] = Field(None, alias="parentId", description="上级部门名称，可选")
    dept_code: Optional[str] = Field(None, alias="deptCode", description="部门编码，可选")
    order_num: int = Field(..., alias="orderNum", description="排序号")
    status: int = Field(..., description="状态(1:启用, 0:禁用)")
