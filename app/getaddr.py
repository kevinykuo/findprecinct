#!/usr/bin/env python
"""
Application: pyconvcred
Author: Matt Pettis
Description: Main Flask application that handles the routing of pages and has utility functions
to help with that.
"""
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from pprint import pprint, pformat
import time
import jinja2
from collections import defaultdict
import requests

    ## Set up the application and read in configuration information.  This should
    ## be pushed to an external configuration file eventually.
app = Flask(__name__)
#DATABASE = '/Users/mpettis/github/pyconvcreds/ccred/db/ccred.db'
app.config.from_object(__name__)




@app.route('/')
def hello_world():
    payload = {'location': '3725 34th ave s 55406' }
    r = requests.get('http://www.gis.leg.mn/mapserver/districtsxml/geocode.php', params=payload)
    #return 'Hello, World!'
    #return(r.text)
    return render_template('getaddr.html', tdict={})




    ## For running with just 'python' command.
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80)

