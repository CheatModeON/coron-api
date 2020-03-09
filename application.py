#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def about():
    """Print 'Hello, world!' as the response body."""
    return 'Information about coronavirus!'
    
@app.route('/api/v1', methods=["GET"])
@app.route('/api/v1/', methods=["GET"])
def info_view():
    """List of routes for this API."""
    output = {
        'info': 'GET /api/v1',
        'statistics': 'GET /api/v1/general',
        'countries infected': 'GET /api/v1/countries',
        'country stats': 'GET /api/v1/stats?name=',
        'TODO: latest news': 'GET /api/v1/news',
        'TODO: about coronavirus': 'GET /api/v1/coronavirus',
        'TODO: protection measurements': 'GET /api/v1/protection'
    }
    return jsonify(output)
    
@app.route('/api/v1/general', methods=["GET"])
def general_view():
    time_of_request = datetime.now()
    html_data = ''
    resp = requests.get('https://www.worldometers.info/coronavirus/')
    if resp.ok:
        html_data = resp.text
    else:
        print ("Error! {}".format(resp.status_code))
        print (resp.text)
            
    soup = BeautifulSoup(html_data, 'html.parser')

    counters = soup.find_all('div', class_ = 'maincounter-number')
    cases = counters[0].get_text()
    deaths = counters[1].get_text()
    recovered = counters[2].get_text()

    counters2 = soup.find_all('div', class_ = 'number-table-main')
    active_cases = counters2[0].get_text()
    closed_cases = counters2[1].get_text()

    counters3 = soup.find_all('span', class_ = 'number-table')
    mild_condition = counters3[0].get_text()
    serious_condition = counters3[1].get_text()
    #recovered = counters3[2].get_text()
    #deaths = counters3[3].get_text()
    
    output = {
        'time_of_request': time_of_request,
        'cases': cases,
        'deaths': deaths,
        'recovered': recovered,
        'active_cases': active_cases,
        'closed_cases': closed_cases,
        'mild_condition': mild_condition,
        'serious_condition': serious_condition
    }
    return jsonify(output)


@app.route('/api/v1/countries', methods=["GET"])
def infected_countries():

    time_of_request = datetime.now()
    html_data = ''
    resp = requests.get('https://www.worldometers.info/coronavirus/')
    if resp.ok:
        html_data = resp.text
    else:
        print ("Error! {}".format(resp.status_code))
        print (resp.text)
            
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find('table', id = 'main_table_countries')

    allrows = table.tbody.findAll('tr')

    output = []
    r=0
    for row in allrows:
        allcols = row.findAll('td')
        c=0
        data = {}
        for col in allcols:
            if(c==0):
                if(col.find(text=True)!="Total:"):
                    output.append(col.find(text=True))
            c+=1
        r+=1
    return jsonify(output)


@app.route('/api/v1/stats', methods=["GET"])
def countries_stats():

    time_of_request = datetime.now()
    html_data = ''
    resp = requests.get('https://www.worldometers.info/coronavirus/')
    if resp.ok:
        html_data = resp.text
    else:
        print ("Error! {}".format(resp.status_code))
        print (resp.text)
            
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find('table', id = 'main_table_countries')

    allrows = table.tbody.findAll('tr')

    output = []
    r=0
    for row in allrows:
        allcols = row.findAll('td')
        c=0
        data = {}
        for col in allcols:
            if(c==0):
                data['country'] = (col.find(text=True).strip(' '))
            if(c==1):
                if((col.find(text=True))!=None):
                    data['total_cases'] = (col.find(text=True).strip(' '))
                else:
                    data['total_cases'] = "No Data";
            if(c==2):
                if((col.find(text=True))!=None):
                    data['new_cases'] = (col.find(text=True).strip(' '))
                else:
                    data['new_cases'] = "No Data";
            if(c==3):
                if((col.find(text=True))!=None):
                    data['total_deaths'] = (col.find(text=True).strip(' '))
                else:
                    data['total_deaths'] = "No Data";
            if(c==4):
                if((col.find(text=True))!=None):
                    data['new_deaths'] = (col.find(text=True).strip(' '))
                else:
                    data['new_deaths'] = "No Data";
            if(c==5):
                if((col.find(text=True))!=None):
                    data['total_recovered'] = (col.find(text=True).strip(' '))
                else:
                    data['total_recovered'] = "No Data";
            if(c==6):
                if((col.find(text=True))!=None):
                    data['active_cases'] = (col.find(text=True).strip(' '))
                else:
                    data['active_cases'] = "No Data";
            if(c==7):
                if((col.find(text=True))!=None):
                    data['serious_cases'] = (col.find(text=True).strip(' '))
                else:
                    data['serious_cases'] = "No Data";
            if(c==8):
                if((col.find(text=True))!=None):
                    data['total_cases'] = (col.find(text=True))
                else:
                    data['total_cases'] = "No Data";
            
            c+=1
        if(data['country'] != "Total:"):
            output.append(data)
        r+=1

    parameter = request.args.get('name')
    if(parameter != None):
        for dat in (output):
            if(dat['country'] == parameter ):
                return jsonify(dat)
        return "Country not found"
    else:
        return jsonify(output)


if __name__ == '__main__':
    app.run()





