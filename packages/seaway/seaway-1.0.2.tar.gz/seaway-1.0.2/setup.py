# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import io
from seaway.version import VERSION


with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="seaway",
    version=VERSION,
    description="客户端组件化CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="组件化",
    author="wangshuwen",
    author_email="331835844@qq.com",
    url="",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["requests"],
    entry_points={"console_scripts": ["seaway = seaway:run"]},
)
