import scrapy
from cdep.items import *

class GrupuriParlamentareSpider(scrapy.Spider):
    name = "grupuri-parlamentare"
    start_urls = ["https://cdep.ro/pls/parlam/structura2015.gp"]

    def parse(self, response):
        table = response.css(".grupuri-parlamentare-list table")
        rows = table.css("tr")
        for row in rows:
            columns = row.css("td *::text").extract()
            try:
                [_, abbr, name, n_members] = columns
            except:
                [abbr, name, n_members] = columns
            args = dict(abbr=abbr, party_name=name, members=int(n_members.split()[0]))
            url = row.xpath(".//a/@href").get()
            yield response.follow(url, callback=self.parse_individual, cb_kwargs=args)
    
    def parse_individual(self, response, abbr, party_name, members):
        email = response.xpath(".//span[contains(@class, 'mailInfo')]/a/text()").get()

        nr_tel_span = response.xpath("//div[contains(@class, 'boxInfo')]/span[starts-with(., 'Tel:') or starts-with(., 'Tel.:')]/text()").get()
        nr_tel = []
        if nr_tel_span is not None:
            nr_tel = nr_tel_span[5:].split(",")
        
        fax_span = response.xpath("//div[contains(@class, 'boxInfo')]/span[starts-with(., 'Fax:')]/text()").get()
        fax = []
        if fax_span is not None:
            fax = fax_span[4:].split(",")

        yield GrupParlamentarItem(
            abbreviation = abbr,
            party_name = party_name,
            members = members,
            email = email,
            nr_tel = nr_tel,
            fax = fax
        )
    
    def parse_deputat(self, response):
        ""