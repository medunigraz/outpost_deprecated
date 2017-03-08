import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medunigraz.settings")

BOT_NAME = 'medunigraz'

SPIDER_MODULES = [
    'dynamic_scraper.spiders',
    'medunigraz.scraper',
]

USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'medunigraz.scraper.pipelines.DjangoWriterPipeline': 800,
}
