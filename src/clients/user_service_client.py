
import requests
from config import USER_SERVICE_URL

def update_user_reputation(user_id: str, delta: int):
    """Updates the user's reputation by a given delta."""
    try:
        response = requests.patch(f"{USER_SERVICE_URL}/v1/users/{user_id}/reputation", json={"delta": delta})
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error connecting to User Service: {e}")
        return None
