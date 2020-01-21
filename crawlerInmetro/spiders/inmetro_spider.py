import scrapy
from crawlerInmetro.items import WorkshopItem

class InmetroSpider(scrapy.Spider):
    name = "inmetro"    

    def start_requests(self):
       
        urls = ['http://www.inmetro.gov.br/inovacao/oficinas/lista_oficinas.asp?end=&descr_ordem=&ind_situacao=&descr_titulo=&descr_estado=&descr_cidade=&descr_bairro=&pagina=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
#Faz o parse do dados da tabela principal e entra nos detalhes
    def parse(self, response):
        absolute_url = "http://www.inmetro.gov.br/inovacao/oficinas/"
        
        for row in response.xpath('/html/body/table[3]/tr/td[2]/table[3]//tr[position()>2]'):                      
            #Entra no link de detalhes e busca as informacoes            
            yield scrapy.Request(absolute_url+row.xpath('td[1]/a/@href').get(), callback=self.parse_detailWorkshop)

	    next_page = response.xpath('/html/body/table[3]/tr/td[2]/table[4]/tr/td[5]/b/a/@href').get();

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    #Faz o parse dos dados do detalhe
    def parse_detailWorkshop(self, response):       

        self.item = WorkshopItem()
        self.item['num_reg'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[1]/td[2]/b/text()').extract_first()
        self.item['nome'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[2]/td[2]/b//text()').extract_first()
        self.item['situacao'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[3]/td[2]//text()').extract_first()
        self.item['site'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[4]/td[2]/b/a/text()').extract_first()
        self.item['reg_inicio'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[5]/td[2]//text()').extract_first()
        self.item['reg_fim'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[6]/td[2]//text()').extract_first()
        self.item['email'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[7]/td[2]/a//text()').extract_first()
        self.item['endereco'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[8]/td[2]//text()').extract_first()
        self.item['uf'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[9]/td[2]//text()').extract_first()
        self.item['cidade'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[10]/td[2]//text()').extract_first()
        self.item['bairro'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[11]/td[2]//text()').extract_first()
        self.item['cep'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[12]/td[2]/text()').extract_first()
        self.item['tel'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[13]/td[2]/text()').extract_first()
        self.item['fax'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[14]/td[2]/text()').extract_first()
        self.item['resp_oper'] = response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[15]/td[2]/text()').extract_first()
        self.item['google_id'] = None
        self.item['lat'] = None
        self.item['lnt'] = None
        self.item['link_google'] = None
        self.item['rating'] = None

        yield self.item