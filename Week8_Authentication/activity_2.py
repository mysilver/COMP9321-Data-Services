from time import sleep, time
from itsdangerous import JSONWebSignatureSerializer, BadSignature, SignatureExpired


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):

        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


if __name__ == "__main__":

    SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
    expires_in = 10
    auth = AuthenticationToken(SECRET_KEY, expires_in)
    token = auth.generate_token('admin')
    print("Generated token is:", token)

    info = auth.validate_token(token)
    print("The token decoded as:", str(info))

    sleep(expires_in + 1)

    try:
        expired_info = auth.validate_token(token)
    except SignatureExpired as e:
        print(e)
    except BadSignature  as e:
        print("Invalid Token")

    try:
        expired_info = auth.validate_token("sssssssssssss")
    except SignatureExpired as e:
        print(e)
    except BadSignature as e:
        print("Invalid Token")
