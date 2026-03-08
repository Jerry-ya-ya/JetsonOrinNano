sudo apt install python3.10-venv

cd Waverover

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

deactivate