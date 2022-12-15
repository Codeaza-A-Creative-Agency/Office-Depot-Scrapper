import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import json
df = pd.read_csv("Staples_product_urls.csv")
df = df['Links'].tolist()

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'staples_data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    
    def start_requests(self):
        for link in df:
            yield scrapy.Request(url=link , callback=self.parse)
    def parse(self, response):
        sc = response.css('script#__NEXT_DATA__::text').get()
        data= json.loads(sc)
        specs=[]
        data= data['props']['initialStateOrStore']['skuState']['skuData']['items'][0]['product']
        try:
            qty = data['uom'].split('/')[0]
            pkg= data['uom'].split('/')[1]
        except:
            qty=data['uom']
            pkg=''
        desc_para = data['description']['paragraph'][0]
        desc_bullets=data['description']['bullets']
        desc_bullets = ''.join(desc_bullets)
        try:
            desc_headline=data['description']['headliner'][0]
        except:
            desc_headline =''
        desc_specs= data['description']['specification']
        for spec in desc_specs:
            specs.append( spec['name']+ spec['value'])
        specs = ' '.join(specs)
        desc = desc_para + desc_bullets + desc_headline + specs
        data_dict ={}
        data_dict['Seller Platform']= 'Staples'
        data_dict['Seller SKU']= data['partNumber']
        data_dict['Manufacture Name']=data['seoData']['anchorText']
        data_dict['Manufacture Code']=data['manufacturerPartNumber']
        data_dict['Product Title']= data['name']
        data_dict['Description']=desc
        data_dict['Packaging']=pkg
        data_dict['Qty']= qty
        data_dict['Category']=data['hierarchy']['category']['name']
        data_dict['Subcategory']= data['hierarchy']['class']['name']
        data_dict['Product Page URL']= response.url
        data_dict['Attachement URL']= ''
        data_dict['Image URL']= data['images']['enlarged']
        yield data_dict
      
 
    
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()