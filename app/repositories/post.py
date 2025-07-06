from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.models import Like, Post, User
from app.security import create_jwt_token


def get_all_posts(user: schemas.User, db: Session) -> list[schemas.PostView]:
    _posts = db.query(Post).order_by(Post.created_at.desc()).all()
    posts = []
    for post in _posts:
        author = db.query(User).filter_by(id=post.user_id).first()
        likes = db.query(Like).filter_by(post_id=post.id).count()
        liked = (
            db.query(Like).filter_by(post_id=post.id, user_id=user.id).first()
            is not None
        )

        _post = schemas.PostView(
            id=post.id,
            content=post.content,
            author=schemas.User.model_validate(author),
            likes=likes,
            liked=liked,
            time=post.time,
        )
        posts.append(_post)

    return posts


def get_post_by_post_id(
    user: schemas.User, post_id: UUID, db: Session
) -> schemas.PostView:
    _post = db.query(Post).filter_by(id=post_id).first()

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    author = db.query(User).filter_by(id=_post.user_id).first()
    likes = db.query(Like).filter_by(post_id=_post.id).count()
    liked = (
        db.query(Like).filter_by(post_id=_post.id, user_id=user.id).first()
        is not None
    )

    return schemas.PostView(
        id=_post.id,
        content=_post.content,
        author=schemas.User.model_validate(author),
        likes=likes,
        liked=liked,
        time=_post.time,
    )


def create_post(
    user: schemas.User, content: schemas.PostCreate, db: Session
) -> schemas.PostView:
    if not content.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content empty",
        )
    new_post = Post(user_id=user.id, content=content.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    post = schemas.PostView(
        id=new_post.id,
        content=new_post.content,
        author=schemas.User.model_validate(user),
        likes=0,
        liked=False,
        time=new_post.time,
    )

    return post


def edit_post(
    user: schemas.User, post_id: UUID, info: schemas.PostEdit, db: Session
) -> schemas.PostView:
    if not info.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content empty",
        )

    _post = db.query(Post).filter_by(id=post_id).first()
    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if _post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    _post.content = info.content
    db.commit()
    db.refresh(_post)

    author = db.query(User).filter_by(id=_post.user_id).first()
    likes = db.query(Like).filter_by(post_id=_post.id).count()
    liked = (
        db.query(Like).filter_by(post_id=_post.id, user_id=user.id).first()
        is not None
    )

    return schemas.PostView(
        id=_post.id,
        content=_post.content,
        author=schemas.User.model_validate(author),
        likes=likes,
        liked=liked,
        time=_post.time,
    )


def delete_post(user: schemas.User, post_id: UUID, db: Session):
    _post = db.query(Post).filter_by(id=post_id).first()

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if _post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    db.delete(_post)
    db.commit()


def toggle_like(
    user: schemas.User, post_id: UUID, db: Session
) -> schemas.PostView:
    _post = db.query(Post).filter_by(id=post_id).first()

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if _post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    like = db.query(Like).filter_by(post_id=_post.id, user_id=user.id).first()
    if like:
        db.delete(like)
    else:
        db.add(Like(post_id=_post.id, user_id=user.id))
    db.commit()

    author = db.query(User).filter_by(id=_post.user_id).first()
    likes = db.query(Like).filter_by(post_id=_post.id).count()
    liked = (
        db.query(Like).filter_by(post_id=_post.id, user_id=user.id).first()
        is not None
    )

    return schemas.PostView(
        id=_post.id,
        content=_post.content,
        author=schemas.User.model_validate(author),
        likes=likes,
        liked=liked,
        time=_post.time,
    )
