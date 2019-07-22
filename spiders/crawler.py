# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.shell import inspect_response

class DronesSpider(scrapy.Spider):
    name = 'spider'
    
    allowed_domains = ['kamera-express.be']
    start_urls = ['https://www.kamera-express.be/producten/video/camera-drone/drone/#?page=1&size=48']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url = url, endpoint = "render.html", callback = self.parse, args = {'wait':'3'})
 
    def parse(self, response):
        second_page = 'https://www.kamera-express.be/producten/video/camera-drone/drone/#?page=2&size=48'
        links_list = [link.get() for link in response.xpath("//a/@ng-href")]
        for prod in links_list:
            product_link = 'https://www.kamera-express.be/' + prod 
            yield SplashRequest(url = product_link, callback = self.extract_data, endpoint = "render.html", args = {"wait":"3"})
        yield SplashRequest(url = second_page, callback = self.parse, endpoint = "render.html", args = {"wait":"3"})
       
        # inspect_response(response, self)

    def extract_data(self, response):
        specs = {}
        property_name = [prop_name.xpath("th/text()").get() for prop_name in response.xpath("//tr")]    
        property_value = []

        for prop_value in response.xpath("//tr"):
            if prop_value.xpath("td/span/text()").get() is not None:
                property_value.append(prop_value.xpath("td/span/text()").get().strip())
            else:
                property_value.append(prop_value.xpath("td/span/text()").get())    

        for index, name in enumerate(property_name):
            specs[name]=property_value[index]

        yield {
            "name": response.xpath("//h1/strong/text()").get(),
            "price": response.xpath("//span[@class='h2']/strong/text()").get(),
            "image": response.xpath("//img[@class='product-image']/@src").get(),
            "specifications": specs
        }
        
        
        
        