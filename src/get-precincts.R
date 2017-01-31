#!/c/R/R-3.3.1/bin/Rscript.exe
print("hello")


# MN Leg GIS
# Email:
# Hi Mathew,
# The API link is below.  It’s not something that is advertised, it has accuracy issues since it uses OpenStreetMap’s geocoding API.  We have plans to improve it in the near future using the MapBox geocoding API while also including documentation.
#  
# http://www.gis.leg.mn/mapserver/districtsxml/geocode.php?location=56001
# You just need to pass an address for the location argument where there is currently a zip code.  XML is returned.
#  
# The elements returned are CD, SD, HD, county code, development region code, CD, SD, HD , precinct id, and precinct name.  The redundancy in the congressional and legislative districts are a remnant from redistricting where some folks wanted the new and old districts.  I’ve left things intact ever since.  The precinct data is from the 2016 primary precincts which are attached.  The 2016 general election precincts will be available sometime in mid-October.
#  
# I hope that helps, let me know if there are any questions.
#  
# Lee
#  
# Lee Meilleur | Minnesota Legislature
# LCC Technology Services | 100 Rev. Dr. MLK Jr. Blvd.
# 55 State Office Building | St. Paul, MN 55155
# Lee.meilleur@gis.leg.mn | 651.296.0098


## Working example
#http://www.gis.leg.mn/mapserver/districtsxml/geocode.php?location=3725%2034th%20ave%20s%20minneapolis%20mn%2055406


