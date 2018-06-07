#!/bin/bash

set -e
set -u

sudo apt-get install python3 python3-pip
sudo pip3 install virtualenv

virtualenv --python=python3 venv
venv/bin/pip install -r requirements.py
