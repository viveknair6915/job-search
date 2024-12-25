from flask import Flask, jsonify, request
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

apikey = '1366f18357msh2cbe30b9ea0dc66p189ae6jsne2235b01e8e3'
apihost = 'jobs-search-api.p.rapidapi.com'

logging.basicConfig(level=logging.DEBUG)

def getjobsbytechstack(techstack, location):
    url = f'https://{apihost}/getjobs'
    headers = {
        'X-RapidAPI-Host': apihost,
        'X-RapidAPI-Key': apikey
    }
    queryparams = {'search_term': techstack, 'location': location, 'results_wanted': '10'}
    try:
        response = requests.post(url, headers=headers, json=queryparams)
        response.raise_for_status()
        logging.debug("Response received: %s", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", e)
        return {"error": f"Failed to fetch data from the job API: {e}"}

@app.route('/jobs', methods=['GET'])
def getjobs():
    techstack = request.args.get('tech_stack', '')
    location = request.args.get('location', '')
    if techstack and location:
        jobs = getjobsbytechstack(techstack, location)
        return jsonify(jobs)
    else:
        return jsonify({"error": "Please provide both tech stack and location."})

def handler(request, *args, **kwargs):
    return app(*args, **kwargs)
