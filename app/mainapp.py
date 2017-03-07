#!/usr/bin/env python
"""
Application: mainapp
Author: Matt Pettis
Description: Main Flask application that connects up people and precincts.
"""
from flask import Flask, request,  render_template, redirect
from pprint import pprint, pformat
import jinja2
import requests
import re
import csv

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

DEBUG=1

def make_dicts(cur, row):
    """Function that structures sql result sets as a list of dicts
    with a key/value structure with keys being column names and values
    being the cell values."""
    return dict((cur.description[idx][0], value) for idx, value in enumerate(row))



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
  return render_template('homepage.html', tdict={})


@app.route('/get_precinct/')
def get_precinct():
    # Get the address parameters passed
    # http://stackoverflow.com/questions/13522137/in-flask-convert-form-post-object-into-a-representation-suitable-for-mongodb
  getp = request.args.to_dict()
  tdict = {'debug':DEBUG}

  print('request get vars %s ' % getp )

    # Build location from the address parameters
  payload = {'location': "%s %s" % (getp['addr'], getp['zip']) }

  try:
    r = requests.get('http://www.gis.leg.mn/mapserver/districtsxml/geocode.php', params=payload)
  except Exception as e:
    print('exception: %s ' % e)
    tdict['error'] = 'Could not retrieve address from GIS server.'
    return render_template('homepage.html', tdict=tdict)

  tdict['xml'] = r.text

    ## Find precinct name, embedded in xml '<name>' tag
  try:
    rx = re.match(r'.*<name>(.*?)</name>.*', r.text, re.DOTALL)
    tdict['precinct'] = rx.group(1)
    getp['precinct'] = tdict['precinct']

    url = precint_name_to_eventbrite(tdict['precinct'])

    return redirect_to_precint(url)

  except Exception as e:
    tdict['error'] = 'Could not parse precinct from GIS server response.'
    tdict['e'] = e
    tdict['form'] = getp

    return render_template('homepage.html', tdict=tdict)

  #return render_template('get_precinct.html', tdict=tdict)
  return render_template('get_precinct.html', tdict=getp)


def redirect_to_precint(url):
    return redirect(url, code=302)

def precint_name_to_eventbrite(precinct):

    with open('precinct-eventbrite-location.csv','r') as csvfile:

        for row in csv.reader(csvfile, delimiter=','):
            precinct_name = row[0]
            eventbrite_link = row[1]
            if precinct_name == precinct:
                print('found match, return %s '% eventbrite_link)
                return eventbrite_link

    # @TODO load precing-eventbrite-location.csv and parse out correct location
    url ='https://www.eventbrite.com/e/2017-caucus-for-ward-2-precinct-10-tickets-32520642116'
    return url