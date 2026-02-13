# 显式导入 sync 子模块的类
from .sync import DepartmentSyncItem, SyncResult, SyncFailDetail, UserSyncItem

# 显式导入 third_party 子模块的类
from .third_party import (
    ThirdPartyFlowBase,
    ThirdPartyFlowUrl,
    ThirdPartyFlowCreateReq,
    AllowedApplyRule,
    ThirdPartyFlowOnlineReq,
    ThirdPartyTaskSyncCcUser,
    ThirdPartyTaskSyncTask,
    ThirdPartyTaskSyncReq
)

# 定义 __all__，控制对外暴露的内容
__all__ = [
    "DepartmentSyncItem",
    "SyncResult",
    "SyncFailDetail",
    "UserSyncItem",
    "ThirdPartyFlowBase",
    "ThirdPartyFlowUrl",
    "ThirdPartyFlowCreateReq",
    "AllowedApplyRule",
    "ThirdPartyFlowOnlineReq",
    "ThirdPartyTaskSyncCcUser",
    "ThirdPartyTaskSyncTask",
    "ThirdPartyTaskSyncReq"
]
