from flask import Flask, jsonify, request
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging to capture debugging information
logging.basicConfig(level=logging.DEBUG)

def getjobsbytechstack(techstack, location):
    """
    Function to fetch jobs from the GitHub Jobs API based on the tech stack and location.
    """
    # GitHub Jobs API endpoint
    url = 'https://jobs.github.com/positions.json'
    
    # Prepare query parameters
    queryparams = {'description': techstack, 'location': location}
    
    try:
        # Sending GET request to GitHub Jobs API
        response = requests.get(url, params=queryparams)
        response.raise_for_status()  # Raise exception for HTTP errors (non-2xx status codes)
        
        # Log the response data (for debugging purposes)
        logging.debug("Response received: %s", response.json())
        
        return response.json()  # Return the response data as JSON
    
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", e)
        return {"error": f"Failed to fetch data from the GitHub Jobs API: {e}"}

@app.route('/')
def home():
    """
    Home endpoint to show a welcome message and basic information about the API.
    """
    return jsonify({"message": "Welcome to the Job Search API. Use the /jobs endpoint to search for jobs."})

@app.route('/jobs', methods=['GET'])
def getjobs():
    """
    Endpoint to fetch jobs based on the tech stack and location parameters.
    """
    # Get tech_stack and location from query parameters
    techstack = request.args.get('tech_stack', '').strip()
    location = request.args.get('location', '').strip()
    
    # Validate that both parameters are provided
    if not techstack or not location:
        return jsonify({"error": "Please provide both tech stack and location."}), 400
    
    # Fetch jobs based on the tech stack and location using the GitHub Jobs API
    jobs = getjobsbytechstack(techstack, location)
    
    # Check if there was an error in fetching jobs
    if 'error' in jobs:
        return jsonify(jobs), 500
    
    # Return jobs data if found
    if jobs:
        return jsonify(jobs), 200
    else:
        return jsonify({"message": "No jobs found for the given criteria."}), 404

if __name__ == '__main__':
    """
    Run the Flask application on port 5001 with debugging enabled.
    """
    app.run(host='0.0.0.0', port=5001, debug=True)
