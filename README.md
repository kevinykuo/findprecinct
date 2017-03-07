# findprecinct

1. if you dont have python3 installed, please do so.  if you are of the homebrew persuasion you can do it that way, otherwise you can build from source

2. if you can type `python3` from the command line and get something that doesn't look like an error, proceed

3. cd into the base app directory

4. create a virtual environment.  `python3 -m venv venv`

5. activate your virtual environment `source venv/bin/activate`

6. now python3 is simply named `python`

7. now install requirements.  `pip install -r requirements.txt` or `sudo pip install -r requirements.txt`

8. now change into the app directory `cd app`

9. now you can use gunicorn to start the app locally on your host and port of choosing: `gunicorn -b 127.0.0.1:8000 mainapp:app --reload`

10. if you make change to the python code it should autoreload the server

11. you can now access the site at `http://127.0.0.1:8000`

12. you can ctrl-c to kill the server.  to leave your virtual environment type `deactivate`
