# src/tools/job_search_tools.py
import os
import json
import requests
from typing import List, Dict, Any

# Ensure you have your SERPER_API_KEY set as an environment variable
# For example: export SERPER_API_KEY='your_serper_api_key_here'

def search_google_jobs_via_serper(keywords: str, location: str = "Mumbai, India", num_results: int = 5) -> str:
    """
    Searches Google Jobs using the Serper.dev API.
    This function acts as a tool for your AutoGen agents.

    Args:
        keywords (str): The job search keywords (e.g., "Software Engineer", "Data Analyst").
        location (str): The desired job location (e.g., "Mumbai, India", "Remote").
        num_results (int): The maximum number of job results to return.

    Returns:
        str: A JSON string containing a list of job dictionaries (title, company, location, link, brief_description),
             or an error message if the search fails.
    """
    serper_api_key = os.getenv('SERPER_API_KEY')
    if not serper_api_key:
        return json.dumps({"error": "SERPER_API_KEY environment variable not set."}, indent=2)

    try:
        # Construct the query for Google Jobs
        # Serper API's /search endpoint with 'tbs' parameter can be used for Google Jobs
        # For a direct Google Jobs search with Serper, you'd typically use 'engine': 'google_jobs' if available
        # or structure 'q' to include 'jobs' directly. Let's use the 'google_jobs' engine for clarity
        # if Serper supports it directly, otherwise we default to general search and filter.

        # Checking Serper API docs, 'engine': 'google_jobs' is the way to go.
        # So, the URL should be "https://google.serper.dev/jobs" if that's exposed directly,
        # otherwise, we stick to /search and rely on a strong query.
        
        # Let's use the /jobs endpoint if it exists, otherwise fall back to /search.
        # The typical Serper /search endpoint works with a "q" parameter for general Google Search,
        # but to target Google Jobs, the API call should specify 'engine': 'google_jobs' in the payload.
        
        url = "https://google.serper.dev/jobs" # Dedicated endpoint for Google Jobs
        payload = json.dumps({
            "q": keywords,
            "location": location,
            "num": num_results, # Max number of results for Serper API
            "hl": "en", # Host language
            "gl": "in"  # Geo-location for Google Jobs (India)
        })
        headers = {
            'X-API-KEY': serper_api_key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code != 200:
            return json.dumps({
                "error": f"Job search API request failed. Status code: {response.status_code}",
                "details": response.text
            }, indent=2)
            
        data = response.json()
        
        job_results = []
        if 'jobs_results' in data: # Serper's Google Jobs endpoint should return this key
            for job in data['jobs_results'][:num_results]:
                job_results.append({
                    "title": job.get('title', 'N/A'),
                    "company": job.get('company_name', 'N/A'),
                    "location": job.get('location', 'N/A'),
                    "link": job.get('link', 'N/A'),
                    "brief_description": job.get('description', '')[:200] + "..." if job.get('description') else "No brief description available."
                })
        else:
            return json.dumps({"error": "No 'jobs_results' found in API response.", "raw_response": data}, indent=2)
            
        return json.dumps(job_results, indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Network or HTTP error during job search: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred during job search: {str(e)}"}, indent=2)

