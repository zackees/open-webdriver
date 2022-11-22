python make_venv.py
source activate.sh
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m pip install -r requirements.testing.txt
python -m pip install -e .