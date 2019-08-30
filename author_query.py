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

def title_count(header, author):

	query = 'search publications for "\\"{}\\"" where type="article" and author_affiliations in {} return publications [doi] limit 1000'.format(author, author_affils)

	try:
		response = response.json()
	except:
		time.sleep(1)
		response = requests.post(
			base_url + 'dsl.json',
			data=query.encode(),
			headers=header)

	# print(response.json())
	
	return response.json()['_stats']['total_count']


def query_titles(header, skip, author):

	query = 'search publications for "\\"{}\\"" where type="article" and author_affiliations in {} return publications [title+author_affiliations+journal+volume+issue+pages+date+doi+pmid+pmcid] limit 1000 skip {}'.format(author, author_affils, skip)

	try:
		response = response.json()
	except:
		time.sleep(1)
		response = requests.post(
			base_url + 'dsl.json',
			data=query.encode(),
			headers=header)
	
	return response.json()['publications']



with open('auths.csv', 'r') as authors, open('pubs.csv', 'w', newline='', encoding="utf-8") as pubs:

	reader = csv.reader(authors, delimiter=',')
	writer = csv.writer(pubs, delimiter=',')
	writer.writerow(['Author Name', 'Publication Title', 'All Authors', 'Journal Title', 'Volume', 'Issue', 'Pages', 'Publication Date', 'DOI', 'PMID', 'PMCID'])
	header = initialize_session()

	for row in reader:
		current_author = row[0]
		pub_count = title_count(header, current_author)

		for skip in range(0, pub_count, 1000):
			authors_queried = query_titles(header, skip, current_author)
			for result in authors_queried:
				pub = [current_author]
				try:
					title = result['title']
				except KeyError:
					title = 'NA'
				try:
					all_auths = []
					authors = result['author_affiliations'][0]
					for auth in authors:
						all_auths.append(' '.join([auth['first_name'], auth['last_name']]))
					all_auths = ', '.join(all_auths)
				except KeyError:
					all_auths = 'NA'
				try:
					journal = result['journal']['title']
				except KeyError:
					journal = 'NA'
				try:
					volume = result['volume']
				except KeyError:
					volume = 'NA'
				try:
					issue = result['issue']
				except KeyError:
					issue = 'NA'
				try:
					pages = result['pages']
				except KeyError:
					pages = 'NA'
				try:
					date = result['date']
				except KeyError:
					date = 'NA'
				try:
					doi = result['doi']
				except KeyError:
					doi = 'NA'
				try:
					pmid = result['pmid']
				except KeyError:
					pmid = 'NA'
				try:
					pmcid = result['pmcid']
				except KeyError:
					pmcid = 'NA'
					
				pub.extend([title, all_auths, journal, volume, issue, pages, date, doi, pmid, pmcid])
				writer.writerow(pub)