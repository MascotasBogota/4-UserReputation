
from src.clients import user_service_client, report_service_client
from config import SIGHTING_USEFUL, FINDING_USEFUL, FINDING_FALSE, SIGHTING_REMOVE

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
        current_response_reviewed = response_details.get("reviewed")
        current_status = response_details.get("is_useful")  # Estado actual de utilidad de la respuesta

        # 2. Calculate reputation change
        delta = 0
        is_useful = False
        response_reviewed = False
        
        if response_type == "avistamiento":
            if rating == "useful":
                # Solo se puede marcar como útil si no lo estaba previamente
                if current_response_reviewed is True and current_status is True:
                    raise ValueError("❌ Este avistamiento ya ha sido marcado como útil.")
                delta = SIGHTING_USEFUL
                is_useful = True
                response_reviewed = True
            elif rating == "not_useful":
                # Solo se puede marcar como no útil si previamente había sido marcado como útil
                if current_status is False:
                    raise ValueError("❌ No se puede marcar como no útil un avistamiento que no ha sido previamente marcado como útil.")
                delta = SIGHTING_REMOVE
                is_useful = False
                response_reviewed = True
            else:
                raise ValueError("❌ Rating inválido para avistamiento. Solo se permite 'useful' o 'not_useful'.")
                
        elif response_type == "hallazgo":
            if rating == "useful":
                if current_response_reviewed is True and current_status is True:
                    raise ValueError("❌ Este hallazgo ya ha sido marcado como útil.")
                delta = FINDING_USEFUL
                is_useful = True
                response_reviewed = True
            elif rating == "false_finding":
                if current_response_reviewed is True and current_status is False:
                    raise ValueError("❌ Este hallazgo ya ha sido marcado como falso.")
                delta = FINDING_FALSE
                is_useful = False
                response_reviewed = True
            else:
                raise ValueError("❌ Rating inválido para hallazgo. Solo se permite 'useful' o 'false_finding'.")
        else:
            raise ValueError("❌ Tipo de respuesta no válido.")

        # 3. Update user reputation
        update_result = user_service_client.update_user_reputation(author_id, delta,token)
        if not update_result:
            raise ConnectionError("❌ Could not update user reputation.")

        # 4. Mark response as rated
        status_result = report_service_client.update_response_status(report_id,response_id,response_reviewed, is_useful,token)
        if not status_result:
            # Note: This could lead to an inconsistent state. A rollback or retry mechanism might be needed here.
            raise ConnectionError("❌ Could not update response status.")
        resObject = {"status": "success","resp_auth":author_id ,"new_reputation": update_result.get("reputation"), "response":status_result}

        return resObject
