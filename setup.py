from setuptools import setup

setup(
    name='pyffish',
    version='0.0.87',
    py_modules=['pyffish'],  # 指定模块名
    data_files=[('pyffish', ['pyffish.cp311-win_amd64.pyd'])],  # 将 .pyd 文件作为数据文件安装
)