from setuptools import setup, find_packages

setup(
    name='excel-runner',
    version='0.1.1',
    author='Han ZhiChao',
    author_email='superhin@126.com',
    licence='MIT',
    url='http://github.com/hanzhichao/excel-runner',
    packages=find_packages(),

    install_requires=['requests'],
    include_package_data=True,
    package_data={'excel_runner.lib': ['*.txt']}
)
