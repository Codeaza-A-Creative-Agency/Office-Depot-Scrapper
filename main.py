import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
df=pd.read_csv(r'C:\Users\admin\Dental-City-Product-URLs.csv')
links= df['Product URL'].tolist()

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'testing.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    def start_requests(self):
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse )
    def parse(self,response):
        sku=response.url.split('/')[4]
        url = f'https://www.dentalcity.com/Widgets-product/gethtml_skulist/{sku}/html_options3/false///'
        
        yield scrapy.Request(url=url, callback=self.parse_skuIDs, meta={"sku":sku})
      
    def parse_skuIDs(self,response):
        prods = response.xpath('//select[@id="skulist"]/option')
        
        for prod in prods:
            
            variant_id=prod.xpath('@id').extract()
           
            for v_id in variant_id:
                url=f'https://www.dentalcity.com/widgets-product/gethtml_filtered_apparelsku/{response.meta.get("sku")}/SkuId%24%{v_id}%24%24true%24%24v/900X380/html_consumer-electronics1sku/param5/param6'
                yield scrapy.Request(url=url, callback=self.parse_data, meta={"Variant ID":v_id, "SKU":response.meta.get("sku")})
    def parse_data(self,response):
        yield{
            "Constructed URL":response.url,
            "Variant ID":response.meta.get("Variant ID"),
            "SKU":response.meta.get("SKU"),
        }
         
        
      
 
    
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()