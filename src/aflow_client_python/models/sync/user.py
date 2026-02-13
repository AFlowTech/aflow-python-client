from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserSyncItem(BaseModel):
    """
    用户同步项
    """
    model_config = ConfigDict(populate_by_name=True)  # 允许通过字段名初始化

    user_id: str = Field(..., alias="userId", description="用户ID（外部系统）")
    user_name: str = Field(..., alias="userName", description="用户名")
    real_name: str = Field(..., alias="realName", description="真实姓名")
    email: str = Field(..., alias="email", description="邮箱")
    mobile: str = Field(..., alias="mobile", description="手机号")
    dept_id: str = Field(..., alias="deptId", description="部门ID（外部系统）")
    personnel_type: int = Field(1, alias="personnelType", description="人员类型：1-正式，2-实习，3-外包，4-劳务，5-顾问（默认1）")
    direct_supervisor: Optional[str] = Field(None, alias="directSupervisor", description="直接上级用户ID（外部系统，最大Boss可为空）")
    status: int = Field(1, alias="status", description="状态：1-启用，0-禁用（默认1）")
