# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default=(
        "https://sentianalyzer.1m4e98nfslx4."
        "us-south.codeengine.appdomain.cloud/"
    )
)


def get_request(endpoint, **kwargs):
    # Use urlencode to handle query parameters safely
    params = urlencode(kwargs) if kwargs else ""

    # Ensure the backend_url ends with a '/' to prevent issues
    request_url = f"{backend_url}{endpoint}"

    if params:
        request_url += f"?{params}"

    print(f"GET FROM {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None


def analyze_review_sentiments(text):
    print(text)
    request_url = sentiment_analyzer_url+"analyze/"+text
    print(request_url)
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        print(response)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
