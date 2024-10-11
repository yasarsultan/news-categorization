from parser import parse_feed
from db_model import Article, Session

RSS_FEEDS = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed', 
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews', 
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]


def main():
    session = Session()
    
    for feed in RSS_FEEDS:
        parse_feed(feed, Article, session)

    session.close()


if __name__ == '__main__':
    main()