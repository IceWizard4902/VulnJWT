import jwt 
from jwt import PyJWK
import time 

# Generate from Burp Suite 
key = {
    "p": "_27nIEMA9xVZopw5Ab6R2zpilvz4CB17wu1rRAOH1rq_aULwyB4OfPfDkdO_QDUNK9eMARmoSyNQzhR2cOA-55Ea0cQ34wQ08zQ1hB-Z8Oovv2LJWoUqbW0ac9i7r0fKA_v3PVGrLaPvvgdxlx3nd-VyjGaAwNJd_uljS8F1wOE",
    "kty": "RSA",
    "q": "uLEiJHyzFtOmiZTbnp91KXMYCVlyT3F_m3pMwK4vdKsYiF15iapmEDhf3A_SwGB2Z0Ikd4u1iuXkKvjxMls2xbz7Kj2Md3IkxO9sgIDHtXzm-qhgM6kchC2JuObz3Lx7BZZ_GL8yxEhGzcyqxY0yHXr5GkdtN-RFsH5Yg8FZn_k",
    "d": "C1nVHzu6tRJRtDRtvvNaQCSWqG96PjZf30Xzg6R3Oeyh7zRLylxbJcBlooQQLzyW_mBbBjt_wXghYUujTdWoOJbgNMXULKoV7fqRDAtnQiH58F42MsLbPyueyOHWw6KQzvB6qM9r5aVQaLmYK0Sv5TxuDL7MpUlavs9klhp0lynA8GJ27HSKlFvMy-hrLeNKilQLd3GXehe_BUQKdpQg7DvvbbYAbsj0irk3bH_RBN8GmtQmBc1viuhs6G90uyuTEiqKoVTlqcUs4ArEL8OlYGcYU_kcvCtNjsKixROBkm7Hj1P2EBv7jFBBEAtr3gfiOIm5G84lnwbHDK9rWFcewQ",
    "e": "AQAB",
    "kid": "27e4c55f-e26d-4b1c-988f-92730eb7d8c5",
    "qi": "3vYTrwK1Ak07v9-UUv6WVUgNAuWRveXFecWIlDV5lsCtR_7NZ4GoWp5UDdw5MojMVya3mVtcDGtL_MBOjdMSocs78kbC4DiQcREvHAXqLNZnUPDX8Jf0nAUe-_IsFzZb-dt1_estpal2ytPbodFOn11Vws0a2LTkpFl_lhLgCe0",
    "dp": "YU5YUdv0lCvX97BXryhv2_oD8Mzxl_XTXdCgGkrWBqEhpfHQVAvPLSAdqoHly4nqOJdmSE0D5YvQjpERBbMHg6OtedesCplhqnxrHqgDNtmf0uLJHei43vK_Lv6TkRRiCt6DsyJXeY2IGPYw-YZ01SHdX0r1JX9-O0uhfgx21UE",
    "dq": "QXILLjC96U3QipokBJ5ujuSI1O9MMVh_pmF9Bx3yFP538AJnid_G0OKZHUrCHIdSDZ8DexUXnIOACbYzCewGiaVAvyQWPVFGND6_DP4VRntfAd1eUZAQWcolLk8whLyJP16n5OYDoEgYRt7KeLxi0M19rdE3o4GRLExpIy8Fikk",
    "n": "uEhz3iAuN_etlzYTdiMNBCC18ibi2x1Jz7JM3iZT1K1Ph-bzJu6DYDkJZWarZ4fGenMIZHx8zae-xULE2IEfCuXoGeBiExLLGSD-mJQ5vmjdeajuo0V9dQMvElnvYgxc4AIheJPOqmJVA3DMAUJcXMzbLnWh3MWMDUNTqcFK4zihGPmTkk9luJLqE5LNADclweORq-vqHKOC3vKE_r4AQWKp7T2y2HoW7Q8pMJ8tq3md1yIO5Pi1EJvfJ0U-iJQmAOXy3ePvVE0Lh-uo_YfqW4NoMSVBlyfuY8AARmLGFlWOoOgp1jV0gICDwwTQDZ5tVueDtN_G-TigKrVT_Y1Z2Q"
}

pub_key = {
    "kty": "RSA",
    "e": "AQAB",
    "kid": "27e4c55f-e26d-4b1c-988f-92730eb7d8c5",
    "n": "uEhz3iAuN_etlzYTdiMNBCC18ibi2x1Jz7JM3iZT1K1Ph-bzJu6DYDkJZWarZ4fGenMIZHx8zae-xULE2IEfCuXoGeBiExLLGSD-mJQ5vmjdeajuo0V9dQMvElnvYgxc4AIheJPOqmJVA3DMAUJcXMzbLnWh3MWMDUNTqcFK4zihGPmTkk9luJLqE5LNADclweORq-vqHKOC3vKE_r4AQWKp7T2y2HoW7Q8pMJ8tq3md1yIO5Pi1EJvfJ0U-iJQmAOXy3ePvVE0Lh-uo_YfqW4NoMSVBlyfuY8AARmLGFlWOoOgp1jV0gICDwwTQDZ5tVueDtN_G-TigKrVT_Y1Z2Q"
}

def generate_token(username):
    signing_key = PyJWK.from_dict(key).key
    return jwt.encode({"username": username, "admin": "false", "iat": int(time.time())}, signing_key, algorithm="RS256", headers={"jwk": pub_key})

def validate_token(token):
    try:
        headers = jwt.get_unverified_header(token)
        signing_key = PyJWK.from_dict(headers["jwk"])
        data = jwt.decode(token, signing_key.key, algorithms=["RS256"])
        is_admin = (data["admin"] == "true")
        return is_admin
    except:
        return False
