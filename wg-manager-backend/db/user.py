from typing import Optional

from sqlalchemy.orm import Session
from database import models

import schemas


def update_user(sess: Session, form_data: schemas.UserInDB):
    user = get_user_by_name(sess, form_data.username)
    user.password = form_data.password
    user.full_name = form_data.full_name
    user.email = form_data.email  # TODO this section should be updated

    sess.add(user)
    sess.commit()
    return get_user_by_name(sess, form_data.username)


def authenticate_user(sess, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_name(sess, username)
    if user and verify_password(password, user.password):
        return user
    return None


def get_user_by_name(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username_and_password(db: Session, username: str, password: str) -> models.User:
    return db.query(models.User).filter((models.User.username == username) & (models.User.password == password)).first()


def create_user(sess: Session, user: models.User):
    # Only hash password if set. Use case: LDAP users don't have passwords on database
    if user.password:
        user.password = get_password_hash(user.password)
    sess.add(user)
    sess.commit()

    return user.id is not None
