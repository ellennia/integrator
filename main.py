#!/usr/bin/python
# -*- encoding: UTF-8 -*-

'''
    Integrator : main.py 
        A flask-based personal web app to integrate financial and other
        relevant information. This file in particular is the main Python
        script, from which the application starts. Primarily contains web
        related code. Starts a server on http://localhost:80.

    Todo:
        - Add JS to web page to automatically refresh the page every 10 seconds, or at least the data.
        - Add JS to web page to automatically update time rather than pre-setting it.
        - Using Jinja template to merge current markdown code with home.html
        - Store account data in a sqlite3 database so reloading doesn't necessarily fetch (SQLAlchemy).
        - Use OpenWeatherMap in weather.py to fetch weather information
        - Fetch transactions. By extension, make sound when transaction occurs.
        - Get gas prices somehow
''' 

# Python standard library imports
from os import environ
from decimal import *
import time
from datetime import datetime
import sqlite3
import markdown
import json

# Third party libraries imports
from flask import Flask, Markup, render_template
from selenium import webdriver
from forex_python.converter import CurrencyRates # From fixer.io, updated every day at 3PM

# Local (project) imports
from cache import *
from weather import *
import necu

print('Starting Integrator (Import successful) | OS user account name: \'{}\''.format(environ.get('USERNAME')))
app = Flask(__name__) # Initialize Flask

# Main, global webdriver browser shared among files.
browser = webdriver.PhantomJS('tools/phantomjs.exe')
cache = Cache(browser)

loaded_data = False

requests = 0

'''
    The main page of the web app.
'''
@app.route('/')
def integrator():
    global requests
    requests += 1

    if loaded_data:
        cache.ping()
        frame = cache.present()

        page = '' # NECU account information
        # Markdown
        for account in frame.accounts:
            page += '+ {}: ${} available, ${} present<br>\n'.format(account.name, account.available, account.total)
        page += 'Total: ${}<p>\n'.format(frame.total())

        page2 = '' # Forex data, and page load data
        cr = CurrencyRates(force_decimal = True)
        page2 += '#### Forex data (equivalents):\n'
        euro_conv = cr.convert('USD', 'EUR', frame.available())
        yen_conv = cr.convert('USD', 'JPY', frame.available())
        page2 += '+ Euro: {}\n + Yen: {}\n'.format(euro_conv, yen_conv)

        # Should go in dataset_3, not related to forex
        page3 = '##### Total requests: {} | Frame: {}\n'.format(requests, cache.framecount())

        dataset_1 = Markup(markdown.markdown(page))
        dataset_2 = Markup(markdown.markdown(page2))
        dataset_3 = Markup(markdown.markdown(page3))
        return render_template('home.html', 
                user = 'Ellen', 
                balance = str(frame.available()),
                data = dataset_1,
                data2 = dataset_2,
                data3 = dataset_3
                )
    else:
        page = '<h1>\n'
        page += 'The page hasn\'t quite warmed up yet. You probably wouldn\'t like it cold.<br>\n'
        page += 'Care to wait? :)<br>\n'
        page += '</h1>\n'
        return page

'''
    Data retrieve and submit function.
'''
@app.route('/api', methods = ['POST'])
def info_fetcher():
    function = '' # Post or get
    label = '' # The piece of data being retrieved

    if label == 'necu_data':
        cache.ping()
        return cache.present().jsonify()
    elif label == 'weather_data':
        wjson = get_weather('Dover, NH')
        return ''
    return 'Unknown label'


# NECU stuff
start_time = time.time()
print('Contacting NECU and downloading account info...')

frame = necu.fetch_accounts(browser, True, (environ.get('NECU_Account'), environ.get('NECU_Password')))
cache.add_frame(frame)

loaded_data = True
end_time = time.time()
print('Initialization NECU fetch completed. Time: {} seconds'.format(end_time - start_time))
print('Website accessible now.')
cache.present().summary('NECU') # Prints out account info to the console.
# End NECU stuff

app.run(debug=False, host='0.0.0.0', port=80)
print('Website running.')
