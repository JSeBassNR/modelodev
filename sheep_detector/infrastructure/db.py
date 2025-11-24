import os
from sqlalchemy import create_engine, Column, Integer, Text, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func

DATABASE_URL = os.environ.get('POSTGRES_URL')

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    file_path = Column(Text, nullable=False)
    processed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    detections = relationship('Detection', back_populates='image')


class Detection(Base):
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'))
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    score = Column(Float)
    class_name = Column(Text)
    color = Column(Text)
    health_status = Column(Text)
    image = relationship('Image', back_populates='detections')


def init_engine(database_url: str = None):
    url = database_url or DATABASE_URL
    if not url:
        return None
    engine = create_engine(url, future=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    if engine is None:
        return None
    Session = sessionmaker(bind=engine)
    return Session()


def save_results(session, image_path: str, detections: list):
    if session is None:
        return None
    img = Image(file_path=image_path)
    session.add(img)
    session.flush()  # get img.id
    for d in detections:
        det = Detection(
            image_id=img.id,
            x1=d.get('x1'), y1=d.get('y1'), x2=d.get('x2'), y2=d.get('y2'),
            score=d.get('score'), class_name=d.get('class_name'), color=d.get('color'), health_status=d.get('health_status')
        )
        session.add(det)
    session.commit()
    return img.id
