import os
import re
from feedparser import parse
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('POSTGRESQL_USER')
password = os.getenv('POSTGRESQL_PASSWORD')
host = os.getenv('POSTGRESQL_HOST')

Base = declarative_base()

class Article(Base):
    __tablename__ = 'rss_feeds'

    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    publication_date = Column(DateTime)
    source_url = Column(String(255), primary_key=True)
    category = Column(Text)

engine = create_engine(f'postgresql://{username}:{password}@{host}/feedsdb')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def clean_content(content):
    if content:
        return re.sub(r'<[^>]*>', '', content)
    return "No content available."

def to_datetime(parsed_time):
    if parsed_time:
        return datetime(*parsed_time[:6])
    return None

def parse_feed(feed_url, db_session):
    feed = parse(feed_url)
    for entry in feed.entries:
        # Check if article already present in our database
        existing_article = db_session.query(Article).filter_by(source_url=entry.link).first()
        if existing_article:
            continue

        article = Article(
            title=entry.get('title', None),
            content= clean_content(entry.get('summary', None)),
            publication_date = to_datetime(entry.get('published_parsed', None)),
            source_url = entry.get('link')
        )
        db_session.add(article)
            
    
    db_session.commit()


# For example:
# session = Session()
# parse_feed("http://rss.cnn.com/rss/cnn_topstories.rss", session)
# session.close()