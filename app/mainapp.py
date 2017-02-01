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
DATABASE = '/home/mpettis/vmshared/find-precinct/dat/findprecinct.db'
app.config.from_object(__name__)



################################################################################
## Setup database
################################################################################

    ## These are helper functions that aid in connecting to the database for page
    ## requests, as well as configuring how 'select' result sets are structured.
def connect_db():
    """Return a connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

def make_dicts(cur, row):
    """Function that structures sql result sets as a list of dicts
    with a key/value structure with keys being column names and values
    being the cell values."""
    return dict((cur.description[idx][0], value) for idx, value in enumerate(row))

def get_db():
    """Retrieve a database connection.  Reuse existing one if possible, and
    make sure to add function to structure result set in way we want it (list
    of dicts from above)."""
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    db.row_factory = make_dicts
    return db

@app.before_request
def before_request():
    """Connect to database before page connection is established."""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Close database connection when request is being torn down."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



  ##
  ## Helper functions
  ##
def query_db(query, args=(), one=False):
    """Query database, providing just the select statement.  'args' contains tuple
    or dict of bind variables.  one=True will assume we have one row returned
    and return just the dict, and not the single dict wrapped in a list."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



def dbinsert_user(qparam):
    """Given a dict of table column values (fname, ..., precinct), insert this
    person into the people table"""

        ## Insert the person into people table
    db = get_db()
    try:
        with db:
            cur = db.execute("""
                    insert into people
                        (fname, lname, addr, zip, email, precinct)
                        values
                        (:fname, :lname, :addr, :zip, :email, :precinct)"""
                    , qparam)
                ### Get rowid of added user
            rowid = cur.lastrowid
            rowid = rowid if rowid else None
    except Exception as e:
        return(e)

    return(True)



def lod2htmltable(lod):
  """Takes a list of dicts, assume dicts have mostly common keys, converts html representation of data in a table."""
    # Get list of keys, sorted
  ks = sorted(set([k for d in lod for k in d.keys()]))

    # Construct headers
  th = "".join(["<th>%s</th>" % k for k in ks])

    # Construct data rows
  dr = ["".join(["<td>%s</td>" % d.get(k, "-") for k in ks]) for d in lod]
  dr = "\n".join(["<tr>%s</tr>" % e for e in dr])

    # Construct final table
  rv = "\n".join([
          "<table class=\"main\">"
          , "<thead>"
          , th
          , "</thead>"
          , "<tdata>"
          , dr
          , "</tdata>"
          ,"</table>"
        ])
    
  return(rv)



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
    # http://stackoverflow.com/questions/13522137/in-flask-convert-form-post-object-into-a-representation-suitable-for-mongodb
  getp = request.args.to_dict()
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
    tdict['precinct'] = rx.group(1)
    getp['precinct'] = tdict['precinct']
  except Exception as e:
    tdict['error'] = 'Could not parse precinct from GIS server response.'
    tdict['e'] = e
    return render_template('error.html', tdict=tdict)

  try:
    dbinsert_user(getp)
  except Exception as e:
    tdict['error'] = 'Error inserting into database.'
    tdict['e'] = e
    return render_template('error.html', tdict=tdict)

  #return render_template('get_precinct.html', tdict=tdict)
  return render_template('get_precinct.html', tdict=getp)


@app.route('/show_db/')
def show_db():
  tdict = {}
  tdict['people'] = query_db("select * from people")
  tdict['table'] = lod2htmltable(tdict['people'])
  return render_template('show_db.html', tdict=tdict)







    ## For running with just 'python' command.
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80)

