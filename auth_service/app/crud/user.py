from sqlmodel import Session, select
from app.models.user import Users
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.exec(select(Users).where(Users.id == user_id)).first()


def get_user_by_email(db: Session, email: str):
    return db.exec(select(Users).where(Users.email == email)).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = Users(
        name=user.name,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_picture(db: Session, user_id: int, file_path: str):
    user = db.exec(select(Users).where(Users.id == user_id)).first()
    user.picture = file_path
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_info(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
):
    user = db.exec(select(Users).where(Users.id == user_id)).first()
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        password = update_data.pop("password")
        user.password = get_password_hash(password)

    # Actualizar el resto de campos
    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
