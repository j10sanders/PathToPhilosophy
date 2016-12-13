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
    initial_call = requests.get('https://api-v2.themuse.com/jobs?api_key=' + api_key, {'page' : 1})
    #print(r.status_code)
    #print(r.headers['content-type'])
    #print(r.json, "json")
    #print(r.text, "text")
    parsed_json = json.loads(initial_call.text)
    page = parsed_json['page_count']
    payload = {'page' : page}
    updated_request = requests.get('https://api-v2.themuse.com/jobs?api_key=' +
    api_key, params=payload)
    print(updated_request)
    #print(z.text)
    print(updated_request.url)
    print(parsed_json['page_count'], "PAGECOUNT")
    
    #company_title = [(_['name'] , _['company']['name']) for _ in parsed_json['results']]
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

    return render_template('jobs.html', 
                            all_category=all_category, 
                            all_locations=sorted(all_locations), 
                            companies=sorted(companies), 
                            all_levels=all_levels)

@app.route("/jobs", methods=["POST"])
def jobs_post():
    choose_locations = request.form.getlist('location')
    payload = {'page' : 1}
    categories = request.form.getlist('category')
    companies = request.form.getlist('company')
    payload['locations'] = choose_locations
    payload['categories'] = categories
    payload['company'] = companies
    z = requests.get('https://api-v2.themuse.com/jobs?api_key=' + api_key, params=payload)
    print(payload, "PRINTING PAYLOAD1")
    print(z.url, "URL1")
    return redirect(url_for('test_get', payload=payload))
    
@app.route("/test/<payload>", methods=["GET"])
def test_get(payload):
    #parsed_json = json.loads(z)
    #print(payload, 'PRINTING PAYLOAD')
    #payload_string = json.loads(payload)
    #payload_dump = json.dumps(payload_string)
    payload = ast.literal_eval(payload)
    z = requests.get('https://api-v2.themuse.com/jobs?api_key=' + api_key, params=payload)
    print(z.url, "URL")
    
    '''parsed_json = json.loads(z.url)
    print(parsed_json)'''
    '''for _ in parsed_json:
        print(_['name'])'''
    return render_template("test.html")
    
@app.route("/test", methods=["POST"])
def test_post(payload):
    #print(z.url)
    return render_template("test.html")
    
    
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