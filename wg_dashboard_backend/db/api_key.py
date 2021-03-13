from sqlalchemy.orm import Session

from database import models


def add_initial_api_key_for_admin(sess: Session, api_key, ADMIN_USERNAME):

    db_user = sess.query(models.User)\
        .filter_by(username=ADMIN_USERNAME)\
        .one()

    exists_api_key = sess.query(models.UserAPIKey)\
        .filter_by(
            user_id=db_user.id,
            key=api_key
        )\
        .count()

    if exists_api_key == 0:
        db_api_key = models.UserAPIKey()
        db_api_key.key = api_key
        db_api_key.user_id = db_user.id

        sess.add(db_api_key)
        sess.commit()

    return True
