import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
import json
df = pd.read_csv("Staples_product_urls.csv")
df = df['Links'].tolist()
class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'staples-sample-data-1.csv',
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #     "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    # start_urls = ['https://www.staples.com/Staples-Economy-Rubber-Bands-Size-64-1-4-lb/product_143297']
    
    def start_requests(self):
        for url in df:

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):

        sku= response.css("span#item_number::text").extract_first().split("#:")[1]
        mfg = response.css("span#manufacturer_number ::text").extract()[1].split("#:")[1]
        desc =response.css("div#detail_container ::text").extract()
        category =response.css("div.sc-izol8d-0 ::text").extract()[1]
        sku_id = response.url.split("_")[1]
        subcategory =response.css("div.sc-izol8d-0 ::text").extract()[2] + ">" + response.css("div.sc-izol8d-0 ::text").extract()[3]
        headers = {
            'authority': 'www.staples.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ur;q=0.8,so;q=0.7,hi;q=0.6',
            'content-type': 'application/json;charset=UTF-8',
            'dnt': '1',
            'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE5ODk3NTDNEpUTHQoQUJMHLrErGJyHg89uy71MyuHiZmM5ZDJjZmRmZmM4MzI1MSIsInRyIjoiYWIzZWQ0YzA0ZTk0YmY5YWI1MDIwOTc4OWE0OWVkNTAiLCJ0aSI6MTDNEpUTHQoQUJMHLrErGJyHg89uy71MyuHyIn19',
            'origin': 'https://www.staples.com',
            'referer': 'https://www.staples.com/Staples-Economy-Rubber-Bands-Size-64-1-4-lb/product_143297',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'traceparent': '00-ab3ed4c04e94bf9ab50209789a49ed50-fc9d2cfdffc83251-01',
            'tracestate': '1887982@nr=0-1-1989754-781924616-fc9d2cfdffc83251----1669696831579',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-http-encode': 'true',}
        json_data = {
        'configValues': {},
        'serviceContext': {
            'tenant': 'StaplesDotCom',
            'legacyTenant': '',
            'locale': 'en-US',
            'channelId': 'WEB',
            'siteId': 'US',
            'zipCode': '01701',
            'langId': '',
            'langCd': '',
            'storeId': '',
            'user': {
                'fingerprint': '',
                'emailHash': '',
                'directCustomerNumber': '',
                'requestId': '8609d88faf95a2898015b17962a5c411',
            },
            'cisResponse': {
                'MEMBERSHIP': {},
                'ORCHID': {},
                'SEGMENTCODE': '1_UNIDENTIFIED',
            },
            'customerTierCode': 'GUS',
        },
        'query': {
            'mboxes': 'SKU_PAGE_FBT_DOTCOM',
            'pageType': 'sku',
            # 'classId': 'CL163579',
            'inputs': {
                'brandTransformationSwitch': True,
                'isQvd': False,
                'sparq': True,
                'coreSkuNumber': sku_id,
                'includeSpecifications': True,
                'includeInkAndTonerDetails': True,
            },
        },
        'siteVariables': {
            'tenant': {
                'legacy': 10001,
                'fullName': 'StaplesDotCom',
                'shortName': 'sdc',
            },
            'channelId': 'WEB',
            'siteId': 'US',
            'catalogId': '10051',
            'langId': -1,
            'langCd': 'en',
            'locale': 'en_US',
            'hyphenatedLocale': 'en-US',
            'storeId': '10001',
            'currency': 'USD',
            'isCOM': True,
            'isCA': False,
            'isSBA': False,
            'assetStoreId': 5051,
            'env': 'azureprod',
            'isProd': True,
            'isLoggedIn': False,
            'ctx': {},
        },}
        json_data = json.dumps(json_data)

        
        
        yield scrapy.Request(url ='https://www.staples.com/ele-lpd/api/sparxProxy/atRecommendation', method='POST',body=json_data, headers=headers, callback=self.parse_product, meta={'mfg':mfg, "sku":sku,'desc':desc,'category':category,'subcategory':subcategory, 'url':response.url})
    def parse_product(self, response):
        data1 = response.json()
        data= data1[0]
        # print(data)
        desc = response.meta['desc']
        desc = ''.join(desc)
        specs = []
        for spec in data['description']['specification'][:-1]:
            specs.append(spec['name'] +":"+spec['value'])
        specs = ','.join(specs)
        desc = desc + specs
        units = data['units']
        try:
            pkg = units.split('/')[1]
            qty = units.split('/')[0]
        except:
            pkg=None
            qty=None
        data_dict={}
        
        data_dict['Seller Platform']= "Staples"
        data_dict['Seller SKU']= response.meta['sku']
        data_dict['Manufacture Name']= data['manufacturerName']
        data_dict['Manufacture Code']= response.meta['mfg']
        data_dict['Product Title']=data['title']
        data_dict['Description']= desc
        data_dict['Packaging']=pkg
        data_dict['Quantity']=qty
        data_dict['Category']=response.meta['category']
        data_dict['Sub Category']=response.meta['subcategory']
        data_dict['Product URL']=response.meta['url']
        data_dict['Attachements']=''
        data_dict['Image URL']=data['images']
        yield data_dict
        
        
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()