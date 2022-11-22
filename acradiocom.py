import scrapy 
from scrapy.crawler import CrawlerProcess


class acradiocom_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'acradiocom.com-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls= ['https://acradiocom.com/products/']
    
    def parse(self,response):
        links = response.css("li.ty-subcategories__item>a::attr(href)").extract()
        

        for link in links:

            yield scrapy.Request(url=link, callback=self.parse_p_links)
    def parse_p_links(self,response):
        
        links  =response.css("div.cm-gallery-item>a ::attr(href)").extract()
        if len(links)<1:
            links =response.css("div.ty-grid-list__image>a::attr(href)").extract()
        

        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_products)
            
            
        next_page= response.css("a.ty-pagination__item::attr(href)").extract()
        
        if next_page is not None:
            for next in next_page:
                yield response.follow(url=next, callback=self.parse_p_links)
    def parse_products(self,response):
        
        desc =response.css("div#content_description>div>p::text").extract()
        desc= ''.join(desc)
        desc1= response.css("dl.featureBox>dd::text").extract()
        desc1= ''.join(desc1)
        desc1= desc1.strip().replace("\r",'')
        desc1= desc1.strip().replace("\t",'')
        desc1= desc1.strip().replace("\n",'')
        desc2 =response.xpath("//div[@class='accordion-content']/ul//text()").extract()
        desc2 = ''.join(desc2)
        desc3 = response.css("div#content_description>div ::text").extract()
        desc3 = ''.join(desc3)
        desc= desc+ desc1 +desc2 +desc3
        att_url =response.xpath("//p[contains(text(),'For detailed warranty ')]/a/@href").extract()
        att_url = ['https://acradiocom.com'+url for url in att_url]
        sku = response.css("span.ty-control-group__item::text").extract_first().strip()
        if sku == "In stock":
            sku =response.css("h1.ty-product-block-title>bdi::text").extract_first()
        elif sku == 'On backorder':
            sku =response.css("h1.ty-product-block-title>bdi::text").extract_first()
        else:
            sku= sku
        data_dict={}
        
        data_dict['Seller Platform']= 'AC Radio'
        data_dict['Seller SKU']= sku
        data_dict['Manufacture']= 'AC Radio'
        data_dict['Manufacture Code']= sku
        data_dict['Product Title']= response.css("h1.ty-product-block-title>bdi::text").extract_first()
        data_dict['Description']= desc
        data_dict['Packaging']=''
        data_dict['Qty']=response.css("input.ty-value-changer__input::attr(value)").extract_first()
        data_dict['Category']= response.xpath("(//a[@class='ty-breadcrumbs__a']/text())[3]").extract_first()
        data_dict['Subcategories']=''
        data_dict['Product Page URL']= response.url
        data_dict['Attachements']= att_url
        data_dict['Image URL']=response.css("img.ty-pict::attr(src)").extract()
        yield data_dict
        
        
        
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(acradiocom_scraper)
process.start()