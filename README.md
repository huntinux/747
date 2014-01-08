# 747

Web page information grabbing script in Python

747 is a small script for grabbing information on the website [http://www.seatguru.com/airlines/Air_China](http://www.seatguru.com/airlines/Air_China). It grabs information about seat detail and saves them in postgreSQL database.

## Models

Right now, 747 can grab information on a single page [http://www.seatguru.com/airlines/Air_China/Air_China_Boeing_747-400.php](http://www.seatguru.com/airlines/Air_China/Air_China_Boeing_747-400.php) using getpage.py and grab airlist in [http://www.seatguru.com/airlines/Air_China/information.php](http://www.seatguru.com/airlines/Air_China/information.php) using airlist.py 


## Compatibility

Currently, 747 will only run on Linux , windows and probably Mac OS X (not tested). 

## Dependencies
- requests
- BeautifulSoup      
- psycopg2 
- re

## Getting started
You should have postgreSQL installed and create a user named 'postgres' with password 'postgres', then create a database named 'test' under that user, run the `init.sql` to create necessary tables. At last run the `airlist.py`, it will grab the data for you and store them in the database.

## Documentation
not complete..

## What's with the name?
_747_ is the name of an airplane ,the full name is _Boeing 747_.

