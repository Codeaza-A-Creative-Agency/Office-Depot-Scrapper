import scrapy 
from scrapy.crawler import CrawlerProcess


class Boi_Horizon_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'BoiHorizon-sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls = ['https://usstore.biohorizons.com/']
    
    def parse(self, response):
        links =response.css("ul.navbar-nav>li>a::attr(href)").extract()[1:]
        baseurl ='https://usstore.biohorizons.com/'
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_category)
    def parse_category(self, response):
        links =response.css("h3.title>a::attr(href)").extract()
        
        
        baseurl ='https://usstore.biohorizons.com/'

        
        for link in links:
            yield response.follow(url=baseurl+link, callback=self.parse_subcat)
    def parse_subcat(self,response):
        links = response.css("h3.product-title>a::attr(href)").extract()
        baseurl ='https://usstore.biohorizons.com'
        check =response.xpath("(//div[@class='input-group-addon']/text())[2]").extract()
        if len(links)<1:
            links = response.css("h3.title>a::attr(href)").extract()
        if len(check)<1:
            for link in links:
                yield response.follow(url=baseurl+link, callback=self.parse_subcat, dont_filter=True)
        else:   
            for link in links:
                yield scrapy.Request(url=baseurl+link, callback=self.parse_p_links)
    def parse_p_links(self,response):
        links = response.css("h3.product-title>a::attr(href)").extract()
        baseurl ='https://usstore.biohorizons.com'  
        next_page =response.css("li.next-page>a::attr(href)").extract_first()
        for link in links:
            yield scrapy.Request(url= baseurl+link, callback=self.parse_product)
        if next_page is not None:
            yield response.follow(baseurl+next_page, callback=self.parse_p_links)
            
            
    
    def parse_product(self,response):
        clean = lambda dirty: dirty.replace('\r', '').replace('\n', '').replace('\t', '').replace("  ",'').strip()
        desc = response.xpath("//div[@itemprop='description']//text()").extract()
        desc2 = response.css("div.product-specs-box ::text").extract()
        if len(desc2)<1:
            desc2 = ''
        
        try:
            cats = response.xpath("//span/a/span[@itemprop='title']/text()").extract()[1]
            subcat = response.xpath("//span/a/span[@itemprop='title']/text()").extract()[2]
        except:
            cats= ''
            subcat=''
        desc = ''.join(desc)
        desc2 = ''.join(desc2)
        desc2 = clean(desc2)
        desc = desc + desc2
        desc = clean(desc)
        data_dict= {}
        data_dict['Seller Platform']= 'BoiHorizon'
        data_dict['Seller SKu']= response.xpath("//span[@itemprop='sku']/text()").extract_first().strip()
        data_dict['Manufacture']= 'BoiHorizon'
        data_dict['Manufacture Code']= response.css("div.gtin>span::text").extract_first()
        data_dict['Product Title']=  response.xpath("//h1[@itemprop='name notranslate']/text()").extract_first().strip()
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
process.crawl(Boi_Horizon_scraper)
process.start()