import jwt 

class SafeJWT: 
    def __init__(self, jwk_whitelist = None, jku_whitelist = None, kid_whitelist = None, verbose = True):
        """
        Initialises the whitelists for the web application
        Parameters:
            jwk_whitelist (list): The whitelisted embedded JWK sets (default is None)
            jku_whitelist (list): The whitelisted JWK Set URL (default is None)
            kid_whitelist (list): The whitelisted Key ID (default is None)
        """
        self.jwk_whitelist = jwk_whitelist 
        self.jku_whitelist = jku_whitelist 
        self.kid_whitelist = kid_whitelist

        # From https://github.com/wallarm/jwt-secrets
        self.common_secret = open("./jwt_common_secret.txt").read()
    
    def encode(self, payload, key, algorithm="HS256", headers=None, json_encoder=None):
        """
        Encode the payload as JSON Web Token

        Parameters:
            payload (dict): JWT claims, e.g. dict(iss=..., aud=..., sub=...)
            key (str): a key suitable for the chosen algorithm
            algorithm (str): algorithm to sign the token with, e.g. "ES256". If headers includes alg, it will be preferred to this parameter
            headers (dict): additional JWT header fields, e.g. dict(kid="my-key-id")
            json_encoder (json.JSONEncoder): custom JSON encoder for payload and headers
        
        Returns:
        A JSON Web Token, or raise exceptions if there is some checks that does not pass
        """
        
        # Checks for the publicly available JWT Secrets
        if key in self.common_secret:
            raise RuntimeError("Use of publicly known JWT secret!")
        
        return jwt.encode(payload, key, algorithm, headers, json_encoder)

    # TODO: Add checks later (if needed for kid directory traversal)
    def __check_jwk_whitelist(self, payload):
        """
        Checks if the specified jwk parameter is in the whitelist
        """
        return payload in self.jwk_whitelist
    
    def __check_jku_whitelist(self, payload):
        """
        Checks if the specified jku parameter is in the whitelist
        """
        return payload in self.jku_whitelist

    def __check_kid_whitelist(self, payload):
        """
        Checks if the specified kid parameter is in the whitelist
        """
        return payload in self.kid_whitelist

    def decode(self, jwt_token, key="", algorithms=None, options=None, audience=None, issuer=None, leeway=0):
        """
        Verify the jwt token signature and return the token claims.

        Parameters:
            jwt_token (str): the token to be decoded
            key (str): the key suitable for the allowed algorithm
            algorithms (list): allowed algorithms, e.g. ["ES256"]
            options (dict): extended decoding and validation options
            audience (Union[str]): optional, the value for verify_aud check
            issuer (str): optional, the value for verify_iss check
            leeway (float): a time margin in seconds for the expiration check
        
        Returns:
            The JWT claims, or raise exceptions if there is some value not in the whitelist
        """

        # Check data in the headers
        # Add in your own checks later
        headers = jwt.get_unverified_header(jwt_token)

        if 'jwk' in headers:
            if not self.__check_jwk_whitelist(headers['jwk']):
                raise RuntimeError("Non whitelisted JSON Web Keys found in token")
        
        if 'jku' in headers:
            if not self.__check_jku_whitelist(headers['jku']):
                raise RuntimeError("Non whitelisted JSON Web Key Set URL found in token")
        
        if 'kid' in headers:
            if not self.__check_kid_whitelist(headers['kid']):
                raise RuntimeError("Non whitelisted JSON Key ID found in token")

        # Checks for None algorithm
        if headers['alg'] == 'none':
            raise RuntimeError("Use of None algorithm is unsafe")

        return jwt.decode(jwt_token, key, algorithms, options, audience, issuer, leeway)
    
    def decode_complete(self, jwt_token, key="", algorithms=None, options=None, audience=None, issuer=None, leeway=0):
        """
        Identical to decode() except for return value which is a dictionary containing the token header (JOSE Header), the token payload 
        (JWT Payload), and token signature (JWT Signature) on the keys “header”, “payload”, and “signature” respectively.

        Parameters:
            jwt_token (str): the token to be decoded
            key (str): the key suitable for the allowed algorithm
            algorithms (list): allowed algorithms, e.g. ["ES256"]
            options (dict): extended decoding and validation options
            audience (Union[str]): optional, the value for verify_aud check
            issuer (str): optional, the value for verify_iss check
            leeway (float): a time margin in seconds for the expiration check
        
        Returns:
            Decoded JWT with the JOSE Header on the key header, the JWS Payload on the key payload, and the JWS Signature on the key signature. 
            Raise exception if there is some value not in the whitelist.      
        """

        # Check data in the headers
        # Add in your own checks later
        headers = jwt.get_unverified_header(jwt_token)

        if 'jwk' in headers:
            if not self.__check_jwk_whitelist(headers['jwk']):
                raise RuntimeError("Non whitelisted JSON Web Keys found in token")
        
        if 'jku' in headers:
            if not self.__check_jku_whitelist(headers['jku']):
                raise RuntimeError("Non whitelisted JSON Web Key Set URL found in token")
        
        if 'kid' in headers:
            if not self.__check_kid_whitelist(headers['kid']):
                raise RuntimeError("Non whitelisted JSON Key ID found in token")
                
        # Checks for None algorithm
        if headers['alg'] == 'none':
            raise RuntimeError("Use of None algorithm is unsafe")

        return jwt.api_jwt.decode_complete(jwt_token, key, algorithms, options, audience, issuer, leeway)
    
