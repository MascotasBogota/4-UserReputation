
import requests
from config import USER_SERVICE_URL

def update_user_reputation(user_id: str, delta: int,token:str):
    """Updates the user's reputation by a given delta."""
    try:
        print(f"⏱️ Updating reputation for user_id: {user_id} with delta: {delta}")
        response = requests.patch(f"{USER_SERVICE_URL}/api/profile/{user_id}/reputation", json={"reputation_delta": delta},
        headers={"Content-Type": "application/json",
                 "accept": "application/json",
                 "Authorization":token})
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"✅ Reputation updated successfully for user_id: {user_id}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        # Handle connection errors, timeouts, etc.
        print(f"❌ Error connecting to User Service: {e}")
        return None
