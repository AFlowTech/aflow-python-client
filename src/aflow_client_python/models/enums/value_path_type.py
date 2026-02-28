

class ValuePathType:
    """
    值路径类型枚举
    
    valuePath 可填：
        RANGE_FROM("rangeFrom", "开始时间"),
        RANGE_TO("rangeTo", "结束时间"),
        OPTION_LABEL("optionLabel", "名称"),
        OPTION_VALUE("optionValue", "值"),
        URL_NAME("urlName", "名称"),
        URL_PATH("urlPath", "地址"),
        NONE_PATH("", "无");
    """

    RANGE_FROM = "RANGE_FROM"
    RANGE_TO = "RANGE_TO"
    OPTION_LABEL = "OPTION_LABEL"
    OPTION_VALUE = "OPTION_VALUE"
    URL_NAME = "URL_NAME"
    URL_PATH = "URL_PATH"
    NONE_PATH = "NONE_PATH"


if __name__ == '__main__':
    # 使用示例
    path_type = ValuePathType.RANGE_FROM
    print(path_type)  # 输出: "rangeFrom"
