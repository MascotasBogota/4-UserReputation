
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.services.reputation_service import ReputationService
from src.utils.auth import get_current_user_id

reputation_blueprint = Blueprint('reputation_api', __name__)
reputation_service = ReputationService()

# A mock function to get user_id from a token
# In a real app, this would be handled by an authentication middleware


@reputation_blueprint.route("/rate-response/<string:report_id>/<string:response_id>", methods=['POST'])
@swag_from({
    'tags': ['Reputation'],
    'summary': 'Rate a response to a report',
    'description': 'Allows a report owner to rate a response as useful or a finding as true/false. This action calculates and applies a reputation change to the response author.',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'report_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The unique identifier of the report',
            'example': 'uuid-del-reporte'
        },
        {
            'name': 'response_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The unique identifier of the response being rated',
            'example': 'uuid-de-la-respuesta'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Rating',
                'required': ['rating'],
                'properties': {
                    'rating': {
                        'type': 'string',
                        'description': 'The rating to apply. For "avistamiento": useful (marks as useful), not_useful (removes useful mark, only if previously marked as useful). For "hallazgo": useful (marks as useful), false_finding (marks as false finding).',
                        'enum': ['useful', 'not_useful', 'false_finding'],
                        'example': 'useful'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Rating applied successfully.',
            'schema': {
                'properties': {
                    'status': {'type': 'string'},
                    'new_reputation': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Invalid input, missing required fields.'},
        401: {'description': 'Authentication required.'},
        403: {'description': 'User is not authorized to rate this response.'},
        503: {'description': 'Service unavailable, could not connect to dependent services.'}
    }
})
def rate_response(report_id, response_id):
    data = request.get_json()
    rating = data.get("rating")
    token = request.headers.get("Authorization")
    print(f"🆔 Token: {token}")
    
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    if not rating:
        return jsonify({"error": "rating is required"}), 400

    try:
        result = reputation_service.rate_response(report_id,response_id, rating, user_id,token)
        return jsonify(result), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 503 # Service Unavailable
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
