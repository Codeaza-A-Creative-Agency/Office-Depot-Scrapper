import scrapy 
from scrapy.crawler import CrawlerProcess
import json,re

class Adin_dental_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        'ROBOTSTXT_OBEY ': 'False',
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        # 'FEED_URI' : 'testing.csv'
        'authority': 'www.adin-implants.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,so;q=0.7,hi;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
#     DEFAULT_REQUEST_HEADERS =  {
    # 'authority': 'www.adin-implants.com',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-language': 'en-US,en;q=0.9,ur;q=0.8,so;q=0.7,hi;q=0.6',
    # 'cache-control': 'max-age=0',
#     # Requests sorts cookies= alphabetically
#     # 'cookie': 'PHPSESSID=bc1qre8jdw2azrg6tf49wmp652w00xltddxmpk98xp; _gcl_au=1.1.1631358157.1668750410; wp-wpml_current_language=en; _ga=GA1.2.981953632.1668750411; _fbp=fb.1.1668750410977.1092109783; hubspotutk=db54292e2daa565bc5664828231240f2; __hssrc=1; messagesUtk=aa43ccbc5e614d8cb02588c9c368a765; _gid=GA1.2.674907458.1669091529; __hstc=20903655.db54292e2daa565bc5664828231240f2.1668750413296.1668750413296.1669091537347.2; __hssc=20903655.5.1669091537347',
    # 'dnt': '1',
    # 'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'none',
    # 'sec-fetch-user': '?1',
    # 'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
# }
     
    name= 'scraper'
    start_urls = ['https://www.adin-implants.com/']

    def parse(self, response):
        links = response.xpath("//li[@role='none']/a[@class='nav-link']/@href").extract()
        links = links[19:-1]
        baseurl = 'https://www.adin-implants.com'
        
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_json_page)
    def parse_json_page(self,response):
        sc = response.xpath("//script[contains(text(),'window.tyco__JS_smdi =')]").extract_first()
        sc2 = re.sub("window.tyco__JS_smdi =",'',sc)
        data= json.loads(sc2)
        url =data['cache_endpoint']
        
        yield scrapy.Request(url=url, callback=self.p_links)
    def p_links(self,response):
        data= response.json()
        links =[]
        length = len(data['products'])
        baseurl = 'https://www.adin-implants.com'
        for i in range(0,length):
            links.append(baseurl+data['products'][i]['permalink'])
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product)
    def parse_product(self,response):
        print("Response URL: ",response.url)
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(Adin_dental_scraper)
process.start()