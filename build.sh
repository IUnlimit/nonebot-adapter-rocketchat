#!/bin/bash
source .venv/bin/active
python -m build
cd dist
pip install nonebot-adapter-rocketchat-0.1.0.tar.gz
# twine upload dist/*