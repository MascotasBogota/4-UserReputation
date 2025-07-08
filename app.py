from flask import Flask
from flasgger import Swagger
from src.routes.reputation_routes import reputation_blueprint
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET") 
Swagger(app, config={
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme."
        }
    },
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
     "headers": [],
    "specs_route": "/apidocs/" 
})

# Register the blueprint for reputation routes
app.register_blueprint(reputation_blueprint, url_prefix='/api')

@app.route("/")
def index():
    return "User Reputation Service is running."

if __name__ == '__main__':
    app.run(port=5100, debug=True)