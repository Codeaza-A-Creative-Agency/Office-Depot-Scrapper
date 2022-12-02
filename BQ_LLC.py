import scrapy 
from scrapy.crawler import CrawlerProcess
import re
class BQ_LLC_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'BQ-LLLC-Sample-data.csv'
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #             "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls=['https://www.bqe-usa.com/products/']
    
    def parse(self, response):
        links =response.css("div.productimage>a::attr(href)").extract()
        
        
        basue_url = 'https://www.bqe-usa.com'
        
        for link in links:
            yield scrapy.Request(url=basue_url+link, callback=self.parse_products)
    def parse_products(self, response):
        desc =desc =response.css("div.contentdescription ::text").extract()
        desc = ''.join(desc)
        desc =re.sub(r'\s+', ' ', desc)
        desc= desc.replace(".gallery { float:left; width:150px; height:210px; padding:10px; padding-left:0px; *padding-top:0px; margin-bottom:30px; } .gallery_nav { margin-top:10px; width:130px; text-align:center; } .gallery_nav tr td { text-align:center; } .galleryimage { position:relative; width:150px; height:180px; } #front_div { position:absolute; width:150px; } #back_div { position:absolute; width:150px; } ",'')
        desc = desc.replace(" <!-- var gallery_2 = new ContentSlider('gallery_2', 'galleryimage2', 'front_div', 'back_div'); --> <!-- gallery_2.Add('image_72'); --> <!-- gallery_2.Add('image_73'); --> <!-- gallery_2.Add('image_74'); --> <!-- gallery_2.Add('image_76'); --> <!-- gallery_2.Add('image_77'); --> <!-- gallery_2.Render(); --> ",'')
        desc = desc.replace(" <!-- var gallery_3 = new ContentSlider('gallery_3', 'galleryimage3', 'front_div', 'back_div'); --> <!-- gallery_3.Add('image_37'); --> <!-- gallery_3.Add('image_38'); --> <!-- gallery_3.Add('image_39'); --> <!-- gallery_3.Render(); --> ",'')
        # desc = re.sub(r'.gallery { float:left; width:150px; height:210px; padding:10px; padding-left:0px; *padding-top:0px; margin-bottom:30px; } .gallery_nav { margin-top:10px; width:130px; text-align:center; } .gallery_nav tr td { text-align:center; } .galleryimage { position:relative; width:150px; height:180px; } #front_div { position:absolute; width:150px; } #back_div { position:absolute; width:150px; } ','',desc)
        print(desc)
        
       
        
        data_dict={}
        data_dict['Seller Platform']= 'BQ Ergonomics LLC'
        data_dict['Seller SKu']=response.css("div#breadcrumb>a.kruimelpad_last::text").extract_first()
        data_dict['Manufacture']= "BQ Ergonomics LLC"
        data_dict['Manufacture Code']= ''
        data_dict['Product Title']=  response.css("div#breadcrumb>a.kruimelpad_last::text").extract_first()
        data_dict['Description']=desc
        data_dict['Packaging']= ''
        data_dict['Qty']= ''
        data_dict['Category']=''
        data_dict['Subcategories']=''
        data_dict['Product Page URL']= response.url
        data_dict['Attachment']=''
        data_dict['Image URL']= ['https://www.bqe-usa.com'+url for url in response.css("img.content_image::attr(src)").extract()]
        yield data_dict
        
        
   
        
      
 
    
    


process = CrawlerProcess()
process.crawl(BQ_LLC_scraper)
process.start()