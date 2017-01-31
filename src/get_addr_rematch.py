#!/usr/bin/env python

import requests
import re

payload = {'location': '3725 34th ave s 55406' }
r = requests.get('http://www.gis.leg.mn/mapserver/districtsxml/geocode.php', params=payload)

rx = re.match(r'.*<name>(.*?)</name>.*', r.text, re.DOTALL)
print rx.group(1)




rx = re.match(r'.*<name>(.*?)</name>.*', r"stuff <name>prct 1</name> more stuff")
# rx = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
print rx.group(0)
