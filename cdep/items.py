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

class ParlamentarItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    circumscriptie = scrapy.Field()
    data_validarii = scrapy.Field()
    formatiune_politica = scrapy.Field()
    grup_parlamentar = scrapy.Field()
    comisii_permanente = scrapy.Field()
    comisii_permanente_comune = scrapy.Field()
    comisii_speciale = scrapy.Field()
    comisii_speciale_comune = scrapy.Field()
    comisii_de_ancheta = scrapy.Field()
    comisii_de_ancheta_comune = scrapy.Field()
    alte_comisii = scrapy.Field()
    delegatii = scrapy.Field()
    grupuri_de_prietenie = scrapy.Field()
    grupuri_de_lucru_comune = scrapy.Field()
    # luari_de_cuvant = scrapy.Field()
    # declaratii_politice = scrapy.Field()
    # propuneri_legislative = scrapy.Field()
    # proiecte_de_hotarare = scrapy.Field()
    # intrebari_interpelari = scrapy.Field()
    # motiuni = scrapy.Field()
    birou = scrapy.Field()