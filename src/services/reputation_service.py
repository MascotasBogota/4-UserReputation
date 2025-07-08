
from src.clients import user_service_client, report_service_client
from config import SIGHTING_USEFUL, FINDING_USEFUL, FINDING_FALSE

class ReputationService:
    def rate_response(self,report_id:str,response_id: str, rating: str, user_id: str,token:str):
        # 1. Get response details to validate owner
        response_details = report_service_client.get_response_details(report_id,response_id)
        if not response_details:
            raise ConnectionError("❌ Could not connect to Report Service.")
        
        report_details = report_service_client.get_report_details(report_id)
        if not report_details:
            raise ConnectionError("❌ Could not connect to Report Service for report details.")

        if report_details.get("user_id") != user_id:
            raise PermissionError("❌ User is not the owner of the report.")

        response_type = response_details.get("type")
        author_id = response_details.get("resp_user_id")

        # 2. Calculate reputation change
        delta = 0
        is_useful = False
        if response_type == "avistamiento" and rating == "useful":
            delta = SIGHTING_USEFUL
            is_useful = True
        elif response_type == "hallazgo":
            if rating == "useful":
                delta = FINDING_USEFUL
                is_useful = True
            elif rating == "false_finding":
                delta = FINDING_FALSE
                is_useful = False
        else:
            raise ValueError("❌ Invalid rating for the given response type.")

        # 3. Update user reputation
        update_result = user_service_client.update_user_reputation(author_id, delta,token)
        if not update_result:
            raise ConnectionError("❌ Could not update user reputation.")

        # 4. Mark response as rated
        status_result = report_service_client.update_response_status(report_id,response_id, is_useful,token)
        if not status_result:
            # Note: This could lead to an inconsistent state. A rollback or retry mechanism might be needed here.
            raise ConnectionError("❌ Could not update response status.")

        return {"status": "success", "new_reputation": update_result.get("new_reputation")}
