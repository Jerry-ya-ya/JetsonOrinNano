# The steps to build up Waverover development

## First time build up
sudo apt install python3.10-venv

cd Waverover

python3 -m venv .venv --system-site-packages

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

source .venv/bin/activate

deactivate

## Daily
cd Waverover

source .venv/bin/activate

deactivate