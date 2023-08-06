import base64
import json

import jwt
import requests
from django.utils.functional import cached_property
from jwt.algorithms import ECAlgorithm, RSAAlgorithm

from django_jwt import settings


class OIDCHandler:
    def get_alg(self, token: str) -> str:
        header = json.loads(base64.b64decode(token.split(".")[0] + "==="))
        return header["alg"]

    @cached_property
    def config(self) -> dict:
        return requests.get(settings.OIDC_CONFIG_URL).json()

    @cached_property
    def public_keys(self) -> dict:
        certs_data = requests.get(self.config["jwks_uri"]).json()
        public_keys = {}
        for key_data in certs_data["keys"]:
            if key_data["kty"] == "RSA":
                public_keys[key_data["alg"]] = RSAAlgorithm.from_jwk(json.dumps(key_data))
            elif key_data["kty"] == "EC":
                public_keys[key_data["alg"]] = ECAlgorithm.from_jwk(json.dumps(key_data))
        return public_keys

    def get_user_info(self, token: str) -> dict:
        return requests.get(
            self.config["userinfo_endpoint"],
            headers={"Authorization": f"Bearer {token}"},
        ).json()

    def decode_token(self, token: str) -> dict:
        alg = self.get_alg(token)
        return jwt.decode(
            token,
            key=self.public_keys[alg],
            algorithms=[alg],
            audience=settings.OIDC_AUDIENCE,
            options={"verify_aud": False},
        )


oidc_handler = OIDCHandler()
