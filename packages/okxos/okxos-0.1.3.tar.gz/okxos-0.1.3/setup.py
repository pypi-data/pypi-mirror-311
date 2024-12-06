from setuptools import setup, find_packages

setup(
    name="okxos",  # 包名称
    version="0.1.3",  # 初始版本号
    author="bobo",
    author_email="your_email@example.com",
    description="A Python client for OKX OS APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/okxos",  # 项目地址
    packages=find_packages(),  # 自动发现包
    install_requires=[
        "httpx>=0.24.1",  # 必需依赖
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # 最低 Python 版本要求
)