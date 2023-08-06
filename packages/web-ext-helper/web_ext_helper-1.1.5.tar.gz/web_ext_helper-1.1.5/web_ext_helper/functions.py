import time
import jwt
import typer

try:
    from .classes import bcolors
except ImportError:
    from classes import bcolors


def error(message: str):
    typer.echo(f"{bcolors.FAIL}Error: {message}{bcolors.ENDC}", err=True)
    raise typer.Exit(1)


def generate_jwt(api_key, api_secret):
    issued_at = int(time.time())
    expiration = issued_at + 300
    jwt_payload = {
        "iss": api_key,
        "jti": str(time.time()),
        "iat": issued_at,
        "exp": expiration,
    }
    jwt_token = jwt.encode(jwt_payload, api_secret, algorithm="HS256")
    return jwt_token
