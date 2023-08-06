import os
import sys
import json
from typing import Union
from pip._internal.cli.main import main as pip

name = 'auto-env-config'

default_pip_index = 'https://pypi.mirrors.ustc.edu.cn/simple'


def pip_update(pip_index=None):
    if pip_index:
        pip(f'install --upgrade pip -i {pip_index}'.split(' '))
    else:
        pip('install --upgrade pip'.split(' '))


def install_package(
        package_name,  # 包名
        version=None,  # 版本
        pip_index=default_pip_index,  # pip源
        extra_index=default_pip_index,  # 额外的pip源
        pre_command=None,  # 安装前执行的命令
        after_command=None,  # 安装后执行的命令
        update=False,  # 是否更新pip
        *args,
        **kwargs  # 其他参数
):
    if len(package_name) == 0:
        return
    if update:
        pip_update(pip_index)
    cmd = f'install {package_name}'
    if version:
        cmd += f'=={version}'
    if pip_index:
        cmd += f' -i {pip_index}'
    if extra_index and extra_index != pip_index:
        cmd += f' --extra-index-url {extra_index}'
    if args:
        for arg in args:
            cmd += f' {arg}'
    if kwargs:
        for k, v in kwargs.items():
            cmd += f' --{k} {v}'
    if pre_command:
        os.system(pre_command.replace('$PYTHON', sys.executable))
    pip(cmd.split(' '))
    if after_command:
        os.system(after_command.replace('$PYTHON', sys.executable))


def remove_package(
        package_name,  # 包名
):
    cmd = f'uninstall {package_name} -y'
    pip(cmd.split(' '))


def get_all_package():
    cmd = f'{sys.executable} -m pip list'
    result = os.popen(cmd)
    return [[y for y in x.split(' ') if len(y)] for x in result.read().split('\n')[2:]][:-1]


def remove_all_package(white_list: Union[list, str] = None, *args):
    if isinstance(white_list, str):
        white_list = [white_list]
    if white_list is None:
        white_list = []
    if args is not None:
        white_list += list(args)
    white_list += ['pip', 'setuptools', 'wheel', 'auto-env-config']
    packages = get_all_package()
    for package in packages:
        if package[0] not in white_list:
            remove_package(package[0])


def check_package(
        package_names: Union[str, list]
):
    if isinstance(package_names, str):
        package_names = [package_names]
    result = {}
    all_package = [x[0] for x in get_all_package()]
    for package_name in package_names:
        if package_name in all_package:
            result[package_name] = True
        else:
            result[package_name] = False
    return result

def install(install_file='install.config.json'):
    pip_update()
    if install_file.endswith('.txt'):
        with open(install_file, 'r') as f:
            for line in f.readlines():
                install_package(line.strip())
    elif install_file.endswith('.json'):
        with open(install_file, 'r') as f:
            data = json.load(f)
            if "pip_index" in data:
                pip_index = data['pip_index']
            for package in data['packages']:
                install_package(**package, pip_index=pip_index)