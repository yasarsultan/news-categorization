import os
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('POSTGRESQL_USER')
password = os.getenv('POSTGRESQL_PASSWORD')
host = os.getenv('POSTGRESQL_HOST')

engine = create_engine(f'postgresql://{username}:{password}@{host}/feedsdb',
                       connect_args={
                            "keepalives": 1,
                            "keepalives_idle": 30,
                            "keepalives_interval": 10,
                            "keepalives_count": 5,
                        })

Base = declarative_base()

class Article(Base):
    __tablename__ = 'rss_feeds'
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    publication_date = Column(DateTime)
    link = Column(String(255), primary_key=True)
    category = Column(Text)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)