

# 尝试相对导入，如果失败则使用绝对导入
try:
    from ..models import (
        DepartmentSyncItem,
        SyncResult,
        SyncFailDetail,
        UserSyncItem,
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
    )
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
        ThirdPartyFlowBase,
        ThirdPartyFlowCreateReq,
        ThirdPartyFlowOnlineReq,
        ThirdPartyFlowUrl,
        AllowedApplyRule,
        ThirdPartyTaskSyncCcUser,
        ThirdPartyTaskSyncTask,
        ThirdPartyTaskSyncReq,
    )
