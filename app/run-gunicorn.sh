#!/bin/bash
#gunicorn -w 4 -b 0.0.0.0:8000 myapp:app
gunicorn -w 4 -b 0.0.0.0:8000 $1:app

