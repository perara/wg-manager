from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from starlette import status

import const
import db.user
import middleware
import models
import schemas

router = APIRouter()


@router.get("/logout")
def logout(user: schemas.User = Depends(middleware.auth)):
    return dict(message="ok")


@router.post("/user/edit", response_model=schemas.User)
def edit(form_data: schemas.UserInDB,
         user: schemas.UserInDB = Depends(middleware.auth),
         sess: Session = Depends(middleware.get_db)
         ):
    form_data.password = middleware.get_password_hash(form_data.password)
    form_data.sync(sess)
    return form_data


@router.post("/login", response_model=schemas.Token)
def login(*, username: str = Form(...), password: str = Form(...), sess: Session = Depends(middleware.get_db)):
    user: schemas.UserInDB = schemas.UserInDB(username=username, password="").from_db(sess)

    # Verify password
    if not user or not middleware.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token
    access_token_expires = timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = middleware.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user=schemas.User(**user.dict())
    )


@router.post("/users/create/")
def create_user(
        form_data: schemas.UserInDB,
        sess: Session = Depends(middleware.get_db),
        user: schemas.User = Depends(middleware.auth)
):
    user = db.user.get_user_by_name(sess, form_data.username)

    # User already exists
    if user:
        if not db.user.authenticate_user(sess, form_data.username, form_data.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

    else:

        # Create the user
        if not db.user.create_user(sess, models.User(
                username=form_data.username,
                password=form_data.password,
                full_name=form_data.full_name,
                email=form_data.email,
                role=form_data.role,
        )):
            raise HTTPException(status_code=400, detail="Could not create user")

