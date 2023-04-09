# Proof of Concepts

The `jku_evil.py` and `kid_evil.py` serves as two malicious server to facilitate the injection to the `jku` and `kid` parameter. Note that the two evil servers are on a different version of the application, so please try to read the code to understand what's going on.

TODO: Change the code a bit so it is easier to set up the "evil" server

Run the server using Python and Flask. Example command: `py jku_evil.py`

Otherwise, please check out the PortSwigger JWT Lab to see how to exploit the application using Burp Suite and the JSON Web Token extension. The application should be exploitable using the techniques from the PortSwigger application.