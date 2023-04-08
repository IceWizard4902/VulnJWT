import jwt
import time

# Implements the core logic for the path traversal vulnerability
# This uses a symmetrical key for ease of following
H256KEY = "eyJhbGciOiJIUzI1NiJ9.ew0KICAic3ViIjogIjEyMzQ1Njc4OTAiLA0KICAibmFtZSI6ICJBbmlzaCBOYXRoIiwNCiAgImlhdCI6IDE1MTYyMzkwMjINCn0.uUuL9YD8pNsK4YY4Fix42xZHPQ3H0pzggU5OffAeRIs"

def generate_token(username):
    return jwt.encode({"username": username, "admin": "false", "iat": int(time.time())}, H256KEY, algorithm="HS256", headers={"kid": "./secret/kid_key.txt"})

def validate_token(token):
    try:
        # Read kid header
        headers = jwt.get_unverified_header(token)
        kid = headers['kid']
        # Read file specified in kid header
        with open(kid, "r") as f:
            key = f.read()
        data = jwt.decode(token, key, algorithms=["HS256"])
        is_admin = (data["admin"] == "true")
        return is_admin
    except:
        return False 
