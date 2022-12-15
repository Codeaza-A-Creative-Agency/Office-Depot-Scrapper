import scrapy 
from scrapy.crawler import CrawlerProcess
import re
import json
class centrixdental_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'ROBOTSTXT_OBEY':False,
        'FEED_URI' : 'centrixdental-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        }
    def start_requests(self):
        url= 'https://www.centrixdental.com'
     
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
    def parse(self, response):
        links =response.css("li.item a::attr(href)").getall()
        
        
        for link in links:
            yield scrapy.Request(url=link, headers=self.headers, callback=self.parse_p_links)
    def parse_p_links(self,response):
        links = response.css('.product-item-link::attr(href)').getall()
        try:
            category =response.url.split('/')[-1].split('.')[0]
        except:
            category = response.url.split('/')[-1]
        for link in links:
            yield scrapy.Request(url=link, headers=self.headers, callback=self.parse_product, meta={"Category":category})
   
        
        next_page =response.css(".next::attr(href)").extract_first()
        
        if next_page is not None:
            yield response.follow(url=next_page, headers=self.headers, callback=self.parse_p_links)
    def parse_product(self,response):
        desc =response.css(".description>.value ::text").getall()
        desc = ''.join(desc)
        desc = desc.replace("\r\n",'')
        data_dict= {}
        t_vals=[]
        imgvals=[]
        check = response.xpath("//select/option/text()").get()
        if check =='Choose an Option...':
            sc2 =response.xpath("//script[contains(text(),'#product_addtocart_form')]//text()").get()
            data= json.loads(sc2)
            t_vals =list(data['#product_addtocart_form']['configurable']['spConfig']['attributes'].keys())[0]
            for img in data['#product_addtocart_form']['configurable']['spConfig']['images']:
                imgvals.append(img)  
            titles_dict = data['#product_addtocart_form']['configurable']['spConfig']['attributes'][t_vals]['options'][1:]
            for title,img in zip(titles_dict,imgvals):
                sku = title['label'].split("REF")[1]
                img1 = data['#product_addtocart_form']['configurable']['spConfig']['images'][img][0]['img']
                img2 = data['#product_addtocart_form']['configurable']['spConfig']['images'][img][0]['full']
                try:
                    result = re.search(r'(\d+)( ct\.|-Pack)', title['label'])
                    qty = result.group(1)
                    pkg= result.group(2)
                except:
                    qty=None
                    pkg=None
                img = [img1 +',' + img2]
                data_dict['Seller Platform']= 'Centrixdental'
                data_dict['Seller SKU']=sku
                data_dict['Manufacture Name']= 'Centrixdental'
                data_dict['Manufacture Code']=sku
                data_dict['Product Title']=response.css("span[itemprop='name']::text").get().strip()+"-"+ title['label'].strip()
                data_dict['Description']=desc
                data_dict['Packaging']=pkg
                data_dict['Qty']=qty
                data_dict['Category']=response.meta.get('Category')
                data_dict['Subcategory']=''
                data_dict['Product Page URL']= response.url
                data_dict['Attachment URL']=response.css("a[title='Download Product Literature']::attr(href)").get()
                data_dict['Image URL']=img
                yield data_dict
        else:
            sc=response.xpath("//script[contains(text(),'data-gallery-role=gallery-placeholde')]/text()").get()
            data= json.loads(sc)
            images =[]
            imgs =data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']['data']
            for img in imgs:
                images.append(img['img'])
            data_dict['Seller Platform']= 'Centrixdental'
            data_dict['Seller SKU']=response.css("div[itemprop='sku']::text").get()
            data_dict['Manufacture Name']= 'Centrixdental'
            data_dict['Manufacture Code']=response.css("div[itemprop='sku']::text").get()
            data_dict['Product Title']=response.css("span[itemprop='name']::text").get().strip()
            data_dict['Description']=desc
            data_dict['Packaging']=''
            data_dict['Qty']=response.css("input[name='qty']::attr(value)").get()
            data_dict['Category']=response.meta.get('Category')
            data_dict['Subcategory']=''
            data_dict['Product Page URL']= response.url
            data_dict['Attachment URL']=response.css("a[title='Download Product Literature']::attr(href)").get()
            data_dict['Image URL']=images
            yield data_dict
            
    


process = CrawlerProcess()
process.crawl(centrixdental_scraper)
process.start()