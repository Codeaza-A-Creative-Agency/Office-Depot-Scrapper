import scrapy 
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import re
class denmat_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'DenMat-Sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls = ['https://www.denmat.com/products.html?product_list_limit=all']
    
    def parse(self,response):
        links = response.css("a.product::attr(href)").extract()
        
        
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product)
    def parse_product(self,response):
        desc = response.css("div.description").extract()
        soup = BeautifulSoup(desc[0],'lxml')
        desc= soup.text.strip()
        title= response.xpath("//span[@itemprop='name']/text()").get().strip()
        try:
            result = re.search(r"(\d+)[\/|-](pk|pack|Pack)", title)
            # result = re.match(r'(\d+)[\/|-](pk|pack|Pack)|(\d+)(pc)',title)
            qty = result.group(1)
            pkg= result.group(2)
        except:
            pkg =''
            qty= ''
            
        
        data_dict={}
        data_dict['Seller Platform']= 'DenMat'
        data_dict['Seller SKU']= response.xpath("//div[@itemprop='sku']/text()").extract_first()
        data_dict['Manufacture Name']= 'DenMat'
        data_dict['Manufacture Code']= response.xpath("//div[@itemprop='sku']/text()").extract_first()
        data_dict['Product Title']= title,
        data_dict['Description']=desc
        data_dict['Packaging']= pkg
        data_dict['Qty']= qty,
        data_dict['Category']=''
        data_dict['Subcategory']=''
        data_dict['Product Page URL']= response.url
        data_dict['Attachment']=''
        data_dict['Image URL']= response.css(".gallery-placeholder__image::attr(src)").getall()
        yield data_dict
        
       
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(denmat_scraper)
process.start()