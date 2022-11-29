import scrapy 
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class supply_clinic_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        # 'FEED_URI' : 'testing.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://www.supplyclinic.com/categories']
    
    def parse(self, response):
        links =response.css("div.cat>a::attr(href)").extract()
        baseurl = 'https://supplyclinic.com'
        
        
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_cat_id)
    def parse_cat_id(self,response):
        name = response.url.split("=")[1]
        
        
        
        yield scrapy.Request(url=f'https://www.supplyclinic.com/search/{name}?utf8=%E2%9C%93&sort_by_price=false&price_descending=false&as_list=false&per_page=40&search_term%5Bto_s%5D=*&sales=false', callback=self.parse_p_links)
    def parse_p_links(self,response):
        
        cat_id = response.xpath("//option[@selected='selected']/@value").extract_first()
        
        
        
        
        yield scrapy.Request(url =f'https://www.supplyclinic.com/search_page?utf8=%E2%9C%93&item%5Bname%5D=&sort_by_price=false&price_descending=false&as_list=false&per_page=4000&category%5Bcategory_id%5D={cat_id}&search_term%5Bto_s%5D=*&sales=false&manufacturer%5Bmanufacturer_id%5D=&brand%5Bbrand_id%5D=&vendor%5Bvendor_id%5D=&price%5Brange%5D=', callback=self.parse_p_links2)
        
        
    def parse_p_links2(self,response):
        
        links = response.css('a#result-item-link ::attr(href)').extract()
        baseurl = 'https://www.supplyclinic.com'
        
        
        for link in links:
            yield scrapy.Request(url=baseurl+link, callback=self.parse_product_page)
    def parse_product_page(self,response):
        desc = response.css("div.col-sm-8,col-md-5 ::text").extract_first()
        bs = BeautifulSoup(desc, 'html.parser')
        desc=bs.get_text()
        
        # qty = response.xpath('//*[@id="item-page"]/div[2]/div[2]/div[2]/div/table/tbody/tr[5]/td[2]/text()').extract_first().split("/")[0]
        # pkg = response.xpath('//*[@id="item-page"]/div[2]/div[2]/div[2]/div/table/tbody/tr[5]/td[2]/text()').extract_first().split("/")[1]
        try:
            try:
                qty =  response.css("table.details-table tr:nth-child(5) td:nth-child(2)::text").extract_first().split("/")[0]
                pkg=response.css("table.details-table tr:nth-child(5) td:nth-child(2)::text").extract_first().split("/")[1]
            except:
                qty =response.css("table.details-table tr:nth-child(4) td:nth-child(2)::text").extract_first().split("/")[0]
                pkg=response.css("table.details-table tr:nth-child(4) td:nth-child(2)::text").extract_first().split("/")[1]
                
        except:
            qty = None
            pkg = None
       
        data_dict={}
        data_dict['Seller Platform']= 'Supply Clinic'
        data_dict['Seller SKu']= response.css("div.manu-code::text").extract_first().split(":")[1].strip()
        data_dict['Manufacture']= response.css("table.details-table tr:nth-child(1) td:nth-child(2)>a::text").extract_first()
        data_dict['Manufacture Code']= response.css("table.details-table tr:nth-child(2) td:nth-child(2)::text").extract_first()
        data_dict['Product Title']=  response.css('h1.item-name::text').extract_first()
        data_dict['Description']=desc
        data_dict['Packaging']= pkg
        data_dict['Qty']= qty
        data_dict['Category']=response.css("div.breadcrumbs>a::text").extract_first()
        data_dict['Subcategories']=response.css("div.breadcrumbs>a::text").extract()[1:]
        data_dict['Product Page URL']= response.url
        data_dict['Attachment']=''
        data_dict['Image URL']= response.css("a.mfp-zoom::attr(href)").extract()
        yield data_dict
        
        
      
 
    
    


process = CrawlerProcess()
process.crawl(supply_clinic_scraper)
process.start()