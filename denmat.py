import scrapy 
from scrapy.crawler import CrawlerProcess


class denmat_scraper(scrapy.Spider):
    
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
    start_urls = ['https://www.denmat.com/products.html?product_list_limit=all']
    
    def parse(self,response):
        links = response.css("a.product::attr(href)").extract()
        
        
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product)
    def parse_product(self,response):
        desc = response.css("div.description ::text").extract()
        clean = lambda dirty: dirty.replace('\r', '').replace('\n', '').replace('\t', '').replace("  ",'').replace("  ", '').strip()
        desc = clean(desc)
        
        data_dict={}
        data_dict['Seller Platform']= 'Den mat'
        data_dict['Seller SKu']= response.xpath("//span[@itemprop='sku']/text()").extract_first()
        data_dict['Manufacture']= 'Den mat'
        data_dict['Manufacture Code']= response.xpath("//span[@itemprop='sku']/text()").extract_first()
        data_dict['Product Title']=  response.xpath("//span[@itemprop='name']/text()").extract_first()
        data_dict['Description']=desc
        data_dict['Packaging']= ''
        data_dict['Qty']= ''
        data_dict['Category']=cats
        data_dict['Subcategories']=subcat
        data_dict['Product Page URL']= response.url
        data_dict['Attachment']=''
        data_dict['Image URL']= response.xpath("//img[@itemprop='image']/@src").extract_first()
        yield data_dict
        
       
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(denmat_scraper)
process.start()