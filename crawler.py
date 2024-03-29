import scrapy
from scrapy.crawler import CrawlerProcess

import time

from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush import CoveoConstants


class PokemonSpider(scrapy.Spider):
    name = "pokemon_spider"
    custom_settings = {"FEEDS":{"results.json":{"format":"json"}}}
    start_urls = ['https://pokemondb.net/pokedex/national']

    def parse(self, response):
        pokemon_pages = []

        SET_SELECTOR = '.infocard'
        for item in response.css(SET_SELECTOR):

            POKEMON_LINK = 'a ::attr(href)'
            POKEMON_PAGE = 'https://pokemondb.net' + item.css(POKEMON_LINK).extract_first()

            pokemon_pages.append(POKEMON_PAGE)

        for item in pokemon_pages:
            yield scrapy.Request(item, callback = self.parse_card)

    def parse_card(self, response):
      
        NAME_SELECTOR = '#main h1 ::text'
        IMAGE_SELECTOR = 'a[rel="lightbox"] ::attr(href)'
        TYPE_SELECTOR = '.tabset-basics .sv-tabs-panel.active .vitals-table td a.type-icon ::text'
        GENERATION = '#main .grid-row abbr ::text'

        yield {
            'url': response.url,
            'name': response.css(NAME_SELECTOR).extract_first(),
            'image': response.css(IMAGE_SELECTOR).extract_first(),
            'type': list(set(response.css(TYPE_SELECTOR).extract())),
            'generation': response.css(GENERATION).extract_first()
        }




if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PokemonSpider)

    sourceId = 'pokemonchallengepebfwi56-tymrhcjeplqwiacezf4rr2cice'
    orgId = 'pokemonchallengepebfwi56'
    apiKey = 'xx0ff4f49e-ddda-45af-a9c0-0e7d899e06db'

    push = CoveoPush.Push(sourceId, orgId, apiKey)

    user_email = "npushkarskii@coveo.com"
    my_permissions = CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.User, "", user_email)
    allowAnonymous = True

    def item_scraped(item, response, spider):
        print('=============> Item scraped:', item)

        mydoc = Document(item['url'])
        mydoc.Title = item['name']
        mydoc.AddMetadata("pokemonimage", item['image'])
        mydoc.AddMetadata("pokemontype", item['type'])
        mydoc.AddMetadata("pokemongeneration", item['generation'])
        

        mydoc.SetAllowedAndDeniedPermissions([my_permissions], [], allowAnonymous)

        push.AddSingleDocument(mydoc) 
        

    for crawler in process.crawlers:
        crawler.signals.connect(item_scraped, signal=scrapy.signals.item_scraped)



    process.start()


   

# sourceId = 'pokemonchallengepebfwi56-tymrhcjeplqwiacezf4rr2cice'
# orgId = 'pokemonchallengepebfwi56'
# apiKey = 'xx0ff4f49e-ddda-45af-a9c0-0e7d899e06db'

# push = CoveoPush.Push(sourceId, orgId, apiKey)
# mydoc = Document("https://pokemondb.net/pokedex/national")
# mydoc.Title = "THIS IS A TEST"
# mydoc.SetData("ALL OF THESE WORDS ARE SEARCHABLE")
# mydoc.FileExtension = ".html"
# mydoc.AddMetadata("connectortype", "CSV")

# user_email = "npushkarskii@coveo.com"
# my_permissions = CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.User, "", user_email)
# allowAnonymous = True
# mydoc.SetAllowedAndDeniedPermissions([my_permissions], [], allowAnonymous)

# push.AddSingleDocument(mydoc)