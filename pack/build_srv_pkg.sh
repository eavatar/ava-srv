#!/bin/sh
echo $(pwd)
pyinstaller pack/srv_pkg.spec --clean -y


