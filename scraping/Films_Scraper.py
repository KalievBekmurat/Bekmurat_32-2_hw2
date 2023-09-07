# from parsel import Selector
# import requests
#
#
# class FilmsScraper:
#     START_URL = "https://kinogo.biz/filmy/"
#     LINK_XPATH = '//div[@class="shortstory"]/div/a/@href'
#     TEXT_XPATH = '//div[@class="description__block"]//text()'
#
#     def parse_data(self):
#         text = requests.get(self.START_URL).text
#         tree = Selector(text=text)
#         links = tree.xpath(self.LINK_XPATH).extract()
#         data = []
#         for link in links:
#             print(link)
#             data.append(link)
#         return data[:5]
#
#
#
#     def parse_detail(self, urls):
#         for url in urls:
#             text = requests.get(url).text
#             tree = Selector(text=text)
#             text = tree.xpath(self.TEXT_XPATH).extract()
#             print(''.join(text))
#
#
# if __name__ == "__main__":
#     scraper = FilmsScraper()
#     scraper.parse_data()