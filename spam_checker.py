import requests

API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def is_spam(payload):	
    output = query({
        "inputs": payload,
    })

    spam_label = None
    relevant_label = None

    for e in output:
        if e['label'] == 'LABEL_0':
             spam_label = e['score']
        if e['label'] == 'LABEL_1':
             relevant_label = e['score']
    
    return spam_label >= relevant_label
