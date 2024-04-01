# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GrupParlamentarItem(scrapy.Item):
    abbreviation = scrapy.Field()
    party_name = scrapy.Field()
    members = scrapy.Field(serializer=int)
    email = scrapy.Field()
    nr_tel = scrapy.Field()
    fax = scrapy.Field()

class ComisieParlamentaraItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field() # "permanente", "speciale", "ancheta" or "alte"
    domenii_de_activitate = scrapy.Field()
    nr_tel = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    numar_membri = scrapy.Field(serializer=int)
    membri = scrapy.Field()
    fosti_membri = scrapy.Field()
    fosti_membri_ai_biroului = scrapy.Field()

class DeputatItem(scrapy.Item):
    name = scrapy.Field()
    circumscriptie
    data_validarii
    formatiune_politica
    grup_parlamentar
    comisii_permanente
    alte_comisii
    delegatii
    grupuri_de_prietenie
    luari_de_cuvant
    declaratii_politice
    propuneri_legislative
    proiecte_de_hotarare
    intrebari_interpelari
    motiuni
    birou