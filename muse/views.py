import requests
import json
from flask import render_template, request, redirect, url_for
from . import app

@app.route("/")
@app.route("/jobs", methods=["GET"])
def jobs_get():
    r = requests.get('https://api-v2.themuse.com/jobs')

    print(r.status_code)
    #print(r.headers['content-type'])
    #print(r.json, "json")
    #print(r.text, "text")
    
    payload = {'page' : 1}
    z = requests.get('https://api-v2.themuse.com/jobs', params=payload)
    print(z)
    #print(z.text)
    print(z.url)
    parsed_json = json.loads(z.text)
    '''for _ in parsed_json['results']:
        name = _['name']
        company = _['company']
        print(company['name'], ":", name)'''
    
    #company_title = [(_['name'] , _['company']['name']) for _ in parsed_json['results']]
    all_category = []
    for _ in parsed_json['results']:
        categories = _['categories']
        for category in categories:
            #print(location['name'])
            all_category.append(category['name'])
    #print(company_title)
    #locations = [company['locations'] for company in parsed_json['results']]
    z = []
    companies = []
    for _ in parsed_json['results']:
        locations = _['locations']
        company = _['company']
        for location in locations:
            #print(location['name'])
            z.append(location['name'])
        for comp in [company]:
            companies.append(comp['name'])

    return render_template("jobs.html", all_category=sorted(all_category), locations=sorted(z), companies=sorted(companies))

@app.route("/jobs", methods=["POST"])
def jobs_post():
    choose_locations = request.form.getlist("location")
    payload = {'page' : 1}
    categories = request.form.getlist("category")
    companies = request.form.getlist("company")
    payload['locations'] = choose_locations
    payload['categories'] = categories
    payload['company'] = companies
    z = requests.get('https://api-v2.themuse.com/jobs', params=payload)
    print(z.url)
    return render_template('test.html', z=z)
    
@app.route("/test/z", methods=["GET"])
def test(z):
    print(z.url)
    return render_template("test.html", z=z)
    
@app.route("/test/z", methods=["POST"])
def test_post(z):
    print(z.url)
    return render_template("joblist.html")
    
    
@app.route("/companies", methods=["GET"])
def companies_get():
    r = requests.get('https://api-v2.themuse.com/jobs')

    print(r.status_code)
    #print(r.headers['content-type'])
    #print(r.json, "json")
    #print(r.text, "text")
    
    payload = {'page' : 1}
    z = requests.get('https://api-v2.themuse.com/companies', params=payload)
    print(z)
    #print(z.text)
    print(z.url)
    parsed_json = json.loads(z.text)
    '''for _ in parsed_json['results']:
        name = _['name']
        company = _['company']
        print(company['name'], ":", name)'''
    
    #company_title = [(_['name'] , _['company']['name']) for _ in parsed_json['results']]
    all_category = []
    for _ in parsed_json['results']:
        categories = _['categories']
        for category in categories:
            #print(location['name'])
            all_category.append(category['name'])
    #print(company_title)
    #locations = [company['locations'] for company in parsed_json['results']]
    z = []
    for _ in parsed_json['results']:
        locations = _['locations']
        for location in locations:
            #print(location['name'])
            z.append(location['name'])

    
    #doop = [location['name'] for location in locations]
    #print(locations)
        
    return render_template("companies.html", all_category=all_category, locations=z)

@app.route("/companies", methods=["POST"])
def companies_post():
    choose_locations = request.form.getlist("location")
    payload = {'page' : 1}
    categories = request.form.getlist("category")
    print(categories)
    payload['locations'] = sorted(choose_locations)
    payload['categories'] = categories
    z = requests.get('https://api-v2.themuse.com/companies', params=payload)
    print(z.url)
    return render_template('test.html', z=z)