# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from db_model import Article, Session
from celery_config import app


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt_tab')

category1 = {'terrorism', 'protest', 'riot', 'unrest'}
category2 = {'positive', 'uplifting', 'inspiring'}
category3 = {'disaster', 'earthquake', 'flood', 'hurricane'}

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

session = Session()


def preprocess_text(text):
    print("Preprocessing")
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)


def categorize_article(title, content):
    preprocessed_text = preprocess_text(title + ' ' + content)
    
    print("Categorizing")
    # Simple rule-based categorization
    if any(word in preprocessed_text for word in category1):
        return 'Terrorism/Protest/PoliticalUnrest/Riot'
    elif any(word in preprocessed_text for word in category2):
        return 'Positive/Uplifting'
    elif any(word in preprocessed_text for word in category3):
        return 'Natural Disasters'
    else:
        return 'Others'


@app.task
def classify_and_store(article_id):
    article = session.query(Article).filter_by(article_id)
    if not article:
        return
    
    result = categorize_article(article.title, article.content)
    article.category = result
    session.commit()    



# Example usage:
# category = categorize_article("Peaceful Protest in City Center", "Hundreds gathered for a peaceful demonstration...")
# print(category)