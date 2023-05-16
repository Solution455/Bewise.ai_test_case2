import os
from uuid import uuid4

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql+psycopg2://{os.getenv("username")}:{os.getenv("password")}@db/test_case2')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """
    Model of User
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    access_token = Column(String, unique=True)


class AudioRecord(Base):
    """
    Model of Audio record
    """
    __tablename__ = "audio_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    audio_id = Column(String, unique=True)


Base.metadata.create_all(bind=engine)


def create_user(name: str) -> User:
    """
    Creating a user
    :param name:
    :return User:
    """
    session = SessionLocal()
    user = User(name=name, access_token=str(uuid4()))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(user_id: int) -> User:
    """
    Getting user by id
    :param user_id:
    :return User::
    """
    session = SessionLocal()
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_name(name: str) -> User:
    """
    Getting user by name
    :param name:
    :return User:
    """
    session = SessionLocal()
    return session.query(User).filter(User.name == name).first()


def check_user_credentials(user_id: int, access_token: str) -> bool:
    """
    Checking user credentials
    :param user_id:
    :param access_token:
    :return bool:
    """
    user = get_user_by_id(user_id)
    return user is not None and user.access_token == access_token


def save_audio(user_id: int, audio_id: str) -> AudioRecord:
    """
    Saving audio record
    :param user_id:
    :param audio_id:
    :return AudioRecord:
    """
    session = SessionLocal()
    audio_record = AudioRecord(user_id=user_id, audio_id=audio_id)
    session.add(audio_record)
    session.commit()
    session.refresh(audio_record)
    return audio_record


def check_audio_record_exists(id_: str, user: int) -> bool:
    """
    Checking audio record exists
    :param id_:
    :param user:
    :return bool::
    """
    session = SessionLocal()
    audio_record = session.query(AudioRecord).filter(AudioRecord.audio_id == id_, AudioRecord.user_id == user).first()
    return audio_record is not None
