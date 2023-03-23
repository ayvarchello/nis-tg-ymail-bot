import requests
import config

headers = {"Authorization": f"Bearer {config.SPAM_AUTH_TOKEN}"}

def query(payload):
	response = requests.post(config.API_URL, headers=headers, json=payload)
	return response.json()

def is_spam(payload):	
    output = query({
        "inputs": payload,
    })

    spam_label = None
    relevant_label = None
    if not isinstance(output, list):
        return False

    for e in output[0]:
        if e['label'] == 'LABEL_0':
             spam_label = e['score']
        if e['label'] == 'LABEL_1':
             relevant_label = e['score']
    
    return spam_label >= relevant_label
