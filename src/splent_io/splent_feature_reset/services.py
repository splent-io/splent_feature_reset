from datetime import datetime, timezone

from flask import abort, current_app, url_for
from itsdangerous import BadTimeSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

from splent_framework.db import db
from splent_framework.services.BaseService import BaseService
from splent_io.splent_feature_auth.models import User
from splent_io.splent_feature_reset.models import ResetToken
from splent_io.splent_feature_reset.repositories import ResetRepository

TOKEN_MAX_AGE = 3600  # 1 hour


class ResetService(BaseService):
    def __init__(self):
        super().__init__(ResetRepository())

    def get_serializer(self):
        return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    def send_reset_password_mail(self, email: str) -> str | None:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None

        s = self.get_serializer()
        token = s.dumps(email, salt="email-confirm")
        link = url_for("reset.reset_password", token=token, _external=True)
        body = f"Your link to reset your password is {link}"

        mail_service = current_app.extensions.get("splent_mail_service")
        if not mail_service:
            raise RuntimeError("Mail service not available. Is splent_feature_mail installed?")
        mail_service.send_email("Password Reset Request", [email], body)

        return token

    def add_token(self, token: str | None):
        if token is None:
            return
        reset_token = ResetToken(token=token)
        db.session.add(reset_token)
        db.session.commit()

    def get_email_by_token(self, token: str) -> str:
        s = self.get_serializer()
        return s.loads(token, salt="email-confirm", max_age=TOKEN_MAX_AGE)

    def check_valid_token(self, token: str):
        s = self.get_serializer()
        try:
            s.loads(token, salt="email-confirm", max_age=TOKEN_MAX_AGE)
        except (SignatureExpired, BadTimeSignature):
            abort(404)

    def token_already_used(self, token: str) -> bool:
        reset_token = self.repository.get_by_column("token", token)
        if not reset_token:
            return False
        return reset_token[0].used_at is not None

    def reset_password(self, email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404)
        user.password = generate_password_hash(password)
        db.session.commit()

    def mark_token_as_used(self, token: str):
        reset_token = self.repository.get_by_column("token", token)
        if reset_token:
            reset_token[0].used_at = datetime.now(timezone.utc)
            db.session.commit()
