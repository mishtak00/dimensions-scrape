import requests
import time
import csv


base_url = 'https://app.dimensions.ai/api/'
affils = '["University of Rochester", "University of Rochester Medical Center", "Strong Memorial Hospital", "Highland Hospital"]'
CTSI_grants = ["UL1TR002001","KL2TR001999", "TL1TR002000", "UL1TR000042", "KL2TR000095", "TL1TR000096"]
year_range = '[2012:2016]'


def initialize_session():

	login = {
		'username': 'ENTER_YOUR_DIMENSIONS_API_EMAIL_HERE',
		'password': 'ENTER_YOUR_DIMENSIONS_API_PASSWORD_HERE'
	}

	print('\nInitializing session...\n')

	resp = requests.post(base_url + 'auth.json', json=login)
	resp.raise_for_status()

	header = {
		'Authorization': 'JWT ' + resp.json()['token']
	}

	print('Session in progress...\n')

	return header

def title_count(header, author):

	query = 'search publications in full_data for "\\"{}\\"" where year in {} and type="article" and author_affiliations in {} return publications [doi]'.format(author, year_range, affils)

	try:
		response = response.json()
	except:
		time.sleep(1)
		response = requests.post(
			base_url + 'dsl.json',
			data=query.encode(),
			headers=header)
	
	return response.json()['_stats']['total_count']


def query_author(header, skip, author):

	query = 'search publications in full_data for "\\"{}\\"" where year in {} and type="article" and author_affiliations in {} return publications [title+author_affiliations+journal+volume+issue+pages+date+doi+pmid+pmcid+supporting_grant_ids] limit 1000 skip {}'.format(author, year_range, affils, skip)

	try:
		response = response.json()
	except:
		time.sleep(1)
		response = requests.post(
			base_url + 'dsl.json',
			data=query.encode(),
			headers=header)
	
	return response.json()['publications']


def query_grant(header, grant_id):

	query = 'search grants where id="{}" return grants[grant_number] limit 1000'.format(grant_id)

	try:
		response = response.json()
	except:
		time.sleep(1)
		response = requests.post(
			base_url + 'dsl.json',
			data=query.encode(),
			headers=header)

	try:
		response = response.json()['grants'][0]['grant_number']
	except IndexError:
		print('Index error for response:\n', response.json())
	
	return response



def get_papers():
	with open('authors.csv', 'r') as authors, open('pubs.csv', 'w', newline='', encoding='utf-8') as pubs:

		reader = csv.reader(authors, delimiter=',')
		writer = csv.writer(pubs, delimiter=',')
		header = initialize_session()
		row = ['Current Author', 'Publication Title', 'Authors Names', 'Journal Title', 'Volume', 'Issue', 'Pages', 'Publication Date', 'DOI', 'PMID', 'PMCID', 'Supporting Grant Number']
		writer.writerow(row)

		for row in reader:
			current_author = row[0]
			pub_count = title_count(header, current_author)

			for skip in range(0, pub_count, 1000):
				papers = query_author(header, skip, current_author)

				for result in papers:
					try:
						grant_ids = result['supporting_grant_ids']
					except KeyError:
						print(result)
						continue
					for grant_id in grant_ids:
						grant_nr = query_grant(header, grant_id)
						print(current_author, grant_nr)
						if grant_nr in CTSI_grants:
							print(f'Paper from {current_author} was supported by CTSI grant nr {grant_nr}')
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
								
							pub = [current_author, title, all_auths, journal, volume, issue, pages, date, doi, pmid, pmcid, grant_nr]
							writer.writerow(pub)



if __name__ == '__main__':
	get_papers()
