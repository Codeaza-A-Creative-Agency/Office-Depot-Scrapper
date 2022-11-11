import re

import scrapy
from scrapy.crawler import CrawlerProcess


class benier_scraper(scrapy.Spider):
    
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
    start_urls=['https://dental.bienair.com/en/products']
    
    def parse(self, response):
        categories= response.css('a.category-elem-content ::attr(href)').extract()
        
        for link in categories:
            yield scrapy.Request(link, callback=self.parse_category)
    def parse_category(self,response):
        products= response.css('div.category-products>a ::attr(href)').extract()
        
        for link in products:
            yield scrapy.Request(link, callback=self.passer_func)
    def passer_func(self,response):
        category =response.css('li.categories0 ::text').extract()
        category = ''.join(str(string) for string in category)
        name = response.css('#w-node-992dc2e73583-7626c44d ::text').extract_first()
        name2 = response.css('span.product-name ::text').extract_first()
        catelog= response.css('a.nav-link-catalogue ::text').extract()
        if category==None and name2==None and name==None:
            yield scrapy.Request(response.url, callback=self.parse_product1,  dont_filter=True)
        elif category !=None and name2 !=None:
            yield scrapy.Request(response.url, callback=self.parse_product2, dont_filter=True)
        elif catelog !=None:
            yield scrapy.Request(response.url, callback=self.parse_product, dont_filter=True)
        else:
            yield scrapy.Request(response.url, callback=self.parse_product3, dont_filter=True)
        

    def parse_product(self,response):
        anch = response.css("div.div-block-34 div.tabs-menu>a").extract()
                  
        data_dict= {}
        for i in range(1,5):
            descrip =response.xpath(f"//div[@data-w-tab='Tab {i}']//text()").extract()
            descrip = ''.join(descrip).strip()
            data_dict["Seller Platform"]= "Bienair"
            data_dict["Seller SKU"]= response.xpath("//div[@class='text-block-11-cop']/text()").extract()
            data_dict["Manufacture"]= "Bienair"
            data_dict['Manufacture Code']=response.xpath("//div[@class='text-block-11-cop']/text()").extract()
            data_dict['Product Title']= response.xpath(f"//a[@data-w-tab='Tab {i}']/div/text()").extract()[1].strip()
            data_dict['Description']= descrip
            data_dict['Category']= response.url.split('/')[5]
            data_dict['Subcategories']=''
            data_dict['Qty']=''
            data_dict['Packaging']=''
            data_dict['Product Page URL']=response.url
            data_dict['Attachments']= ''
            data_dict['Image URL']= response.css("div.div-block-cool-touch>img' ::attr(srcset)").extract()
            
        yield data_dict
        
        print("1st function", response.url)
    def parse_product2(self,response):
        descrip =response.css('div.product-desc ::text').extract()
        descrip = ''.join(descrip).strip()
        descrip2 =response.css("div.product-technical ::text").extract()
        descrip2 = ''.join(descrip2).strip()
        descrip = descrip + descrip2
        sku =response.xpath("(//p[@class='ref'])[1]/text()").extract()
        sku =''.join(sku).strip()
        cat = response.css('li.categories0 ::text').extract_first()
        cat= ''.join(cat).strip()
        data_dict = {}
        data_dict['Seller Platform']= 'Bienair'
        data_dict['Seller SKU']= sku
        data_dict['Manufacture']= 'Bienair'
        data_dict['Manufacture Code']= sku
        data_dict["Product Title"]= response.css('span.product-name ::text').extract_first().strip()
        data_dict['Description']= descrip
        data_dict['Category']= response.url.split('/')[5]
        data_dict['Subcategories']=''
        data_dict['Qty']=''
        data_dict['Packaging']=''
        data_dict['Product Page URL']=response.url
        data_dict['Attachments']= response.css('a.product-download-elem ::attr(href)').extract_first()
        data_dict['Image URL']= response.xpath("//a[@class='image']//img/@src").extract()
        yield data_dict    
    def parse_product3(self,response):
        data_dict= {}
        data_dict['Seller Platform']= 'Bienair'
        data_dict['Seller SKU ']= response.css("#w-node-846222816ea4-7626c44d ::text").extract_first().strip()
        data_dict['Manufacture']= "Bienair"
        data_dict['Manufacture Code']=response.css("#w-node-846222816ea4-7626c44d ::text").extract_first().strip()
        data_dict['Product Title'] = response.css('#w-node-992dc2e73583-7626c44d ::text').extract_first().strip()
        data_dict['Description'] = response.css("div#technical_data ::text").extract()
        data_dict['Category'] = response.url.split('/')[5]
        data_dict['Subcategories']=''
        data_dict['Qty']=''
        data_dict['Packaging']=''
        data_dict['Product Page URL'] = response.url
        data_dict['Attachments']=''
        data_dict['Image URL']=''
        
        
        yield data_dict
        
      
 
    
    


process = CrawlerProcess()
process.crawl(benier_scraper)
process.start()