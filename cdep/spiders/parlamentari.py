from cdep.items import *
import scrapy
import re

# https://cdep.ro/pls/parlam/structura2015.de
# https://cdep.ro/pls/parlam/structura2015.ab?idl=1

class ParlamentariSpider(scrapy.Spider):
    name = "parlamentari"
    start_urls = ["https://cdep.ro/pls/parlam/structura2015.de"]

    def parse(self, response):
        tables = response.css(".grupuri-parlamentare-list table")
        deputati = tables[0]

        for row in deputati.css("tr"):
            columns = row.css("td")
            if len(columns) != 0:
                url = "https://cdep.ro" + columns[1].css("a").attrib["href"]
                yield response.follow(url, callback=self.parse_parlamentar)
    
    def parse_parlamentar(self, response):
        text = "".join(response.xpath(".//h3[contains(text(), 'DEPUTAT')]/following::p[1]//text()").getall())
        data_validarii = " ".join(re.search(r"data validarii: (\d+) (.*) (\d+)", text).groups())

        yield ParlamentarItem(
            name = response.css("div.boxTitle h1::text").get(),
            email = response.css(".mailInfo.innerText::text").get(),
            circumscriptie = response.xpath(".//h3[contains(text(), 'DEPUTAT')]/following::p[1]/a[1]/text()").get(),
            data_validarii = data_validarii,
            formatiune_politica = response.xpath(".//h3[contains(text(), 'Formatiunea politica')]/following::td[5]/text()").get(),
            grup_parlamentar = response.xpath(".//h3[contains(text(), 'Grupul parlamentar')]/following::a[1]/text()").get(),
            comisii_permanente = response.xpath(".//h3[text() = 'Comisii permanente']/following::p[1]/a/text()").getall() or [],
            comisii_permanente_comune = response.xpath(".//h3[text() = 'Comisii permanente comune']/following::p[1]/a/text()").getall() or [],
            comisii_speciale = response.xpath(".//h3[text() = 'Comisii speciale']/following::p[1]/a/text()").getall() or [],
            comisii_speciale_comune = response.xpath(".//h3[text() = 'Comisii speciale comune']/following::p[1]/a/text()").getall() or [],
            comisii_de_ancheta = response.xpath(".//h3[text() = 'Comisii de ancheta']/following::p[1]/a/text()").getall() or [],
            comisii_de_ancheta_comune = response.xpath(".//h3[text() = 'Comisii de ancheta comune']/following::p[1]/a/text()").getall() or [],
            alte_comisii = response.xpath(".//h3[text() = 'Alte comisii']/following::p[1]/a/text()").getall() or [],
            delegatii = response.xpath(".//h3[contains(text(), 'Delegatii')]/following::table[1]//a/text()").getall() or [],
            grupuri_de_prietenie = response.xpath(".//h3[contains(text(), 'Grupuri de prietenie')]/following::table[1]//a/text()").getall() or [],
            grupuri_de_lucru_comune = response.xpath(".//h3[text() = 'Grupuri parlamentare de lucru comune']/following::p[1]/a/text()").getall() or [],
            birou = response.xpath(".//h3[contains(text(), 'Biroul parlamentar')]/following::p[string-length(text()) > 0][1]/text()").get()
        )