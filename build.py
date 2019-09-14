#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年9月10日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: build
@description: 
"""
import argparse
import os
import shutil
import subprocess
import sys
from zipfile import ZipFile


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--platform', default=None,
                    metavar='[Windows or Linux]',
                    choices=['Windows', 'Linux'],
                    required=True, help='System platform')
parser.add_argument('-a', '--arch', default=None, type=str.lower,
                    metavar='[x86 or x64]',
                    choices=['x86', 'x64'],
                    required=True, help='System Arch')
parser.add_argument('--qmake', default='', help='qmake tools')
parser.add_argument('--sudo', default=False, type=bool, help='sudo')

args = parser.parse_args()

print('Platform:', args.platform)
print('Arch:', args.arch)
make = 'make'
if args.platform == 'Windows':
    make = 'nmake'
print('make:', make)
print('qmake:', args.qmake)
print('sudo:', args.sudo)


def buildPySide2():
    # 编译
    try:
        shutil.rmtree('OpenSSL', ignore_errors=True)
    except Exception as e:
        print('remove OpenSSL', e)

    with ZipFile('src/openssl-1.0.2j-fips-x86_64.zip', 'r') as tf:
        tf.extractall(path='src')

    print('extractall OpenSSL ok')

    try:
        shutil.rmtree('pyside-setup-everywhere-src-5.13.1', ignore_errors=True)
    except Exception as e:
        print('remove pyside-setup-everywhere-src-5.13.1', e)

    with ZipFile('src/pyside-setup-everywhere-src-5.13.1.zip', 'r') as tf:
        tf.extractall(path='src')

    print('extractall PyQt5 ok')

    os.chdir('src/pyside-setup-everywhere-src-5.13.1')

    try:
        cmd = '{0} setup.py ' \
              'build ' \
              '{1} {2}'.format(
                  sys.executable,
                  '--qmake={}'.format(args.qmake) if args.qmake else '',
                  '--openssl={}'.format(os.path.abspath(
                      'src/OpenSSL/bin').replace('/', '\\'))
              )
        print('cmd:', cmd)
        retcode = subprocess.check_call(
            cmd,
            env=os.environ, shell=True,
            stderr=subprocess.STDOUT
        )
        print('retcode:', retcode)
        assert retcode == 0
        print('\nbuild PySide2 ok\n')
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    buildPySide2()
