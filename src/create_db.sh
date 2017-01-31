#!/bin/bash
# hello
#

dir_proj=/home/mpettis/vmshared/find-precinct
dir_db=${dir_proj}/dat
file_db=${dir_db}/ccred.db
sql_setupfile=${dir_proj}/src/setup_db.sql

if [[ -e $file_db ]]; then
    rm $file_db
fi

## In dat directory:
## <people.csv sed 1d > people_noh.csv
## <precincts.csv sed 1d > precincts_noh.csv

  ### Create the database
sqlite3 $file_db ".databases"

  ### Run setup and load
sqlite3 $file_db < $sql_setupfile

