from setuptools import setup, find_packages
import os

# 读取版本信息
version_file = os.path.join(os.path.dirname(__file__), '__version__.py')
with open(version_file, 'r', encoding='utf-8') as f:
    exec(f.read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aflow_client_python",
    version=__version__,
    author="Aiden",
    author_email="Aiden@aiflow.fan",
    description="Python客户端库用于服务注册和接口扫描",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AFlowTech/aflow-python-client.git",
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=["tests*", "examples*", "encrypt_lib*", "fastapi_demo*"]),
    package_data={
        '': ['utils/*.so', 'utils/*.dll', 'utils/*.dylib'],  # 包含 utils 目录下的 dll 文件
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
