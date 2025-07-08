
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.services.reputation_service import ReputationService
from src.utils.auth import get_current_user_id

reputation_blueprint = Blueprint('reputation_api', __name__)
reputation_service = ReputationService()

# A mock function to get user_id from a token
# In a real app, this would be handled by an authentication middleware


@reputation_blueprint.route("/rate-response", methods=['POST'])
@swag_from({
    'tags': ['Reputation'],
    'summary': 'Rate a response to a report',
    'description': 'Allows a report owner to rate a response as useful or a finding as true/false. This action calculates and applies a reputation change to the response author.',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Rating',
                'required': ['report_id','response_id', 'rating'],
                'properties': {
                    'report_id': {
                        'type': 'string',
                        'description': 'The unique identifier of the report',
                        'example': 'uuid-de-la-respuesta'
                    },
                    'response_id': {
                        'type': 'string',
                        'description': 'The unique identifier of the response being rated.',
                        'example': 'uuid-de-la-respuesta'
                    },
                    'rating': {
                        'type': 'string',
                        'description': 'The rating to apply.',
                        'enum': ['useful', 'false_finding'],
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
def rate_response():
    data = request.get_json()
    report_id = data.get("report_id")  
    response_id = data.get("response_id")
    rating = data.get("rating")
    token = request.headers.get("Authorization")
    print(f"🆔 Token: {token}")
    
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    if not response_id or not rating:
        return jsonify({"error": "response_id and rating are required"}), 400

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
