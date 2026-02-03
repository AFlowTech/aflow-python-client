# 整体架构

引入统一参数模型概念，通过Pydantic BaseModel实现GET/POST参数的标准化定义。
核心思想是：无论GET还是POST请求，都使用继承自BaseModel的类来定义所有参数，实现接口定义的完全统一。

**系统流程增强**
- 模型定义：开发者定义继承自BaseModel的参数模型类
- 注解标记：使用统一装饰器标记HTTP处理函数并关联参数模型
- 自动扫描：扫描器识别被标记的函数及其关联的模型
- 智能解析：解析器从模型类中提取完整的参数信息（字段名、类型、是否必填、默认值）
- 服务注册：将服务实例及标准化接口描述注册到服务中心

## 支持的类型
- int
- float
- str
- bool
- list
- set
- BaseModel

## 安装

### Via pip

```bash
# 安装最新版本
pip install git+https://github.com/AFlowTech/aflow-python-client.git

# 安装指定版本/标签
pip install git+https://github.com/AFlowTech/aflow-python-client.git@1.0.0

# 安装指定分支
pip install git+https://github.com/AFlowTech/aflow-python-client.git@main

# 安装指定提交
pip install git+https://github.com/AFlowTech/aflow-python-client.git@commit-hash
```

### From source

```bash
git clone git@github.com:AFlowTech/aflow-python-client.git
cd aflow-client-python
pip install -e .
```
