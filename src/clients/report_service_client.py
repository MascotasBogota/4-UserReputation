
import requests
from config import REPORT_SERVICE_URL

def get_response_details(response_id: str):
    """Gets details for a specific response."""
    try:
        response = requests.get(f"{REPORT_SERVICE_URL}/v1/responses/{response_id}/details")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Report Service: {e}")
        return None

def update_response_status(response_id: str, is_useful: bool):
    """Updates the 'is_useful' status of a response."""
    try:
        response = requests.patch(f"{REPORT_SERVICE_URL}/v1/responses/{response_id}/status", json={"is_useful": is_useful})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Report Service: {e}")
        return None
