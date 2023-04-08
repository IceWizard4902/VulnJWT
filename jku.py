import jwt
from jwt import PyJWKClient
import time

# Implements the vulnerability which allows arbitrary signing 
# Generated from https://mkjwk.org/

PRIV_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxWdA3gp/VQvnZ
pCF+4QvfQrEhrC3iAVxuKHUJDdeze5j9HNGxlLx2QP7rY/qthHE2YeuXPuO3obeJ
vu+X0WK3kIDgjvR6QDy4Gz0cVXBAZtIHmBPVtcOpKLL71fq8umxtChoUPyhwauue
h7vUS97/6EUYE9aZVHeVMZVhT1fUdYPRW4t1pHAyDmNdZ9s15qLoQyF6GnmhjORt
UobJZ983LyWykqWTZM5J5Ly3Slst4MCV6mPrWRj3/fNltV6hssaU+Tbn7SojDzK0
H91kAzbbQJqcwhCxdB2zsmLFrsv3bi4RuyypmoVAXgW9C8UxPkK/nQp6lmEy4+Zn
zBfpJ2v5AgMBAAECggEAYaOxx63psy6xgYokSsc5kwwTmxdBF4lqSteJP5fYZl8o
pklkhSD+9RfpgMzFaRxee/NDEjy0gBfPhU2SeQH1GFy9J2Rs4pVVGIMejOfY6gvx
m+61FNaCRzI5//4ZkigMo6eJHhZ7fBDRcbEGzuWKe1d0GsJpRndDcuced7mIAFZX
6+Qd0fZLI8S+Xg1xeEhMDmwrDC0YMylhq55MA3x36I/gfmuVqkL49nnS0MwMNM2P
hzaV3qp40IYAmkMpwyJcASWmcIEqr45xsxixJQSoA64jMTYnAM9FUN3RIyXgUTgT
OS66IWQCIRzphchriz32TrGOeGouZKHPrRCZ/xNsgQKBgQD/QzaZOyDcYaflGZu4
RUKEJwI9xPWYWlk+jWbSLCcewkhxmnMtXusEoX3g8zX93xgXMqK9nDw11Zi6FQZQ
Mkh9pM3haMK5LQ06RBGDikzH/jgfksHkOJrWsNz+89ZxvEsqiJTNYwnW4ZBSTHad
GZMyVt8nlh1/PY8kCW678AGqKQKBgQCx3PptUlwmITcExNwGod9XRt4g+MRTmbUD
1CD6fvQHdvQFS8vcF3AYGw3FDMqlWIjCq190CcMv3k/J3qxuVpTP7xYO/b0pEyzH
3+wmkZsm6L0x5loqwyzxRbfzvrk+eV9j74iAv+05/q9ttChAObbYYZc+tgIwddnj
8ZgXq6iNUQKBgFBZQtVm1EgqgSPPNMIDIxXgBYeV+MyVG+RhtAzSExpOg2km+bw9
VXLmtm3ZgJRB5h5fNPTEOfukGWfxeEREH6dU+e1LAYgyUyiVBoJGRTbqoZXmpxuE
adDMaTPjYwv3/h0MUvJ3i0BVTg1pvihjRX8h8ypNyUklAmqQgYes24lJAoGADMyG
CM/gaa4CM4mm+6MyWylyWpUMK6fn6rqdFOmFzfO1Y5wss03Mdy+bMg7Vlkhkrv1+
BO+e6BbrTu+DIP2B/+SIhdOkhQwoMMngSHY53/bnhmu5GVKqLUKDFjsnQWOihaJ7
BCjLfVziataH/vcoPTHonE6kobAZWdnMxAdKPcECgYEA9CiroW64j0xIGOyOImOj
55CCBStiTDXkRFjvIqqM+eSFKiDPH3kJsQi4M3DIjY/rmEVhwitWxSN+xD0yeQmK
USIankxvES2JLb2orYTz8BjzGY3tbZ87k1L3SXuoVD+umR93bT7viDDK2W7lpugy
YTbcHdJfY/ZhA5BP9JT5eY0=
-----END PRIVATE KEY-----"""

def generate_token(username):
    return jwt.encode({"username": username, "admin": "false", "iat": int(time.time())}, PRIV_KEY, algorithm="RS256", headers={"jku": "http://localhost:5000/public_keys.json", "kid": "Nzv4oc46mMpaVnzKHKzTmh2Ajip_ITEGZLoGCbkZBIg"})

def validate_token(token):
    try:
        headers = jwt.get_unverified_header(token)
        jwks_client = PyJWKClient(headers["jku"])
        pub_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(token, pub_key.key, algorithms=["RS256"])
        is_admin = (data["admin"] == "true")
        return is_admin
    except:
        return False