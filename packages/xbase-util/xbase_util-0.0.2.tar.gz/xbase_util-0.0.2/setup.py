from distutils.core import setup

from setuptools import find_packages

setup(name="xbase_util",
      version="0.0.2",
      description="网络安全基础工具",
      long_description="包含提取，预测，训练的基础工具",
      author="xyt",
      author_email="2506564278@qq.com",
      license="<MIT License>",
      packages=find_packages(),
      install_requires=[
            'PyExecJS==1.5.1',
      ],
      zip_safe=False)
