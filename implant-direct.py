from pydoc import describe
from urllib import request
import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import json
class implant_direct_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'sample-implant-direct-2.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls=['https://store.implantdirect.com/us/en/']
    
    def parse(self,response):
        links =response.css("li.parent>a ::attr(href)").extract()
        
        
        
        for link in links:
            if link != "#":
                yield scrapy.Request(url=link, callback=self.parse_p_links)
    def parse_p_links(self,response):
        p_links= response.css('a.product-item-link ::attr(href)').extract()
        
        
        next_page= response.css('a.next ::attr(href)').extract_first()
        
        for p_link in p_links:
            yield scrapy.Request(url=p_link, callback=self.parse_data)
        
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_p_links)
        
 
    def parse_data(self,response):
        sc =response.xpath("(//script[contains(text(),'breakpoints')]/text())[2]").extract_first()
        data= json.loads(sc)
        title= response.xpath("//span[@itemprop='name']/text()").extract_first()
        try:
            pkg= title.split('-')[1].split('/')[1]
            qty= title.split('-')[1].split('/')[0]
        except:
            pkg=''
            qty=''
        descrip1= response.xpath("//div[@itemprop='description']//text()").extract()
        descrip1= ''.join(str(stri) for stri in descrip1)
        descrip2 = response.xpath("//div[@class='product attribute description']//p//text()").extract() 
        descrip3=response.xpath("//div[@class='product attribute description']//div//text()").extract_first()
       
        descrip2= ''.join(str(stri) for stri in descrip2)
        descrip3= response.xpath("//div[@class='product attribute description']//ul//text()").extract()
        descrip3= ''.join(str(string) for string in descrip3)
        descrip4= response.xpath("//table[@class='data table additional-attributes']//text()").extract()
        descrip4= ''.join(str(stri)for stri in descrip3)
        descrip=descrip1 +descrip2+descrip3+descrip4
        try:
            subcat1= response.xpath("(//li[@class='level0 nav-1 category-item first level-top parent']/a)[2]/text()").extract_first()
            subcat2=response.xpath("(//li[@class='level0 nav-1 category-item first level-top parent']/a)[2]/text()").extract_first()
            subcat= subcat1 +">"+ subcat2
        except:
            subcat=''
        try:
            image1 =data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']['data'][0]['img']
            image2= data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']['data'][1]['img']
            images = ','.join(img for img in [image1, image2])
        except:
            images= response.xpath('//meta[@property="og:image"]/@content').extract()
            
        response.xpath("(//script[contains(text(),'twe_1_2.png')]/text())[2]")
        
        yield{
            "Seller Platform": "Implant Direct",
            "Seller SKU":response.xpath("//div[@itemprop='sku']/text()").extract_first(),
            "Manufacture Name":"Implant Direct",
            "Manufacture Code":response.xpath("//div[@itemprop='sku']/text()").extract_first(),
            "Product Title":title,
            "Description":descrip,
            "Packaging":pkg,
            "Qty":qty,
            "Categories":response.xpath("//li[@class='level0 nav-1 category-item first level-top parent']/a//text()").extract_first(),
            "Subcategories":subcat,
            "Product Page URL":response.url,
            "Attachment":'',
            "Image URL":images,
        }
       
         
        
      
 
    
    


process = CrawlerProcess()
process.crawl(implant_direct_scraper)
process.start()