import scrapy 
from scrapy.crawler import CrawlerProcess
import re

class a_dec_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'A-dec-sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://www.a-dec.com/']
    
    def parse(self,response):
        links = response.css(".mega-menu_title>a::attr(href)").extract()
        
        
        
        for link in links:
            yield scrapy.Request(url="https://a-dec.com"+link, callback=self.parse_p_link)
    def parse_p_link(self, response):
        links =  response.css(".mini-feature-box>a::attr(href)").getall()
        
        for link in links:
            yield scrapy.Request(url="https://www.a-dec.com"+link, callback=self.parse_product)
    def parse_product(self, response):
        desc =response.css(".one-column-sublayout div ::text").getall()
        desc = ''.join(desc)
        desc2 =response.css(".fifty-fifty-image-right__copy>p ::text").getall()
        desc2 = ''.join(desc2)
        specs = response.css("table.specs ::text").getall()
        specs = ''.join(specs)
        desc = desc + desc2 + specs
        desc = re.sub(r"\s+"," ",desc)
        att_urls =response.css(".internal-links-downloads ul li>a::attr(href)").getall()
        att_url = ["https://a-dec.com"+att_url for att_url in att_urls]
        data_dict ={}
        data_dict['Seller Platform'] = 'A-dec'
        data_dict['Seller SKU'] = response.url.split('/')[-1]
        data_dict['Manufacture Name']='A-dec'
        data_dict['Manufacture Code']=response.url.split('/')[-1]
        data_dict['Product Title']=response.css(".positioning-statement-box-two-column>div>h1::text").get()
        data_dict['Description']=desc
        data_dict['Packaging']=''
        data_dict['Qty']= ''
        data_dict['Category']=response.url.split("/")[3]
        data_dict['Subcategory']=''
        data_dict['Product Page URL']= response.url
        data_dict['Attachment URL']=att_url
        data_dict['Image URL']="https://www.a-dec.com"+response.css(".hero-image>img::attr(src)").get()
        yield data_dict
   
    
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(a_dec_scraper)
process.start()