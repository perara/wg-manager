from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(sess, username: str, password: str):
    user = get_user_by_name(sess, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_by_name(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username_and_password(db: Session, username: str, password: str) -> models.User:
    return db.query(models.User).filter((models.User.username == username) & (models.User.password == password)).first()


def create_user(sess: Session, user: models.User):
    user.password = get_password_hash(user.password)
    sess.add(user)
    sess.commit()

    return user.id is not None
