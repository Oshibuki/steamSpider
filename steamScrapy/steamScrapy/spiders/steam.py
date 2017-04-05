import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import SteamscrapyItem


class steamSpider(scrapy.Spider):
    name = "steam"
    startUrl = 'http://store.steampowered.com/search/?specials=1'
    baseUrl = 'http://store.steampowered.com/search/?specials=1&page='

    def start_requests(self):
        yield Request(self.startUrl, callback=self.parse)

    def parse(self, response):
        Max_page_Num = int(BeautifulSoup(response.text, 'html.parser'). \
                           find_all('a', onclick="SearchLinkClick( this ); return false;")[-2].text)
        for i in xrange(Max_page_Num):
            url = self.baseUrl + str(i)
            yield Request(url, callback=self.parse_game)

    def parse_game(self, response):
        game_list = BeautifulSoup(response.text, 'html.parser').find_all('a', class_='search_result_row')
        item = SteamscrapyItem()
        for game in game_list:
            item['name'] = game.find_all('span', attrs={'class': "title"})[0].text
            item['original_price'] = game.find_all('strike')[0].text.strip()
            item['current_price'] = game.find_all('div', attrs={'class': "discounted"})[0]. \
                text.replace(item['original_price'], '').strip()
            item['discount'] = game.find_all('div', attrs={'class': "search_discount"})[0].text.strip()
            item['releaseday'] = game.find_all('div', attrs={'class': "search_released"})[0].text
            try:
                item['score'] = game.find('span', attrs={'class': "search_review_summary"}) \
                    ['data-store-tooltip'].replace('<br>', '_').split('_')[0]
            except:
                item['score'] = 'unknown'
            try:
                item['review'] = game.find('span', attrs={'class': "search_review_summary"}) \
                    ['data-store-tooltip'].replace('<br>', '_').split('_')[1]
            except:
                item['review'] = 'unknown'
            item['link'] = game['href']

            yield item
