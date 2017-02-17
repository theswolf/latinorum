# coding=utf-8
import scrapy


class VersioniSpider(scrapy.Spider):
    name = "versioni"


    uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),

            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),

            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),

            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),

            #ord('\xf2'.decode('utf-8')): ord("o"),

    }

    trans_table = {ord(c): None for c in u'\r\n\t'}
    
    def old_start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        url = "http://www.skuola.net/versioni-latino/"
        #yield scrapy.Request(url=url, meta={'suca':"suca"},callback=self.parse) 
        yield scrapy.Request(url=url,callback=self.parseindex)
 
    def parse(self, response):
        test = response.xpath('//dl')
        author = response.xpath('//dl/dt/div/h3/a/text()')
        author_def=response.xpath('//dl/dt/div/h3/a/@title')
        page = response.url.split("/")[-2]
        print(test.extract_first())
        print(author.extract())
        print(author_def.extract_first())
        filename = 'quotes-%s.html' % page 
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parseindex(self, response):
        infoBlock = response.css('dl.list_box')
        for p in infoBlock:
            '''for aut in p.css('h3 a::text').extract():
                autore = aut.decode('utf-8').translate(self.uni2ascii).encode('ascii')
                #print autore
            for d in p.css('h3 a::attr(title)').extract():
                desc = d.translate(self.uni2ascii)'''
            
            yield {
                'autore':p.css('h3 a::text').extract_first(),
                'desc':''.join(s.translate(self.trans_table) for s in p.css('h3 a::attr(title)').extract_first()),
                'link':p.css('h3 a::attr(href)').extract_first(),
                'data-type':'autore'
                #'versioni':(scrapy.Request(response.urljoin(p.css('h3 a::attr(href)').extract_first()), callback=self.parseauthorpage))
            }
        for p in infoBlock:
            autore = p.css('h3 a::text').extract_first(),
            link = p.css('h3 a::attr(href)').extract_first()
            url = response.urljoin(link)
            yield scrapy.Request(url = url, meta={'autore':autore}, callback=self.parseauthorpage)
            


    def parseauthorpage(self, response):
        versBlock = response.css('dl.list_box')
        for p in versBlock: 
            yield {
                'autore': response.meta['autore'],
                'titolo':p.css('h3 a::text').extract_first(),
                'desc':''.join(s.translate(self.trans_table) for s in p.css('h3 a::attr(title)').extract_first()),
                'link':p.css('h3 a::attr(href)').extract_first(),
                'data-type':'versione'
            }
        for p in versBlock: 
            titolo= p.css('h3 a::text').extract_first()
            autore= response.meta['autore']
            link= p.css('h3 a::attr(href)').extract_first()
            url = response.urljoin(link)
            yield  scrapy.Request(url = url, meta={'autore':autore,'titolo':titolo}, callback=self.parseversionecapitoli)

    def parseversionecapitoli(self, response):
        versBlock = response.css('div.list_box')
        for p in versBlock: 
            yield {
                'autore': response.meta['autore'],
                'titolo': response.meta['titolo'],
                'capitolo':p.css('h3 a::text').extract_first(),
                'intro':''.join(s.translate(self.trans_table) for s in p.css('h3 a::attr(title)').extract_first()),
                'link':p.css('h3 a::attr(href)').extract_first(),
                'data-type':'dettaglio'
            }
        for p in versBlock: 
            titolo= response.meta['titolo']
            autore= response.meta['autore']
            capitolo=p.css('h3 a::text').extract_first()
            link= p.css('h3 a::attr(href)').extract_first()
            url = response.urljoin(link)
            yield  scrapy.Request(url = url, meta={'autore':autore,'titolo':titolo,'capitolo':capitolo}, callback=self.parseversionetraduzione)

    def parseversionetraduzione(self, response):
        versBlock = response.css('div[id=versione]')
        #print response.xpath('//div[@class="testo"]/text()').extract_first()
        #print response.css('div.testo::text').extract()#versione > div.testo > br:nth-child(2)
        '''testoTran = ""
        for testo in response.css('div.traduzione p:nth-child(n+2)::text').extract():
            testoTran =  testo.encode('utf-8')#response.css('div.traduzione p:nth-child(n+2)::text').extract()#versione > div.testo > br:nth-child(2)
        print testoTran'''
        for orig in response.css('div.testo::text').extract():
            originale = orig.encode('utf-8')
        for tr in response.css('div.traduzione p:nth-child(n+2)::text').extract():
            trad = tr.encode('utf-8')
        yield {
            'titolo': response.meta['titolo'],
            'autore': response.meta['autore'],
            'capitolo':response.meta['capitolo'],
            'originale':''.join(s.strip().translate(self.trans_table) for s in response.css('div.testo::text').extract()),
            'traduzione':''.join(s.strip().translate(self.trans_table) for s in response.css('div.traduzione p:nth-child(n+2)::text').extract()),
            'data-type':'traduzione'
        }
            
        