from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 


@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} NOT FOUND")
    
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"No Post with id: {id}")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="NOT authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, publiched = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"No Post with id: {id}")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="NOT authorized to perform requested action")    

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()