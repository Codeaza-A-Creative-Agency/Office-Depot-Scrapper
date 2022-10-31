import scrapy
import json
import re
import requests
import pandas as pd
df= pd.read_csv(r'C:\scrapy\officedepot\project\project\spiders\officedepot.csv')
df= df['Links'].tolist()
df =df[6445:]

class ScrapSpider(scrapy.Spider):
    name = 'scrap'
  
    def findImages(self,scriptData : str) -> list:
        """
        This function is written for finding image urls from the script text
        """
        temp = scriptData[scriptData.find('"images":["'):]
        data = json.loads("{" + temp[:temp.find('"],"')] + '"]}')
        return [ 'https://media.officedepot.com/images' + url for url in data['images']]
    def findQuantity(self,scriptData : str) -> str:
        """
        This function is written for finding product quantity from the script text
        """
        temp = scriptData[scriptData.find('"name":"quantity"'):]
        data = json.loads("{" + temp[:temp.find('}')] + "}")
        return data.get('value')
    def start_requests(self):
        
        for link in df:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        print(response.url)
        sc1 =response.xpath("//div[@id='SkuPage']/script/text()").extract_first()
        data= json.loads(sc1)
        sku = data['sku']
        req= requests.get(f'https://api.bazaarvoice.com/data/products.json?passkey=caob5V3OJhI8lZDGWAWVDrPTHzXvME8y9qobBOFBZnfhQ&locale=en_US&allowMissing=true&apiVersion=5.4&filter=id:{sku}')
        resp = req.json()
        desc = resp['Results'][0]['Description']
        mfg_name= resp['Results'][0]['Attributes']['VendorName']['Values'][0]['Value']
        mpn =resp['Results'][0]['ManufacturerPartNumbers'][0]
        name =data['name']
        sc2 =response.xpath('//script[@id="globalSettings"]/text()').extract_first()
        resp2= json.loads(sc2)
        category =resp2['MasterTmsUdo']['department']
        subcategory =resp2['MasterTmsUdo']['category']
        # mpn = data['mpn']
        sc = response.xpath("//script[contains(text(), 'window.SKUPAGE_INITIAL_STATE')]/text()").extract_first()
        data = re.search('({.*\}\})\;', sc).group(1)
        images = self.findImages(data)
        qty = self.findQuantity(data)
        
        yield{
            "Seller Platform": 'Office Depot',
            "Seller SKu":sku,
            "Manufacture Name":mfg_name,
            "Manufacture Code":mpn,
            "Product Title":name,
            "Description":desc,
            "Packaging":'',
            "Qty ":qty,
            "Categories":category,
            "Subcategories":subcategory,
            "Product URL":response.url,
            "Image URL":images,   
        }
        
        
        
    

