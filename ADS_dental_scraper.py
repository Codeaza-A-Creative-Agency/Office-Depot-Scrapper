import scrapy 
from scrapy.crawler import CrawlerProcess
import re
import json
class ADS_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'ADS-dental-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls= ['https://www.adsdental.com/']
    
    def parse(self,response):
        categories = response.xpath('//a[@class="header_down_item second_font"]/@href').extract()
        
        
        for link in categories:
            yield scrapy.Request(url=response.url+link, callback=self.parse_category)
    def parse_category(self, response):
        baseurl ='https://www.adsdental.com/'
        p_links = response.css('a.product_second_item_title ::attr(href)').extract()
        
        
        for link in p_links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_product)
    def parse_product(self, response):
        data_dict= {}
        baseurl ='https://www.adsdental.com/'
        src =response.xpath("//script[contains(text(),'price')]/text()").extract_first()
        data= json.loads(src)
        image = data['image']
        descrip2= data['description']
        try:
            image2= response.xpath("//div[@class='detail_img']/img/@src").extract_first()
        except:
            image2 =''
            
            
        if image2 !=None:
            image = baseurl+image +","+ baseurl+image2
        src2 =response.xpath("//script[contains(text(),'ListItem')]/text()").extract_first()
        data2= json.loads(src2)
        cat = data2['itemListElement'][2]['item']['name']
        
        descrip = response.css("div.detail_text_group ::text").extract()
        descrip= ''.join(descrip)
        clean = lambda dirty: dirty.replace("  ",'')
        descrip = str(descrip)
        descrip = clean(descrip)
        descrip2 =str(descrip2)
        descrip2 = clean(descrip2)
        descrip = descrip+descrip2
        sku = response.xpath("//tr[@class='firstRow']/td/text()").extract()
        sku= ''.join(sku)
        # sku = re.search(r"\d+",sku)
        data_dict["Seller Platform"]= "ADS Dental"
        data_dict["Seller SKU"]= sku
        data_dict["Manufacture Name"]= "ADS Dental"
        data_dict['Manufacture Code']=response.xpath("//tr[@class='firstRow']/td/text()").extract()
        data_dict['Product Title']= response.css('h1.inner_title ::text').extract_first()
        data_dict['Description']= descrip
        data_dict['Packaging']=''
        data_dict['Qty']=''
        data_dict['Category']= cat
        data_dict['Subcategory']=''
        data_dict['Product Page URL']=response.url
        data_dict['Attachment URL']= baseurl+response.xpath("(//div[@class='mp_bottom_up_item_href_group flex']/a/@href)[18]").extract_first()
        data_dict['Image URL']=  image
        yield data_dict
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(ADS_scraper)
process.start()