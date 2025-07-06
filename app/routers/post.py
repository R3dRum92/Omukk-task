from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.repositories import auth, post
from app.security import get_user, get_user_strict

router = APIRouter(prefix="/posts", tags=["posts"])

get_db = database.get_db


@router.get("/", response_model=list[schemas.PostView])
def get_all_posts(
    user: schemas.User = Depends(get_user), db: Session = Depends(get_db)
):
    return post.get_all_posts(user, db)


@router.get("/{post_id}", response_model=schemas.PostView)
def get_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user),
):
    return post.get_post_by_post_id(user=user, post_id=post_id, db=db)


@router.post(
    "/create",
    response_model=schemas.PostView,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    content: schemas.PostCreate,
    user: schemas.User = Depends(get_user_strict),
    db: Session = Depends(get_db),
):
    return post.create_post(user, content, db)


@router.put("/{post_id}", response_model=schemas.PostView)
def edit_post(
    post_id: UUID,
    update: schemas.PostEdit,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user_strict),
):
    return post.edit_post(user=user, post_id=post_id, info=update, db=db)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id=UUID,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user_strict),
):
    post.delete_post(user=user, post_id=post_id, db=db)


@router.post("/{post_id}/like", response_model=schemas.PostView)
def toggle_like(
    post_id: UUID,
    user: schemas.User = Depends(get_user_strict),
    db: Session = Depends(get_db),
):
    return post.toggle_like(user=user, post_id=post_id, db=db)
