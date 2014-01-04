# 747

Web page information grabbing script in Python

747 is a small script for grabbing information on the website http://www.seatguru.com/airlines/Air_China. It grabs information about seat detail and saves them in postgreSQL database.

## Models

Right now, 747 implements only grabbing informatino on a single page 'http://www.seatguru.com/airlines/Air_China/Air_China_Boeing_747-400.php' . Other pages are grabbed for the future.


## Compatibility

Currently, 747 will only run on Linux , windows and probably Mac OS X (not tested). 

## Dependencies
- requests
- BeautifulSoup      
- psycopg2 
- re

## Getting started
You should have postgreSQL installed and create a user named 'admin' with password 'admin', then create a database named 'test' under that user, run the init.sql to create necessary tables.At last run the 747.py, it will grab the data for you and store them in the database.

## Documentation
not complete

## What's with the name?
747 is the name of an airplane ,the full name is Boeing 747.

