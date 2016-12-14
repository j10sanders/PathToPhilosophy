import requests
import json
from flask import render_template, request, redirect, url_for, flash
from . import app
import copy
import ast
import fuzzywuzzy
from . import locationsearch

api_key = 'afb4ed7652b99475b548e55ddbca70bcb72575fa881bc2c0a652e2ec0150356b'

@app.route("/", methods=["GET"])
@app.route("/jobcriteria", methods=["GET"])
def job_criteria_get():
    initial_call = requests.get('https://api-v2.themuse.com/jobs', {'page' : 1})
    parsed_json = json.loads(initial_call.text)
    page = parsed_json['page_count']
    payload = {'page' : page}
    updated_request = requests.get('https://api-v2.themuse.com/jobs', params=payload)
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
    '''all_locations = []
    companies = []
    for _ in parsed_json['results']:
        locations = _['locations']
        company = _['company']
        for location in locations:
            all_locations.append(location['name'])
        for comp in [company]:
            companies.append(comp['name'])
    '''
    
    return render_template('jobcriteria.html', 
                            all_category=all_category, 
                            #companies=sorted(companies), 
                            all_levels=all_levels)

@app.route("/", methods=["POST"])
@app.route("/jobcriteria", methods=["POST"])
def job_criteria_post():
    full_fuzzy=[]
    payload = {'page' : 1}
    choose_locations = request.form['location']
    if len(choose_locations) != 0:
        full_fuzzy = locationsearch.locations(choose_locations)
        payload['location'] = locationsearch.locations(choose_locations)[0][0]
    payload['category'] = request.form.getlist('category')
    payload['level'] = request.form.getlist('level')
    return redirect(url_for('job_results_get', payload=payload, full_fuzzy=full_fuzzy, page=1))
    
@app.route("/jobresults/<payload>/<full_fuzzy>/<page>", methods=["GET"])
def job_results_get(payload, full_fuzzy, page):
    payload2 = ast.literal_eval(payload)
    full_fuzzy2 = ast.literal_eval(full_fuzzy)
    payload2['page'] = page
    if len(full_fuzzy2) > 0:
        flash("Displaying results for " + full_fuzzy2[0][0] + 
                ".  Please change your search if you meant " + 
                full_fuzzy2[1][0], "success")
    call = requests.get('https://api-v2.themuse.com/jobs', params=payload2)
    parsed_json = json.loads(call.text)
    last_page = parsed_json['page_count']
    all_all = {}
    for _ in parsed_json['results']:
        all_all[_['name']] = [_['company']['name'],_['id']]
    #print(all_all, "ALL ALL")
    return render_template("jobresults.html", all_all=all_all,
                            page=int(page), 
                            full_fuzzy=full_fuzzy2,
                            payload=payload2, last_page=int(last_page))
    
@app.route("/jobresults", methods=["POST"])
def job_results_post(payload):
    return render_template("jobresults.html")
    
@app.route("/listing/<id>", methods = ["GET"])
def listing_get(id):
    single = requests.get('https://api-v2.themuse.com/jobs/' + id)
    parsed_json = json.loads(single.text)
    #print(parsed_json["refs"]["landing_page"], "PRINTED")
    return redirect(parsed_json["refs"]["landing_page"])
    
    
@app.route("/companies", methods=["GET"])
def companies_get():
    r = requests.get('https://api-v2.themuse.com/jobs')

    print(r.status_code)
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
    return render_template('jobresults.html', z=z)
    
