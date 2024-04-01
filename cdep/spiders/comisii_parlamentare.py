import scrapy
from cdep.items import *

class ComisiiParlamentareSpider(scrapy.Spider):
    name = "comisii-parlamentare"
    start_urls = ["https://cdep.ro/pls/parlam/structura2015.co"]
    
    def parse(self, response):
        tables = response.css(".grupuri-parlamentare-list table")
        type_lookup = {
            0: "permanente",
            1: "speciale",
            2: "ancheta",
            3: "alte"
        }

        for i, table in enumerate(tables):
            for row in table.css("tr"):
                name = row.css("td *::text").extract()[2]
                url = row.css("td a").attrib["href"]
                args = dict(name=name, type=type_lookup[i])
                yield response.follow(url, callback=self.parse_individual, cb_kwargs=args)
    
    def parse_individual(self, response, name, type):
        domenii_de_activitate = (response.xpath("//div[contains(@class, 'boxInfo')]/h3[contains(text(), 'Domenii de activitate')]/following::span/div/text()").get() or "").split(";")

        nr_tel_span = response.xpath("//div[contains(@class, 'boxInfo')]/span[starts-with(., 'Tel:')]/text()").get()
        nr_tel = []
        if nr_tel_span is not None:
            nr_tel = nr_tel_span[4:].split(",")
        
        fax_span = response.xpath("//div[contains(@class, 'boxInfo')]/span[starts-with(., 'Fax:')]/text()").get()
        fax = []
        if fax_span is not None:
            fax = fax_span[4:].split(",")
        
        email = response.xpath("//div[contains(@class, 'boxInfo')]/span[starts-with(., 'Email:')]/a/text()").get() or None

        membri_table = response.xpath("//h1[contains(text(), \"Comisia\")]/following::table[1]")
        fosti_membri_table = response.xpath("//h1[contains(text(), \"Fosti membri ai comisiei\")]/following::table")
        fosti_membri_ai_biroului_table = response.xpath("//h1[contains(text(), \"Fosti membri ai biroului comisiei\")]/following::table")

        membri = list(filter(None, map(self.row_to_deputat, membri_table.css("tr"))))
        fosti_membri = list(filter(None, map(self.row_to_fost_membru, fosti_membri_table.css("tr"))))
        fosti_membri_ai_biroului = list(filter(None, map(self.row_to_fosti_membri_ai_biroului, fosti_membri_ai_biroului_table.css("tr"))))

        yield ComisieParlamentaraItem(
            name=name,
            type=type,
            domenii_de_activitate=domenii_de_activitate,
            nr_tel=nr_tel,
            fax=fax,
            email=email,
            numar_membri=len(membri),
            membri=membri or [],
            fosti_membri=fosti_membri or [],
            fosti_membri_ai_biroului=fosti_membri_ai_biroului or []
        )
    
    def row_to_deputat(self, row):
        columns = row.xpath(".//td//text()").getall()
        
        if len(columns) == 10:
            [_, function, _, name, _, _, _, party, joined, _] = columns
        elif len(columns) == 9:
            [_, function, _, name, _, _, party, _, joined] = columns
        elif len(columns) == 0:
            return None

        return {
            "function": function,
            "name": name,
            "party_name": party,
            "joined": joined
        }
    
    def row_to_fost_membru(self, row):
        columns = row.xpath(".//td//text()").getall()

        if len(columns) == 9:
            [_, function, name, _, _, party, _, joined, left] = columns
        elif len(columns) == 8:
            [_, _, name, _, _, party, _, left] = columns
            function = None
            joined = None
        elif len(columns) == 0:
            return None

        return {
            "function": function,
            "name": name,
            "party_name": party,
            "joined": joined,
            "left": left
        }
    
    def row_to_fosti_membri_ai_biroului(self, row):
        columns = row.xpath(".//td//text()").getall()

        if len(columns) == 10:
            [_, function, _, name, _, _, party, _, joined, left] = columns
        elif len(columns) == 9:
            [_, function, name, _, _, party, _, joined, left] = columns
        elif len(columns) == 8:
            [_, _, name, _, _, party, joined, left] = columns
            function = None
        elif len(columns) == 0:
            return None
        
        return {
            "function": function,
            "name": name,
            "party_name": party,
            "joined": joined,
            "left": left
        }