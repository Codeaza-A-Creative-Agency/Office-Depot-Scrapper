import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
import requests
import html2text
class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'dcdental-complete-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls=['https://www.dcdental.com/search']
    
    def parse(self,response):
        baseurl='https://www.dcdental.com'
        links = response.xpath("//div[@class='facets-item-cell-list-left']//a[@class='facets-item-cell-list-anchor']/@href").extract()
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_products)
            
        next_page= response.xpath("//li[@class='global-views-pagination-next']/a/@href").extract_first()
        print("Next",next_page)
        if next_page is not None:
            yield response.follow(baseurl+next_page, callback=self.parse)
    def parse_products(self,response):
        url = f'https://www.dcdental.com/api/items?c=1075085&country=US&currency=USD&custitem_pri_hideonweb=F&fieldset=details&include=facets&language=en&n=3&pricelevel=10&url={response.url.split("/")[-1]}'
        data=requests.get(url).json()
        subcat= data['facets'][2]['values'][0]['label']
        data=data['items'][0]['storedetaileddescription']
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        descrip= converter.handle(data)   
        title=response.xpath("//h1[@itemprop='name']/text()").extract_first()
        try:
            pkg= re.search(r'(\d+)\/(\D+)',title).group(2)
            # pkg= pkg.split(' ')[0]
            qty=re.search(r"(\d+)\/(\D+)",title).group(1)
            # qty=  qty.split(' ')[1]
        except:
            pkg=''
            qty=''
        yield{
            "Seller Platform":"DC Dental",
            "Seller SKU":response.xpath("//span[@itemprop='sku']/text()").extract_first(),
            "Manufacture Name":response.xpath("//div[@class='product-details-main-content-manufacturer desktop']/text()").extract_first(),
            "Manufacture Code":response.xpath("//span[@itemprop='sku']/text()").extract_first(),
            "Product Title":response.xpath("//h1[@itemprop='name']/text()").extract_first(),
            "Description":descrip,
                #response.css('div.product-details-information-tab-content-container ::text').extract_first(),
            "Category": response.xpath("(//a[@class='header-menu-level1-anchor']/text())[2]").extract_first(),
            "Subcategories":subcat,
            "Packaging":pkg,
            "Qty":qty,
            "Product Page URL":response.url,
            "Image URL":response.css('img.center-block ::attr(src)').extract()
            
        }
    
        
      
 
    
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()