# -*- coding: utf-8 -*-

from .local_settings import *

BOT_NAME = 'scrascrapy_iiiedupy_iiiedu'

SPIDER_MODULES = ['scrapy_iiiedu.spiders']
NEWSPIDER_MODULE = 'scrapy_iiiedu.spiders'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrapy_iiiedu.pipelines.iiieduJsonPipeline': 300,
    'scrapy_iiiedu.pipelines.iiieduMongoPipeline': 300,

}


