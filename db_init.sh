mv migrations /tmp
python3 app.py db init
python3 app.py db migrate
python3 app.py db upgrade
