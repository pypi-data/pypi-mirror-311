# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="myMath_yao",  # 包的名称
    version="0.2",  # 包的版本
    description="A simple math package",  # 包的描述
    long_description=open('README.md').read(),  # 长描述，通常读取 README 文件
    long_description_content_type="text/markdown",  # 长描述的格式
    author="Your Name",  # 作者
    author_email="your.email@example.com",  # 作者邮箱
    url="https://github.com/yourusername/mymath",  # 项目主页
    packages=find_packages(),  # 自动发现包
    classifiers=[  # 分类器，有助于在 PyPI 中分类
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # 没有外部依赖
    python_requires='>=3.6',  # 支持的 Python 版本
)
