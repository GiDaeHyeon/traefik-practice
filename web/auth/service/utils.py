from datetime import datetime, timedelta, timezone

import jwt


class TokenManager:
    def __init__(self, secret: str) -> None:
        self.token_info = ["user_id", "email", "is_active"]
        self.secret_key = secret.get("SECRET")
        self.alg = secret.get("ALGORITHM")

    def create_token(self, payload: dict, exp_time: int) -> str:
        payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=exp_time)
        return jwt.encode(payload, self.secret_key, self.alg)

    def check_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.alg)
        except jwt.exceptions.PyJWTError:
            return {}
        return payload
