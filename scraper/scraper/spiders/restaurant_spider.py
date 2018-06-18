import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        base_url = 'https://www.yamu.lk/place/restaurants?page='
        urls = [];

        for i in range(1,45):
            urls.append(base_url+str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for url in response.css('a.front-group-item'):
            inner_url = url.css('a::attr(href)').extract_first()+'#full';
            yield scrapy.Request(url=inner_url, callback=self.parse_restaurant)

    def parse_restaurant(self, response):

        name = response.css('h2::text').extract_first()
        address = response.css('p.addressLine::text').extract_first().strip()
        telephone = response.css('a.emph::attr(href)').extract_first().split(":")[-1]
        close_time = response.css('p.open::text').extract_first()
        description = response.css('p.excerpt::text').extract_first()
        tip = response.css('div.panel-body::text').extract_first()

        review = "";

        body = response.css('div.bodycopy')[0]
        for paragraph in body.css('p::text').extract():
            review = review + paragraph.strip() + '\n'
            review = review.replace('\u00A0', " ")

        resaurant_entry = {
            'name' : name,
            'address' : address,
            'telephone' : telephone,
            'close_time' : close_time,
            'description' : description,
            'tip' : tip,
            'review' : review,
            'url' : response.url
        }

        file_name = 'corpus/' + name + '.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(resaurant_entry, indent=2))