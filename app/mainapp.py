#!/usr/bin/env python
"""
Application: mainapp
Author: Matt Pettis
Description: Main Flask application that connects up people and precincts.
"""
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from pprint import pprint, pformat
import time
import jinja2
from collections import defaultdict
import requests
import re

################################################################################
## Setup misc
################################################################################
jinja2.filters.FILTERS['pformat'] = pformat

    ## Set up the application and read in configuration information.  This should
    ## be pushed to an external configuration file eventually.
################################################################################
## Setup app
################################################################################
app = Flask(__name__)
app.config.from_object(__name__)



################################################################################
## Setup database
################################################################################
#DATABASE = '/Users/mpettis/github/pyconvcreds/ccred/db/ccred.db'



################################################################################
## Page route setup
################################################################################

  ## Just a trial setup
@app.route('/')
def homepage():
  # return 'Hello, World!'
  # return render_template('homepage.html', tdict={})
  return render_template('homepage.html')


@app.route('/get_precinct/')
def get_precinct():
    # Get the address parameters passed
  getp = request.args
  tdict = {}

    # Build location from the address parameters
  payload = {'location': "%s %s" % (getp['addr'], getp['zip']) }
  try:
    r = requests.get('http://www.gis.leg.mn/mapserver/districtsxml/geocode.php', params=payload)
  except:
    tdict['error'] = 'Could not retrieve address from GIS server.'
    return render_template('error.html', tdict=tdict)

  tdict['xml'] = r.text

    ## Find precinct name, embedded in xml '<name>' tag
  try:
    rx = re.match(r'.*<name>(.*?)</name>.*', r.text, re.DOTALL)
    tdict['prct'] = rx.group(1)
  except:
    tdict['error'] = 'Could not parse precinct from GIS server response.'
    return render_template('error.html', tdict=tdict)

  return render_template('get_precinct.html', tdict=tdict)










    ## For running with just 'python' command.
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80)

