import requests
import time
import json
import csv

base_url = 'https://app.dimensions.ai/api/'
author_affils = '["University of Rochester", "University of Rochester Medical Center", "Strong Memorial Hospital", "Highland Hospital"]'


def initialize_session():

	with open('login.txt', 'r') as login:
		login = json.load(login)

	print('\nInitializing session...\n')

	resp = requests.post(base_url + 'auth.json', json=login)
	resp.raise_for_status()

	header = {
		'Authorization': 'JWT ' + resp.json()['token']
	}

	print('Session in progress...\n')

	return header



def grant_query(header):

    query = "search grants in full_data for \"pain || opioid\" where research_orgs.name in {} and start_year in [2014:2019] return grants[grant_number+title+start_year+researchers+research_orgs+abstract] limit 1000".format(author_affils)

    try:
        response = response.json()
    except:
        time.sleep(1)
        response = requests.post(
            base_url + 'dsl.json',
            data=query.encode(),
            headers=header)

    return response.json()['grants']


with open('grants.csv', 'w', newline='', encoding="utf-8") as grants:

    writer = csv.writer(grants, delimiter=',')
    writer.writerow(['Grant Number', 'Grant Title', 'Start Year', 'Researchers', 'Research Organization', 'Abstract'])
    header = initialize_session()
    grants_queried = grant_query(header)
    
    for result in grants_queried:
        
        try:
            grant_number = result['grant_number']
        except KeyError:
            grant_number = 'NA'
        try:
            title = result['title']
        except KeyError:
            title = 'NA'
        try:
            start_year = result['start_year']
        except KeyError:
            start_year = 'NA'
        try:
            all_auths = []
            authors = result['researchers']
            for auth in authors:
                all_auths.append(' '.join([auth['first_name'], auth['last_name']]))
            all_auths = ', '.join(all_auths)
        except KeyError:
            all_auths = 'NA'
        try:
            all_orgs = []
            orgs = result['research_orgs']
            for org in orgs:
                all_orgs.append(org['name'])
            all_orgs = ', '.join(all_orgs)
        except KeyError:
            all_orgs = 'NA'
        try:
            abstract = result['abstract']
        except KeyError:
            abstract = 'NA'
            
        row = [grant_number, title, start_year, all_auths, all_orgs, abstract]
        writer.writerow(row)
