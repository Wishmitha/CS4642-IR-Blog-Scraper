import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "blogs"

    def start_requests(self):
        base_url = 'https://www.yamu.lk/blog/all?lang=en&page='
        urls = [];

        for i in range(1,40):
            urls.append(base_url+str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for url in response.css('a.front-group-item'):
            inner_url = url.css('a::attr(href)').extract_first()+'#full';
            yield scrapy.Request(url=inner_url, callback=self.parse_blog)

    def parse_blog(self, response):

        title = response.css('h1::text').extract_first()
        abstract = response.css('div.text-muted::text').extract_first()
        author = response.css('div.text::text').extract_first().split(" ")[-1]
        date_published = response.css('span.author-datetime::attr(title)').extract_first().split(" ")[-1]

        content= "";

        body = response.css('div.bodycopy')[0]
        for paragraph in body.css('p::text').extract():
            content = content + paragraph.strip() + '\n'
            content = content.replace('\u00A0', " ")

        blog_entry = {
            'title' : title,
            'abstract' : abstract,
            'author' : author,
            'date_published' : date_published,
            'content' : content,
            'url' : response.url
        }

        file_name = 'blog_corpus/' + title + '.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(blog_entry, indent=2))