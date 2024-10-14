import re
from feedparser import parse
from datetime import datetime
from classify import classify_and_store


def clean_content(content):
    if content:
        return re.sub(r'<[^>]*>', '', content)
    return "No content available."


def to_datetime(parsed_time):
    if parsed_time:
        return datetime(*parsed_time[:6])
    return None


def parse_feed(feed_url, table_class, db_session):
    feed = parse(feed_url)
    
    for entry in feed.entries:
        # Check if article already present in our database
        existing_article = db_session.query(table_class).filter_by(link=entry.link).first()
        if existing_article:
            continue

        article = table_class(
            title=entry.get('title', None),
            content= clean_content(entry.get('summary', None)),
            publication_date = to_datetime(entry.get('published_parsed', None)),
            link = entry.get('link')
        )

        db_session.add(article)
        db_session.commit()
        classify_and_store.delay(article.link)

    print(f"Finished parsing {feed_url}")



# For example:
# session = Session()
# parse_feed("http://rss.cnn.com/rss/cnn_topstories.rss", Article, session)
# session.close()