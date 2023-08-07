# python_tes_shopify

## install dev
python -m venv venv
venv/Scripts/activate
pip install -r requirements_dev.txt
pre-commit install --hook-type pre-push

## build and deploy
pip install build
python -m build
