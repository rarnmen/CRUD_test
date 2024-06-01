import requests
from datetime import datetime as dt
def trigger_dag(dag_id, id):
    url = f'http://localhost:8080/api/v1/dags/{dag_id}/dagRuns'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "logical_date": dt.today().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "execution_date": dt.today().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "conf": {"id":id },
        "note": "Testing",
        }
    auth = ('kikilatam', 'test')
    response = requests.post(url, headers=headers, json=data, auth=auth)
    return response.text, response.status_code

