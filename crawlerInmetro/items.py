# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WorkshopItem(scrapy.Item):
    num_reg = scrapy.Field()
    nome = scrapy.Field()
    situacao = scrapy.Field()
    site = scrapy.Field()
    reg_inicio = scrapy.Field()
    reg_fim = scrapy.Field()
    email = scrapy.Field()
    endereco = scrapy.Field()
    uf = scrapy.Field()
    cidade = scrapy.Field()
    bairro = scrapy.Field()
    cep = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()
    resp_oper = scrapy.Field()
    google_id = scrapy.Field()
    lat = scrapy.Field()
    lnt = scrapy.Field()
    link_google = scrapy.Field()
    rating = scrapy.Field()
    #data_atualizacao = scrapy.Field()

# class CrawlerinmetroItem(scrapy.Item):
#     #define the fields for your item here like:
#     #name = scrapy.Field() 
#     pass
