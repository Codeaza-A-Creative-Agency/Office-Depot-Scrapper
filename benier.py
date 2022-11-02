from tkinter import Y
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
            yield scrapy.Request(link, callback=self.parse_product)
    def parse_product(self,response):
        try:
            cat= response.xpath("//li[@class='item categories0']//a[@itemprop='item']//text()").extract_first()
        except:
            cat =cat= response.url.split('/')[5]
        try:
            att_url =response.css('a.product-download-elem ::attr(href)').extract()
        except:
            att_url=''
        images = response.xpath("//img[@class='image-turbines']/@srcset").extract()
        if len(images) <1:
            images= response.xpath("//div[@class='main-image-container-small show-for-small-only']//img//@src").extract()
        title=  response.xpath("//h1[@class='product-heading']//span//text()").extract()
        if len(title)<1:
            title =response.xpath("//div[@class='text-block-11-copy']//text()").extract_first()
        desc = response.xpath("//div[@class='tabs w-tabs']//text()").extract()
        desc =''.join(str(string) for string in desc)
        desc = desc.replace('\n','')
        if len(desc) <1:
            desc= response.xpath("//div[@class='product-desc']//text()").extract()
            desc2 =response.xpath("//p[@class='section-description']//text()").extract()
            desc2 =''.join(str(string) for string in desc2)
            desc=''.join(str(string).strip() for string in desc)
            desc = desc.replace('\n','')
            if len(desc2) <1:
                desc2= response.xpath("//table[@class='product-technical-table show-for-medium']//text()").extract()
                desc2 = ''.join(str(string) for string in desc2)
            references= response.css("div.reference-list ::text").extract()
            references= ''.join(str(string).strip() for string in references)
            references= references.replace('\n','')
            desc = desc + desc2+ references
        yield{
            "Seller Platform": "bienair dental",
            "Seller SKU":references,
            "Manufacture Name": "bienair dental",
            "Manufacture Code":references,
            "Product Title":title,
            "Description":desc,
            "Packaging":'',
            "Qty":'',
            "Category":cat,
            "Subcategories":'',
            "Product Page URL":response.url,
            "Attachment URL":att_url,
            "Image URL":images
        }
   
        //div[@class='tabs-content w-tab-content']//div[contains(text(),'Tab ')]
      
 
    
    


process = CrawlerProcess()
process.crawl(benier_scraper)
process.start()