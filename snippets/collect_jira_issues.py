import csv
from xml.dom.minidom import Element
import requests

def get_versions_without_name(versions):
    result = ' '.join([issue['name'].replace('Jena','') for issue in versions])
    return result

def convert_issue_to_record(issue):
    record = {}
    fields = issue['fields']
    record['key'] = issue['key']
    record['priority'] = fields['priority']['name']
    record['created'] = fields['created']
    record['status'] = fields['status']['name']
    record['versions'] = get_versions_without_name(fields['versions'])
    return record

def get_records_from_project(project,page_length):
    jira_api_base_url = "https://issues.apache.org/jira/"
    proj_jira_id = project.upper()
    start_idx = 0
    url = (
        jira_api_base_url
        + f"rest/api/2/search?jql=project={proj_jira_id}+order+by+created"
        + f"&issuetypeNames=Bug&maxResults={page_length}&"
        + f"startAt={start_idx}&fields=id,key,priority,labels,versions,"
        + "status,components,creator,reporter,issuetype,description,"
        + "summary,resolutiondate,created,updated"
    )
    print(f"Getting data from {url}...")
    r = requests.get(url)
    r_dict = r.json()
    result = []

    for issue in r_dict['issues']:
        record = convert_issue_to_record(issue)
        result.append(record)
    return result

def write_records_to_csv_file(filename,records):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['key', 'priority', 'created', 'status', 'versions'])
        for record in records:
            writer.writerow([record['key'], record['priority'], record['created'], record['status'], record['versions']])

records = get_records_from_project('jena',200)
write_records_to_csv_file("records.csv",records)