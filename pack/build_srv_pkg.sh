#!/bin/sh
echo $(pwd)
python ./pack/pyinstdev/pyinstaller.py pack/srv_pkg.spec --clean -y


