import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-71tt1j9b.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    if "Authorization" not in request.headers:
        abort(401)

    auth_header = request.headers["Authorization"]
    auth_header_parts = auth_header.split(" ")

    if len(auth_header_parts) != 2:
        abort(401)
    elif auth_header_parts[0].lower() != "bearer":
        abort(401)

    print(auth_header_parts,'parts')

    token = auth_header_parts[1]

    print(token, 'token 1')

    return token


def verify_decode_jwt(token):

    print(token, 'verify 1')
    
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    print(unverified_header, 'verify 2')

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_authorization_header',
            'description': 'Authorization Header is malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://{}/'.format(AUTH0_DOMAIN)
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_authorization_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    raise AuthError({
        'code': 'invalid_authorization_header',
        'description': 'Unable to find the appropriate key.'
    }, 401)


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(403)
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()

            print(token, 'requires token')

            try:
                payload = verify_decode_jwt(token)

                print(payload, 'payload decode')

            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator