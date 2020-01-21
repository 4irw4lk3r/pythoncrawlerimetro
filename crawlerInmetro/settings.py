# -*- coding: utf-8 -*-

# Scrapy settings for crawlerInmetro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawlerInmetro'

SPIDER_MODULES = ['crawlerInmetro.spiders']
NEWSPIDER_MODULE = 'crawlerInmetro.spiders'

ITEM_PIPELINES = { 'crawlerInmetro.pipelines.CrawlerinmetroPipeline': 1000 }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlerInmetro (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#Db settings
CONNECTION_STRING = {
    'drivername':???,
    'username':???,
    'password':???,
    'host':???,
    'port':???,
    'database':???
}
