from flask import Flask, request, jsonify
import requests
from functools import wraps
import jwt

app = Flask(__name__)
ISSUER = "http://keycloak:8080/realms/master-realm"
CLIENT_ID = "flask-client"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({"message": "Missing token"}), 401

        token = auth.split(" ")[1]
        try:
            jwks = requests.get(f"{ISSUER}/protocol/openid-connect/certs").json()
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks['keys'][0])
            decoded = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
            request.user = decoded
        except Exception as e:
            return jsonify({"error": str(e)}), 403

        return f(*args, **kwargs)
    return decorated

@app.route("/public")
def public():
    return {"message": "Hello from a public route"}

@app.route("/protected")
@token_required
def protected():
    return {"message": f"Hello {request.user['preferred_username']}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

