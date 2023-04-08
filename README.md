# VulnJWT

## What is this about?

This is a Flask application which is vulnerable to some JWT injection attacks. The attacks are inspired from the [PortSwigger Academy JWT lab](https://portswigger.net/web-security/jwt).

The project is in the CS5331 module in NUS.

## How to run?
- Install the necessary modules by doing `pip install -r requirements.txt`
- Install [PostgreSQL](https://www.postgresql.org/download/), then run the commands in the `commands.sql` file to initialize the necessary database and tables for the program.
- Finally, run `py app.py` and the application should be up and running.

TODO later: Include some Docker containers to simplify the process of installation.

## Mitigation

- The `SafeJWT` tool, which helps defend against the injection attacks, using whitelisting is in the `mitigation` branch. The application's vulnerable logic (in the `jku.py`, `jwk.py` and `kid.py` files) are fixed.
- `SafeJWT` is a wrapper to the API provided by [pyjwt](https://github.com/jpadilla/pyjwt).

Example usage:

```python
from safejwt import SafeJWT

# Include the whitelist for your application
pub_key = {
    "kty": "RSA",
    "e": "AQAB",
    "kid": "27e4c55f-e26d-4b1c-988f-92730eb7d8c5",
    "n": "uEhz3iAuN_etlzYTdiMNBCC18ibi2x1Jz7JM3iZT1K1Ph-bzJu6DYDkJZWarZ4fGenMIZHx8zae-xULE2IEfCuXoGeBiExLLGSD-mJQ5vmjdeajuo0V9dQMvElnvYgxc4AIheJPOqmJVA3DMAUJcXMzbLnWh3MWMDUNTqcFK4zihGPmTkk9luJLqE5LNADclweORq-vqHKOC3vKE_r4AQWKp7T2y2HoW7Q8pMJ8tq3md1yIO5Pi1EJvfJ0U-iJQmAOXy3ePvVE0Lh-uo_YfqW4NoMSVBlyfuY8AARmLGFlWOoOgp1jV0gICDwwTQDZ5tVueDtN_G-TigKrVT_Y1Z2Q"
}
jwk_whitelist = [pub_key]

jwt_signer = SafeJWT(jwk_whitelist = jwk_whitelist)

# Do encoding and decoding accordingly, use the same as pyjwt
jwt_signer.encode(...)
```

