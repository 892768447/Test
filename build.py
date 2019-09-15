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
import subprocess
import sys


try:
    from pip._internal import main as _main  # @UnusedImport
except:
    from pip import main as _main  # @Reimport @UnresolvedImport


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

_main(['install', 'wheel', 'requests'])

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
parser.add_argument('--openssl', default='', help='openssl path')
parser.add_argument('--sudo', default=False, type=bool, help='sudo')

args = parser.parse_args()

print('Platform:', args.platform)
print('Arch:', args.arch)
make = 'make'
if args.platform == 'Windows':
    make = 'nmake'
print('make:', make)
print('qmake:', args.qmake)
print('openssl:', args.openssl)
print('sudo:', args.sudo)


def buildPySide2():
    # 编译
    os.chdir('pyside-setup-everywhere-src-5.13.1')

    # 修改支持Webkit
    data = open(r'sources\cmake_helpers\helpers.cmake',
                'rb').read().decode('utf-8')
    data = data.replace('WebChannel WebEngineCore',
                        'WebKit WebKitWidgets WebChannel WebEngineCore')
    open(r'sources\cmake_helpers\helpers.cmake', 'wb').write(data.encode())
    print(data)

    try:
        cmd = '{0} setup.py ' \
              'build ' \
              '--skip-modules=Sql,Test,Concurrent,WinExtras,Xml,XmlPatterns,Help,Multimedia,MultimediaWidgets,OpenGL,OpenGLFunctions,Positioning,Location,Qml,Quick,QuickWidgets,RemoteObjects,Scxml,Script,ScriptTools,Sensors,TextToSpeech,Charts,Svg,DataVisualization,UiTools,AxContainer,WebChannel,WebEngineCore,WebEngine,WebEngineWidgets,WebSockets,3DCore,3DRender,3DInput,3DLogic,3DAnimation,3DExtras ' \
              '{1} {2}'.format(
                  sys.executable,
                  '--qmake={}'.format(args.qmake) if args.qmake else '',
                  '--openssl={}'.format(args.openssl) if args.openssl else ''
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
