from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app import database, schemas
from app.redis import get_redis
from app.repositories import auth
from app.security import get_user

router = APIRouter(prefix="", tags=["auth"])

get_db = database.get_db


@router.post(
    "/register",
    response_model=schemas.BaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: schemas.RegistrationRequest, db: Session = Depends(get_db)
):
    return auth.register(request, db)


@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return auth.login(request, db)


@router.get("/me", response_model=schemas.User)
def current_user(user: schemas.User = Depends(get_user)):
    return user


@router.post("/verify", response_model=schemas.VerificationCodeResponse)
async def send_verification_code(
    user: schemas.User = Depends(get_user),
    redis: Redis = Depends(get_redis),
):
    return await auth.send_verification_code(user=user, redis=redis)


@router.get("/verify/{code}", response_model=schemas.User)
async def verify_code(
    code: str,
    user: schemas.User = Depends(get_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    return await auth.verify_code(user=user, code=code, db=db, redis=redis)
