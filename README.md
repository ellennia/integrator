# Integrator

## What this code currently does:
It starts a web server, serving a page that details the funds
in an NECU bank account, and the current time, as well as some
conversions between the bank balance and some foreign currencies
using a forex library.

## Why?
Because NECU doesn't have an API, and I wanted access to my financial info.
In addition, many other service I like don't have APIs- such as the Hannaford (grocery store)
website. I wanted to have a central location to scrape and display information from all these
services that I can check "at a glance", and integrate together to form a concise look at my
personal 'financial surroundings', if that makes sense..

## What tools this code uses:
+ Flask
+ Selenium Webdriver
+ python-forex - fixer.io
+ SQLAlchemy

## Files, and what they do/are:
### Code
+ main.py
The main file. This is where execution starts.
It mostly contains web/Flask related code, as-is.

+ necu.py
The NECU 'banking driver'. It drives Selenium, which
tells PhantomJS how to log into and scrape NECU's website
for banking information.

+ cache.py
A small library file that contains the classes Cache, Frame,
and Account. These store information collected by banking drivers,
into classes that allow structured, easy access to them and their
information.

+ weather.py
The weather driver. Fetches (or at least will fetch) weather information
from the service OpenWeatherMap.

+ alarm.py / work.py
Currently unused. Time related code and job/gig related code, respectively.

### Templates, etc.:
+ templates/home.html
The HTML code for the home page.

### Other:
+ .gitignore
If you're unfamiliar, this marks files that should not be staged/committed
in a git repository. These are files that I've had pop into existence here
that I would really prefer wouldn't, for one reasons or another.

+ README.md
*squints*
