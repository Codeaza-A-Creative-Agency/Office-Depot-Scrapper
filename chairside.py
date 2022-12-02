import scrapy 
from scrapy.crawler import CrawlerProcess
import re,json

class chairside_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'Chairside-solutions.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls=['https://www.chairsidesolutions.com/shop']
    
    def parse(self,response):
        links =response.css(".grid-item-link::attr(href)").extract()
        baseurl= 'https://www.chairsidesolutions.com'
        
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_products)
    def parse_products(self,response):
        sc =response.css("script[data-name='static-context']::text").extract_first()
        new = re.sub("Static = window.Static || {}; Static.SQUARESPACE_CONTEXT =",'',sc)
        new = re.sub("||",'',new)
        new = re.sub("\||",'',new)
        new= re.sub(';','',new)
        new= re.sub(" ",'',new)
        data= json.loads(new)
        data= data['product']['variants']
        desc =response.css(".ProductItem-details-excerpt ::text").extract()
        desc = ''.join(desc)
        desc= desc.strip()
        data_dict={}
        
        for i in data:
    
            data_dict['Seller Platform']= "Chairside Solutions"
            data_dict['Seller SKU']= i['sku']
            data_dict['Manufacture Name']= 'Chairside Solutions'
            data_dict['Manufacture Code']= ''
            data_dict['Product Title']= response.css("h1.ProductItem-details-title::text").extract_first().strip()
            data_dict['Description']= desc
            data_dict['Packaging']=''
            data_dict['Quantity']= response.xpath("//input[@aria-label='Quantity']/@value").extract_first()
            data_dict['Category']=''
            data_dict['Sub Category']=''
            data_dict['Product URL']=response.url
            data_dict['Attachements']=''
            data_dict['Image URL']=response.css("img.ProductItem-gallery-slides-item-image::attr(data-src)").extract()
            yield data_dict
    
        # check = response.css("select[aria-label='Select Options']>option:first-child::text").extract_first()
        # if check == "Select Options":
        #     print("under check")
            
        #     for i in response.css("select[aria-label='Select Options']>option"):
        #         data_dict['Seller Platform']= "Chairside Solutions"
        #         data_dict['Seller SKU']= response.css("h1.ProductItem-details-title::text").extract_first().strip()
        #         data_dict['Manufacture Name']= 'Chairside Solutions'
        #         data_dict['Manufacture Code']= ''
        #         data_dict['Product Title']= i.css("::text").extract_first().strip()
        #         data_dict['Description']= desc
        #         data_dict['Packaging']=''
        #         data_dict['Quantity']= response.xpath("//input[@aria-label='Quantity']/@value").extract_first()
        #         data_dict['Category']=''
        #         data_dict['Sub Category']=''
        #         data_dict['Product URL']=response.url
        #         data_dict['Attachements']=''
        #         data_dict['Image URL']=response.css("img.ProductItem-gallery-slides-item-image::attr(data-src)").extract()
        #         yield data_dict
        # else:
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(chairside_scraper)
process.start()