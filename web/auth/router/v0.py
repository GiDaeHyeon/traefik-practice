from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, HTTPException, status

from model import schema
from model.conn import get_db
from service import auth_service

router = APIRouter(prefix="/auth")


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def sign_up(data: schema.CreateUser, db: Session = Depends(get_db)):
    if auth_service.create_user(db=db, data=data):
        return {"detail": "created"}


@router.post("/sign-in", status_code=status.HTTP_200_OK)
def sign_in(data: schema.CheckUser, db: Session = Depends(get_db)):
    payload = auth_service.check_user(db=db, data=data)
    if payload:
        access_token = auth_service.create_access_token(payload=payload)
        refresh_token = auth_service.create_save_refresh_token(db=db, payload=payload)
        return {"detail": "ok",
                "tokens": {"access_token": access_token, "refresh_token": refresh_token}}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid_email_or_password"
    )


@router.get("/validation", status_code=status.HTTP_200_OK)
def validate(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    payload = auth_service.check_access_token(token=token)
    if payload:
        access_token = auth_service.create_access_token(payload=payload)
        return {"detail": "ok", "tokens": {"access_token": access_token}}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid_token"
    )


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(data: schema.CheckToken, db: Session = Depends(get_db)):
    payload = auth_service.check_refresh_token(db=db, data=data)
    if payload:
        access_token = auth_service.create_access_token(payload=payload)
        return {"detail": "ok", "tokens": {"access_token": access_token}}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid_token"
    )


@router.post("/log-out", status_code=status.HTTP_200_OK)
def log_out(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization", "")
    payload = auth_service.check_access_token(token=token)
    print(payload)
    if payload and auth_service.delete_refresh_token(db=db, payload=payload):
        return {"detail": "ok"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid_token"
    )
