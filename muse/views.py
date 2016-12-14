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
    first_location, other_location = [], []
    if len(full_fuzzy2) > 0:
        print(full_fuzzy2, len(full_fuzzy2))
        if len(full_fuzzy2) == 1:
            other_location = []
            first_location = full_fuzzy2
            payload2['location'] = full_fuzzy2.keys()
        else:
            other_location = dict([full_fuzzy2[1]])
            first_location = full_fuzzy2[0][0]
    call = requests.get('https://api-v2.themuse.com/jobs?api_key=' + api_key, params=payload2)
    parsed_json = json.loads(call.text)
    last_page = parsed_json['page_count']
    all_all = {}
    for _ in parsed_json['results']:
        all_all[_['name']] = [_['company']['name'],_['id']]
    return render_template("jobresults.html", all_all=all_all,
                            page=int(page), 
                            full_fuzzy=full_fuzzy2,
                            payload=payload2, last_page=int(last_page), other_location=other_location, first_location=first_location)
    
@app.route("/jobresults", methods=["POST"])
def job_results_post(payload):
    return render_template("jobresults.html")
    
@app.route("/listing/<id>", methods = ["GET"])
def listing_get(id):
    single = requests.get('https://api-v2.themuse.com/jobs/' + id)
    parsed_json = json.loads(single.text)
    return redirect(parsed_json["refs"]["landing_page"])
    
    
@app.route("/companies", methods=["GET"])
def company_criteria_get():
    industries =  ['Advertising and Agencies',
                'Arts and Music',
                'Client Services',
                'Consumer',
                'Education',
                'Engineering',
                'Entertainment & Gaming',
                'Fashion and Beauty',
                'Finance',
                'Food',
                'Government',
                'Healthcare',
                'Law',
                'Manufacturing',
                'Media',
                'Real Estate & Construction',
                'Social Good',
                'Social Media',
                'Tech',
                'Telecom',
                'Travel and Hospitality']
                
    sizes = ['Small Size',
            'Medium Size',
            'Large Size']

    return render_template('companycriteria.html', 
                            industries=industries, 
                            #companies=sorted(companies), 
                            sizes=sizes)

@app.route("/", methods=["POST"])
@app.route("/companycriteria", methods=["POST"])
def company_criteria_post():
    full_fuzzy=[]
    payload = {'page' : 1}
    choose_locations = request.form['location']
    if len(choose_locations) != 0:
        full_fuzzy = locationsearch.locations(choose_locations)
        payload['location'] = locationsearch.locations(choose_locations)[0][0]
    payload['category'] = request.form.getlist('category')
    payload['level'] = request.form.getlist('level')
    return redirect(url_for('company_results_get', payload=payload, full_fuzzy=full_fuzzy, page=1))
    
