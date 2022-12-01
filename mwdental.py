import scrapy 
from scrapy.crawler import CrawlerProcess
import re

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'Midwest-dentla-sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://www.mwdental.com/supplies.html','https://www.mwdental.com/equipment.html']
    
    def parse(self, response):
        links =response.css("li.extra>a::attr(href)").extract()
        
        
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_links)
    def parse_links(self, response):
        links = response.css('div.product-shop-info a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_item)
        
        
        next_page = response.css('a.next::attr(href)').extract_first()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_links)
    def parse_item(self, response):
        try:
            sku =response.css("td.product-main-table-info>dl.product-attributes>dd::text").extract_first()
            if sku is None:
                sku = response.css("h3.product-name::text").extract_first()
        except:
            pass
        try:
            mfg_code= response.css("td.product-main-table-info>dl.product-attributes dd:last-child::text").get()
        except:
            mfg_code= None
        
        img =response.css("ul#zoom_additionalimages>li a::attr(href)").get()

        img2 =response.css("ul#zoom_additionalimages>li img::attr(src)").get()
        if img2 is None:
            img2 = ''
    
        elif img is None:  
            img = ''
        else:
            pass
     
            
            img = [img +','+ img2]
        desc = response.css("div.short-description ::text").getall()
        desc = ''.join(desc)
        desc = re.sub(r"\s+"," ",desc)
        desc2 =response.css(".product-specs ::text").getall()
        desc2 = ''.join(desc2)
        desc2 = re.sub(r"\s+"," ",desc2)
        desc = desc + desc2
        if len(desc) == 0:
            desc=response.css("table.product-main-table ::text").getall()
            desc = ''.join(desc)
            desc = re.sub(r"\s+"," ",desc)
        try:
            qty =response.xpath("//input[@id='qty']@value").get()
            pkf =response.css("div.short-description>dl:last-child ::text").getall()[-4].split(' ')[1]
        except:
            qty =None
            pkg=None
        
        mfg= response.css("td.product-main-table-info>dl.product-attributes dd.main::text").get()
        if mfg is None:
            mfg =response.css(".product-main-table-info-mfg>strong ::text").get()
    
        data_dict={}
        
        data_dict['Seller Platform']= "MW Dental"
        data_dict['Seller SKU']= sku
        data_dict['Manufacture Name']= mfg
        data_dict['Manufacture Code']= mfg_code
        data_dict['Product Title']=response.css("h3.product-name::text").extract_first()
        data_dict['Description']= desc
        data_dict['Packaging']=pkg
        data_dict['Quantity']=qty
        data_dict['Category']= response.css('.breadcrumbs li:nth-child(3)>a::text').get()
        data_dict['Sub Category']=''
        data_dict['Product URL']=response.url
        data_dict['Attachements']=''
        data_dict['Image URL']=img
        yield data_dict
        
       
        
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()