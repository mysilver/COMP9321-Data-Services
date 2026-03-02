"""
Modern Authentication Token using itsdangerous (v2+)

- Uses URLSafeTimedSerializer
- Built-in expiration handling
- Compatible with latest itsdangerous
"""

from time import sleep
from typing import Optional
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class AuthenticationToken:
    def __init__(self, secret_key: str, expires_in: int):
        """
        :param secret_key: Secret key used to sign tokens
        :param expires_in: Token expiration time in seconds
        """
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = URLSafeTimedSerializer(secret_key)

    def generate_token(self, username: str) -> str:
        """
        Generate a signed authentication token
        """
        payload = {
            "username": username
        }
        return self.serializer.dumps(payload)

    def validate_token(self, token: str) -> Optional[str]:
        """
        Validate token and return username if valid
        Raises:
            SignatureExpired
            BadSignature
        """
        data = self.serializer.loads(
            token,
            max_age=self.expires_in  # Built-in expiration check
        )
        return data["username"]


if __name__ == "__main__":

    SECRET_KEY = "A_SECRET_KEY_SHOULD_BE_LONG_RANDOM_STRING"
    expires_in = 10  # seconds

    auth = AuthenticationToken(SECRET_KEY, expires_in)

    # Generate token
    token = auth.generate_token("admin")
    print("Generated token:", token)

    # Validate token (valid case)
    try:
        username = auth.validate_token(token)
        print("Token is valid for user:", username)
    except SignatureExpired:
        print("Token expired")
    except BadSignature:
        print("Invalid token")

    # Wait until token expires
    sleep(expires_in + 1)

    # Expired token case
    try:
        auth.validate_token(token)
    except SignatureExpired:
        print("Token expired — get a new one")
    except BadSignature:
        print("Invalid token")

    # Invalid token case
    try:
        auth.validate_token("invalid.token.string")
    except SignatureExpired:
        print("Token expired")
    except BadSignature:
        print("Invalid token")