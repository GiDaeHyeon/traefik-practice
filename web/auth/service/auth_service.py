import json

import bcrypt
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from model import schema
from model.table import Users, Tokens
from .utils import TokenManager

with open("./secret.json", "r") as fp:
    secret = json.load(fp)["KEY"]

TM = TokenManager(secret=secret)


def create_user(db: Session, data: BaseModel) -> bool:
    hashed_password = bcrypt.hashpw(
        password=data.password.encode("utf8"),
        salt=bcrypt.gensalt()).decode("utf8")
    try:
        db.add(Users(email=data.email, password=hashed_password))
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="integrity_error"
        )
    return True


def check_user(db: Session, data: schema.CheckUser) -> dict:
    try:
        hashed_password = (
            db.query(Users)
            .filter(Users.email == data.email)
            .with_entities(Users.password)
            ).one()[0].encode("utf8")
    except NoResultFound:
        return {}
    if bcrypt.checkpw(data.password, hashed_password):
        user_info = (
            db.query(Users)
            .filter(Users.email == data.email)
            .with_entities(
                Users.id,
                Users.email,
                Users.is_active
            )
        ).one()
        payload = {k: v for k, v in zip(TM.token_info, user_info)}
        return payload if payload.get("is_active") else {}
    return {}


def create_access_token(payload: dict, exp_time: int = 3600) -> str:
    return TM.create_token(payload=payload, exp_time=exp_time)


def create_save_refresh_token(db: Session, payload: dict, exp_time: int = 2629700) -> str:
    token = TM.create_token(payload=payload, exp_time=exp_time)
    try:
        db.add(Tokens(user_id=payload.get("user_id"), token=token))
        db.commit()
    except IntegrityError:
        delete_refresh_token(db=db, payload=payload)
        db.add(Tokens(user_id=payload.get("user_id"), token=token))
        db.commit()
    except (KeyError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid_payload"
        )
    return token


def delete_refresh_token(db: Session, payload: dict) -> bool:
    try:
        db.query(Tokens).filter(Tokens.user_id == payload.get("user_id")).one()
    except NoResultFound:
        return False
    db.query(Tokens).filter(Tokens.user_id == payload.get("user_id")).delete()
    db.commit()
    return True


def check_access_token(token: str) -> dict:
    try:
        valid_token = schema.CheckToken(token=token)
        return TM.check_token(token=valid_token.token)
    except ValidationError:
        return {}


def check_refresh_token(db: Session, token: BaseModel) -> dict:
    valid_token = token.token
    try:
        payload = TM.check_token(token=valid_token)
    except ValidationError:
        return {}
    token_info = (
        db.query(Tokens)
        .filter(Tokens.token == valid_token)
    ).one()
    if token_info:
        return payload
    return {}
