import requests
import json
from flask import render_template, request, redirect, url_for, flash
from . import app
import ast
from . import locationsearch, lists

api_key = 'afb4ed7652b99475b548e55ddbca70bcb72575fa881bc2c0a652e2ec0150356b'


# Choose criteria for job search.
@app.route("/", methods=["GET"])
@app.route("/jobcriteria", methods=["GET"])
def job_criteria_get():
    return render_template('jobcriteria.html',
                            all_category=lists.categories,
                            all_levels=lists.levels,
                            all_companies=lists.companies)


# Add criteria to api call
@app.route("/", methods=["POST"])
@app.route("/jobcriteria", methods=["POST"])
def job_criteria_post():
    full_fuzzy = []
    payload = {'page': 1}
    choose_locations = request.form['location']
    # Use fuzzy search to find closest two location matches
    if len(choose_locations) != 0:
        full_fuzzy = locationsearch.locations(choose_locations)
        payload['location'] = locationsearch.locations(choose_locations)[0][0]
    payload['category'] = request.form.getlist('category')
    payload['level'] = request.form.getlist('level')
    payload['company'] = request.form.getlist('company')
    return redirect(url_for('job_results_get',
                            payload=payload,
                            full_fuzzy=full_fuzzy,
                            page=1))


# Return jobs
@app.route("/jobresults/<payload>/<full_fuzzy>/<page>", methods=["GET"])
def job_results_get(payload, full_fuzzy, page):
    payload2 = ast.literal_eval(payload)
    full_fuzzy2 = ast.literal_eval(full_fuzzy)
    payload2['page'] = page
    # Fuzzy search returns top 2 matches, in order.  use first but send both on
    # initial request. If the user selects the second one, just send that one.
    first_location, other_location = [], []
    if len(full_fuzzy2) > 0:
        if len(full_fuzzy2) == 1:
            other_location = []
            first_location = full_fuzzy2
            payload2['location'] = full_fuzzy2.keys()
        else:
            other_location = dict([full_fuzzy2[1]])
            first_location = full_fuzzy2[0][0]
    call = requests.get('https://api-v2.themuse.com/jobs?api_key=' +
                        api_key, params=payload2)
    parsed_json = json.loads(call.text)
    last_page = parsed_json['page_count']
    # Send template a dictionary with {Job Title : [company name, job id]}
    jobs_w_companies = {}
    for _ in parsed_json['results']:
        jobs_w_companies[_['name']] = [_['company']['name'], _['id']]
    return render_template("jobresults.html",
                            jobs_w_companies=jobs_w_companies,
                            page=int(page),
                            full_fuzzy=full_fuzzy2,
                            payload=payload2,
                            last_page=int(last_page),
                            other_location=other_location,
                            first_location=first_location)


@app.route("/listing/<id>", methods=["GET"])
def listing_get(id):
    single = requests.get('https://api-v2.themuse.com/jobs/' + id)
    parsed_json = json.loads(single.text)
    return redirect(parsed_json["refs"]["landing_page"])


@app.route("/companycriteria", methods=["GET"])
def company_criteria_get():
    return render_template('companycriteria.html',
                            industries=lists.industries,
                            sizes=lists.sizes)


@app.route("/companycriteria", methods=["POST"])
def company_criteria_post():
    full_fuzzy = []
    payload = {'page': 1}
    choose_locations = request.form['location']
    if len(choose_locations) != 0:
        full_fuzzy = locationsearch.locations(choose_locations)
        payload['location'] = locationsearch.locations(choose_locations)[0][0]
    payload['category'] = request.form.getlist('category')
    payload['level'] = request.form.getlist('level')
    return redirect(url_for('company_results_get',
                            payload=payload,
                            full_fuzzy=full_fuzzy,
                            page=1))

@app.route("/companyresults/<payload>/<full_fuzzy>/<page>", methods=["GET"])
def company_results_get(payload, full_fuzzy, page):
    payload2 = ast.literal_eval(payload)
    full_fuzzy2 = ast.literal_eval(full_fuzzy)
    payload2['page'] = page
    # Fuzzy search returns top 2 matches, in order.  use first but send both on 
    # initial request. If the user selects the second one, just send that one.
    first_location, other_location = [], []
    if len(full_fuzzy2) > 0:
        if len(full_fuzzy2) == 1:
            other_location = []
            first_location = full_fuzzy2
            payload2['location'] = full_fuzzy2.keys()
        else:
            other_location = dict([full_fuzzy2[1]])
            first_location = full_fuzzy2[0][0]
    call = requests.get('https://api-v2.themuse.com/companies?api_key=' +
                        api_key, params=payload2)
    print(call.url)
    parsed_json = json.loads(call.text)
    print(parsed_json, "PARSED")
    last_page = parsed_json['page_count']

    # Send template a dictionary with {Job Title : [company name, job id]}
    companies_w_description = {}
    for _ in parsed_json['results']:
        print(_['name'])
        print(_['id'])
        print(_['description'])
        companies_w_description[_['name']] = [_['description'], _['id']]
    return render_template("companyresults.html",
                            companies_w_description=companies_w_description,
                            page=int(page), 
                            full_fuzzy=full_fuzzy2,
                            payload=payload2,
                            last_page=int(last_page),
                            other_location=other_location,
                            first_location=first_location)


@app.route("/companylisting/<id>", methods=["GET"])
def company_listing_get(id):
    single = requests.get('https://api-v2.themuse.com/companies/' + id)
    parsed_json = json.loads(single.text)
    return redirect(parsed_json['refs']["landing_page"])
