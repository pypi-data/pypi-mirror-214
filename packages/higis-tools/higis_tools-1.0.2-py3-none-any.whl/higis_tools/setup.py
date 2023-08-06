from setuptools import setup
from setuptools import find_packages
setup(
    name="higis_tools",  # 包名
    version="1.0.2",  # 版本
    # 最重要的就是py_modules和packages
    py_modules=["higis_tools.serverless"],  # py_modules : 打包的.py文件
    packages=find_packages(),  # packages: 打包的python文件夹
    # keywords=("AI", "Algorithm"),  # 程序的关键字列表
    description="higis serverless tools",                 # 简单描述
    long_description="higis serverless tools,1、add Filed,support schema,type,defualt,decription ", # 详细描述
    # license="MIT Licence",  # 授权信息
    url="",  # 官网地址
    author="lwt",  # 作者
    author_email="watoliu@163.com",  # 作者邮箱
    # packages=find_packages(), # 需要处理的包目录（包含__init__.py的文件夹）
    # platforms="any",  # 适用的软件平台列表
    install_requires=[],  # 需要安装的依赖包
    # 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data和package_data来指定了。
    # scripts=[],  # 安装时需要执行的脚本列表
    # entry_points={     # 动态发现服务和插件
    #     'console_scripts': [
    #         'jsuniv_sllab = jsuniv_sllab.help:main'
    #     ]
    # }
)