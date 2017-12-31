# Integrator

## What this code currently does:
It starts a web server on localhost:80, serving a page that displays the funds in an NECU online banking account, the current time, as well as some conversions between the bank balance and some foreign currencies using a forex library. If you have an NECU account, this code may be of interest to you.

## Why?
The primary purpose is to integrate all my financial information in one place. I want to have an auto-updating interface that shows me in realtime what resources I have access to, what I can do with those resources, and what my immediate environment looks like.

Because my credit union, Northeast Credit Union, does not have an API for their online banking system (shame), I had to write a scraper using Selenium Webdriver to obtain the information. This is one of the most important features of this program- it scrapes and fetches that account information.

In addition, many other service I use don't have APIs- such as the Hannaford (grocery store) website. With the boilerplate in place, I could see weird stats such as, say, how many miles I could drive in my car by taking the financial information, multiplying it by local gas prices and then computing it against my car's gas mileage. It's an open source program similar to a program called 'Mint' made by a certain financial software company.

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
