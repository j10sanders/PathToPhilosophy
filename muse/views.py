import requests
import json
from flask import render_template, request, redirect, url_for
from . import app
import copy
import ast

api_key = 'afb4ed7652b99475b548e55ddbca70bcb72575fa881bc2c0a652e2ec0150356b'

@app.route("/")
@app.route("/jobs", methods=["GET"])
def jobs_get():
    initial_call = requests.get('https://api-v2.themuse.com/jobs', {'page' : 1})
    #print(r.status_code)
    #print(r.headers['content-type'])
    #print(r.json, "json")
    #print(r.text, "text")
    parsed_json = json.loads(initial_call.text)
    page = parsed_json['page_count']
    payload = {'page' : page}
    updated_request = requests.get('https://api-v2.themuse.com/jobs', params=payload)
    print(updated_request)
    #print(z.text)
    print(updated_request.url)
    print(parsed_json['page_count'], "PAGECOUNT")
    
    all_category =  ['Account Management',
                    'Business & Strategy',
                    'Creative & Design',
                    'Customer Service',
                    'Data Science',
                    'Editorial',
                    'Education',
                    'Engineering',
                    'Finance',
                    'Fundraising & Development',
                    'Healthcare & Medicine',
                    'HR & Recruiting',
                    'Legal',
                    'Marketing & PR',
                    'Operations',
                    'Project & Product Management',
                    'Retail',
                    'Sales',
                    'Social Media & Community']
    
    all_levels = ['Internship',
                    'Entry Level',
                    'Mid Level',
                    'Senior Level']
                    
    all_locations = []
    companies = []
    for _ in parsed_json['results']:
        locations = _['locations']
        company = _['company']
        for location in locations:
            #print(location['name'])
            all_locations.append(location['name'])
        for comp in [company]:
            companies.append(comp['name'])
    job_listings = "not yet"
    
    return render_template('jobs.html', 
                            all_category=all_category, 
                            all_locations=sorted(all_locations), 
                            companies=sorted(companies), 
                            all_levels=all_levels,
                            job_listings=job_listings)

@app.route("/jobs", methods=["POST"])
def jobs_post():
    choose_locations = request.form.getlist('location')
    payload = {'page' : 1}
    categories = request.form.getlist('category')
    levels = request.form.getlist('level')
    payload['location'] = choose_locations
    payload['category'] = categories
    #payload['company'] = companies
    payload['level'] = levels
    z = requests.get('https://api-v2.themuse.com/jobs', params=payload)
    print(payload, "PRINTING PAYLOAD1")
    print(z.url, "URL1")
    return redirect(url_for('test_get', payload=payload))
    
@app.route("/test/<payload>", methods=["GET"])
def test_get(payload):
    payload2 = ast.literal_eval(payload)
    z = requests.get('https://api-v2.themuse.com/jobs', params=payload2)
    print(z.url, "URL2")
    parsed_json = json.loads(z.text)
    names = []
    all_all = {}
    for _ in parsed_json['results']:
        names.append(_['name'])
        all_all[_['name']] = [_['company']['name'],_['id']]
    all_category = []
    '''for _ in parsed_json['results']:
        categories = _['categories']
        for category in categories:
            all_category.append(category['name'])'''
    
    print(all_all, "ALL ALL")
    '''for _ in parsed_json['results']:
        print(_['id'])'''
    
    return render_template("test.html", all_all=all_all)
    
@app.route("/test", methods=["POST"])
def test_post(payload):
    #print(z.url)
    return render_template("test.html")
    
@app.route("/listing/<id>", methods = ["GET"])
def listing_get(id):
    a = requests.get('https://api-v2.themuse.com/jobs/' + id)
    parsed_json = json.loads(a.text)
    #print("PARSED:", parsed_json, "PARDDED")
    print(parsed_json["refs"]["landing_page"], "PRINTED")
    return redirect(parsed_json["refs"]["landing_page"])
    
    
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