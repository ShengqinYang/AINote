# -*- coding: utf-8 -*-
import sys
from pip._internal import main as pip_main
import os


def install(package):
    package_name = package.decode("utf-8").replace("\n", "")
    # print(package)
    # pip_main(['--default-timeout=1000', 'install', '-U', package, '-i',
    #           'http://pypi.douban.com/simple/'])
    # os.system(f'pip install {package_name} -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com')
    os.system(f'pip install {package_name} -i https://mirrors.aliyun.com/pypi/simple/')


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        for line in f:
            install(line)