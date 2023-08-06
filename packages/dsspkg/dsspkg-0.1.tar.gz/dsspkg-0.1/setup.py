from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dsspkg",   # 包名字
    version="0.1",
    description="A data splitting and scaling package",
    long_description=long_description,  # 将说明文件设置为README.md
    long_description_content_type="text/markdown",
    packages=find_packages(),   # 默认从当前目录下搜索包
    author="DW",
    author_email="wwwsbx@live.com",
    python_requires='>=3.10',

)
