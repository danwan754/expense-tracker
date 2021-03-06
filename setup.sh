cd expense-tracker;
virtualenv ./venv;
source ./venv/bin/activate;
pip install -r requirements.txt;
export FLASK_APP=run.py;
export FLASK_ENV=development;
export FLASK_CONFIG=development;
flask db init;
flask db migrate;
flask db upgrade;
