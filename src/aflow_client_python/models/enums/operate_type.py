

class OperateType:
    """
    流程操作类型枚举

    operateType 可填类型：
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

    ACCEPT = "accept"
    PASS = "pass"
    TRANSFER = "transfer"
    REBUT = "rebut"
    REJECT = "reject"
    REVOKE = "revoke"
    CC = "cc"
    URGE = "urge"
    REMARK = "remark"


if __name__ == '__main__':
    # 使用示例
    operate_type = OperateType.PASS
