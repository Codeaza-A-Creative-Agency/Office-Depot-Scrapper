import scrapy 
from scrapy.crawler import CrawlerProcess
import re
from bs4 import BeautifulSoup
class beutlich_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'OBEY_ROBOTS' : False,
        'FEED_URI' : 'Beutlich-sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://beutlich.com/products/']
    def parse(self, response):
        links =response.xpath("//article[contains(@class, 'portfolio-item count')]/a/@href").extract()
        
        
        for link in links:
            yield scrapy.Request(link.replace("/stock",'/product'), callback=self.parse_product)
    def parse_product(self, response):
        desc = response.css("div#tab-description ::text").extract()
        desc = ''.join(desc)
        desc =  re.sub(r"\s+"," ",desc)
        try:
            img =response.css("img.wp-post-image::attr(srcset)").extract()
            if len(img)<1:
                img =response.css("img.wp-post-image::attr(src)").extract()
        except:
            img =response.css("img.wp-post-image::attr(src)").extract()
        data_dict = {}
        data_dict['Seller Platform']= 'Beutlich'
        data_dict['Seller SKU']= response.css("div.entry>div:nth-child(3)::attr(id)").extract_first().split("-")[1]
        data_dict['Manufacture Name']='Beutlich'
        data_dict['Manufacture Code']=response.css("div.entry>div:nth-child(3)::attr(id)").extract_first().split("-")[1]
        data_dict['Product Title']=response.css("h1.product_title::text").extract_first()
        data_dict['Description']=desc
        data_dict['Packaging']=''
        data_dict['Qty']=''
        data_dict['Category']=response.css("span.posted_in a:nth-child(2)::text").extract_first()
        data_dict['Subcategory']=response.css("span.posted_in a:nth-child(1)::text").extract_first()
        data_dict['Product Page URL']= response.url
        data_dict['Attachement']=''
        data_dict['Image URL']=img
        yield data_dict

    


process = CrawlerProcess()
process.crawl(beutlich_scraper)
process.start()