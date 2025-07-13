from flask import Flask, request
from flasgger import Swagger
from src.routes.reputation_routes import reputation_blueprint
import os
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET") 
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme."
        }
    }
}
#Swagger(app)
Swagger(app, config=swagger_config)

# Register the blueprint for reputation routes
app.register_blueprint(reputation_blueprint, url_prefix='/api')

@app.route("/")
def index():
    return "User Reputation Service is running."

# Métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])
ERROR_COUNT = Counter('http_request_errors_total', 'Total HTTP request errors', ['endpoint'])

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    latency = time.time() - request.start_time
    endpoint = request.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    if response.status_code >= 400:
        ERROR_COUNT.labels(endpoint=endpoint).inc()
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(port=5100, debug=True)