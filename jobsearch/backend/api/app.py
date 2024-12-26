from flask import Flask, jsonify, request
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

apikey = '8286240622msh67b2fe7d3f080f9p159d69jsn3e21985ef294'
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
    techstack = request.args.get('tech_stack', '').strip()
    location = request.args.get('location', '').strip()
    
    if not techstack or not location:
        return jsonify({"error": "Please provide both tech stack and location."}), 400
    
    jobs = getjobsbytechstack(techstack, location)
    
    if 'error' in jobs:
        return jsonify(jobs), 500
    
    if 'jobs' in jobs and jobs['jobs']:
        return jsonify(jobs), 200
    else:
        return jsonify({"message": "No jobs found for the given criteria."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
