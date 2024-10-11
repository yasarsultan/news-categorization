from celery import Celery

app = Celery('news_feed', 
             broker='redis://localhost:6379/0')

app.conf.result_backend = 'redis://localhost:6379/0'