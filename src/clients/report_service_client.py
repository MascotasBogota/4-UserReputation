
import requests
from config import REPORT_SERVICE_URL

def get_response_details(report_id:str,response_id: str):
    """Gets details for a specific response."""
    try:
        print(f"⏱️Fetching response details for report_id: {report_id}, response_id: {response_id}")
        response = requests.get(f"{REPORT_SERVICE_URL}/responses/{report_id}/{response_id}")
        response.raise_for_status()
        print(f"✅Response details fetched successfully for report_id: {report_id}, response_id: {response_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to Report Service: {e}")
        return None

def get_report_details(report_id:str):
    """Gets details for a specific response."""
    try:
        print(f"⏱️Fetching report details for report_id: {report_id}")
        report = requests.get(f"{REPORT_SERVICE_URL}/reports/public/{report_id}")
        report.raise_for_status()
        print(f"✅Report details fetched successfully for report_id: {report_id}")
        return report.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to Report Service: {e}")
        return None

def update_response_status(report_id:str,response_id: str, response_reviewed:bool,is_useful: bool,token:str):
    """Updates the 'is_useful' status of a response."""
    try:
        print(f"⏱️Updating response status for report_id: {report_id}, response_id: {response_id}, is_useful: {is_useful}")
        response = requests.patch(f"{REPORT_SERVICE_URL}/responses/{report_id}/{response_id}/patch", json={"is_useful": is_useful, "reviewed":response_reviewed},headers={"Content-Type": "application/json",
                 "Authorization":token})
        response.raise_for_status()
        print(f"✅Response status updated successfully for report_id: {report_id}, response_id: {response_id}")
        print(f"Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to Report Service: {e}")
        return None
