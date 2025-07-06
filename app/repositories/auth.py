import random
import string

from fastapi import HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app import schemas
from app.models import User
from app.security import create_jwt_token, get_password_hash, verify_password


def register(
    request: schemas.RegistrationRequest, db: Session
) -> schemas.BaseResponse:
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    user = User(
        name=request.name,
        email=request.email,
        password_hash=get_password_hash(request.password),
    )

    db.add(user)
    db.commit()

    return schemas.BaseResponse(message="Registration successful")


def login(request: schemas.LoginRequest, db: Session):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    token = create_jwt_token({"user_id": str(user.id)})

    return schemas.LoginResponse(token=token, verified=user.is_verified)


async def send_verification_code(user: schemas.User, redis: Redis):
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already verified",
        )

    code = "".join(random.choices(string.digits, k=6))

    key = f"verify:{user.id}"

    await redis.set(key, code, ex=600)

    return schemas.VerificationCodeResponse(
        message="Verification code sent", verification_code=code, expires_in=300
    )


async def verify_code(
    user: schemas.User, code: str, db: Session, redis: Redis
) -> schemas.User:
    key = f"verify:{user.id}"
    stored_code = await redis.get(key)

    if not stored_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired or not found",
        )

    _user = db.query(User).filter_by(id=user.id).first()
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    if stored_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )

    # Code is valid - update user and clean up
    await redis.delete(key)
    _user.is_verified = True
    db.commit()
    db.refresh(_user)

    return _user
