from flask import Flask
from flasgger import Swagger
from src.routes.reputation_routes import reputation_blueprint

app = Flask(__name__)
Swagger(app)

# Register the blueprint for reputation routes
app.register_blueprint(reputation_blueprint, url_prefix='/api')

@app.route("/")
def index():
    return "User Reputation Service is running."

if __name__ == '__main__':
    app.run(port=5000, debug=True)