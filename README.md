# findprecinct

findprecint uses flask and python 2.7.  the general gist of it is to allow a user to input their address/zip code and this app looks up their address via a GIS/MN Legislature API to return a minneapolis precinct.  The app then looks up that precinct from a csv file of a corresponding EventBrite caucus event, and redirects the user to that page.

## development setup

1. you should have python 2.7(ish) installed, but to double check, type `python` and see what happens

2. cd into the base app directory

3. you will need to install pip if you don't have it. use the supplied get-pip.py script: `python get-pip.py`

4. after you have pip, you'll need to install virtualenv: `pip install virtualenv` or `sudo pip install virtualenv`

5. create a virtual environment.  `virtualenv venv`

6. activate your virtual environment `source venv/bin/activate`

7. now install requirements.  `pip install -r requirements.txt` or `sudo pip install -r requirements.txt`

8. now change into the app directory `cd app`

9. now you can use gunicorn to start the app locally on your host and port of choosing: `gunicorn -b 127.0.0.1:8000 mainapp:app --reload`

10. if you make change to the python code it should autoreload the server

11. you can now access the site at `http://127.0.0.1:8000`

12. you can ctrl-c to kill the server.  to leave your virtual environment type `deactivate`


## production setup

1. insert server setup information here :) 

2. the run command is:
```
sudo nohup /home/mpettis/.local/bin/gunicorn -w 4 -b 0.0.0.0:80 mainapp:app > gunicorn.log 2>&1 &
```