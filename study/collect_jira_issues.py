import csv
from xml.dom.minidom import Element
import os
import requests

def main(repo):

    filename = os.path.join("..", "data", "input", "jira_records.csv")
    if os.path.exists(filename):
        print(f"{__file__}: {filename} exists, nothing to be done")
        return

    jira_api_base_url = "https://issues.apache.org/jira/"
    page_length = 500
    proj_jira_id = repo.upper()
    start_idx = 0
    total = 10**8
    final = []

    while total > start_idx:
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
        start_idx += page_length
        total = r_dict['total']
        final.append(r_dict)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['key', 'priority', 'created', 'status', 'versions'])
        for piece in final:
            for issue in piece['issues']:
                key = issue['key']
                priority = issue['fields']['priority']['name']
                created = issue['fields']['created']
                status = issue['fields']['status']['name']
                versions = ' '.join([version['name'] for version in issue['fields']['versions']])
                # print(key, priority, created, status, versions)
                writer.writerow([key, priority, created, status, versions])

if __name__ == "__main__":
    main("camel")
