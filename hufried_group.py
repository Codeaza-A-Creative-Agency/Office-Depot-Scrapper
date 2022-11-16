import scrapy 
from scrapy.crawler import CrawlerProcess


class H_Group_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        # 'FEED_URI' : 'Hufried-group-sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls = ['https://www.accutron-inc.com/product/']
    
    def parse(self, response):
        links =response.css("a.product-list-item ::attr(href)").extract()
        
        
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_p_links)
    def parse_p_links(self, response):
        links = response.css("span.field-content>a ::attr(href)").extract()
        
        
        
        for link in links:
            link= response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_products)
        
        next_page =response.css('a.pager__link ::attr(href)').extract()
        
        for next in next_page:
            url= response.urljoin(next)
            yield response.follow(url=url, callback=self.parse_p_links)
    def parse_products(self,response):
        data_dict ={}
        desc =response.css("div#prod-overview ::text").extract()
        desc= ''.join(desc)
        desc2 = response.css("div.short-description ::text").extract()
        desc2 = ''.join(desc2)
        desc = desc.strip() + desc2.strip()
        vars = response.xpath("//tr[@class='variation-item']")
        if len(vars)> 0:
            for var in vars:
                link= var.css("::attr(onclick)").extract()[0].split("= '")[1].replace("';",'')
                link = response.urljoin(link)
                yield scrapy.Request(url=link, callback=self.parse_variations)

        else:
            data_dict['Seller Platform']= 'Hufried Group'
            data_dict['Seller SKU']= response.css('sku.prod-details__sku ::text').extract_first()
            data_dict['Manufacture']='Hufried Group'
            data_dict['Manufacture Code']=response.css('sku.prod-details__sku ::text').extract_first()
            data_dict['Product Title']= response.css("span.page__title ::text").extract_first()
            data_dict['Description']=desc
            data_dict['Packaging']=''
            data_dict['Qty']= ''
            data_dict['Category']=response.url.split("/")[3]
            data_dict['Subcategories']=''
            data_dict['Product Page URL']=response.url
            data_dict["Attachement"]= response.xpath("//a[contains(text(),'DOWNLOAD')]//@href").extract()
            data_dict['Image URL']= response.css("li.easyzoom,easyzoom--overlay>a>img").css('::attr(src)').extract()
            
            yield data_dict
    def parse_variations(self,response):
        print("***********variation********----->",response.url)
        data_dict= {}
        desc =response.css("div#prod-overview ::text").extract()
        desc= ''.join(desc)
        desc2 = response.css("div.short-description ::text").extract()
        desc2 = ''.join(desc2)
        desc = desc.strip() + desc2.strip()
        data_dict['Seller Platform']= 'Hufried Group'
        data_dict['Seller SKU']= response.css('sku.prod-details__sku ::text').extract_first()
        data_dict['Manufacture']='Hufried Group'
        data_dict['Manufacture Code']=response.css('sku.prod-details__sku ::text').extract_first()
        data_dict['Product Title']= response.css("span.page__title ::text").extract_first()
        data_dict['Description']=desc
        data_dict['Packaging']=''
        data_dict['Qty']= ''
        data_dict['Category']=response.url.split("/")[3]
        data_dict['Subcategories']=''
        data_dict['Product Page URL']=response.url
        data_dict["Attachement"]= response.xpath("//a[contains(text(),'DOWNLOAD')]//@href").extract()
        data_dict['Image URL']= response.css("li.easyzoom,easyzoom--overlay>a>img").css('::attr(src)').extract()
        yield data_dict
        
   
        

    


process = CrawlerProcess()
process.crawl(H_Group_scraper)
process.start()