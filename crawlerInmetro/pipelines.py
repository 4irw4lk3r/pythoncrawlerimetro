from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

from crawlerInmetro.models import Workshops, db_connect
from scrapy import signals

import datetime

class CrawlerinmetroPipeline(object):

    def __init__(self):
        self.workshops = [] 
        self.db_session = None       

        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        self.db_session = self.Session()

        workshop = Workshops()
        workshop.num_reg = self.clean_data(item['num_reg']) 
        workshop.nome = self.clean_data(item['nome']) 
        workshop.site = self.clean_data(item['site']) 
        workshop.reg_inicio = datetime.datetime.strptime(item['reg_inicio'].replace(u'\xa0',u'').strip(), "%d/%m/%Y").date()
        workshop.reg_fim = datetime.datetime.strptime(item['reg_fim'].replace(u'\r\n',u'').strip(), "%d/%m/%Y").date()
        workshop.email = self.clean_data(item['email']) 
        workshop.endereco = self.clean_data(item['endereco']) 
        workshop.uf = self.clean_data(item['uf']) 
        workshop.cidade = self.clean_data(item['cidade']) 
        workshop.bairro = self.clean_data(item['bairro']) 
        workshop.cep = self.clean_data(item['cep']) 
        workshop.tel = self.clean_data(item['tel']) 
        workshop.fax = self.clean_data(item['fax']) 
        workshop.resp_oper = self.clean_data(item['resp_oper'])
        
        self.workshops.append(workshop)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_closed(self):        
        try:
            db_workshops = self.db_session.query(Workshops).all()
           
            if len(db_workshops) == 0:
                print("WE SAVE THEM ALL!!")            
                self.db_session.bulk_save_objects(self.workshops)
                self.db_session.commit()

            # remover a diferenca - removida uma oficina
            elif len(db_workshops) > len(self.workshops):
                print("WE'VE MORE THAN WE NEED !!")
                # workshops_to_delete = set(db_workshops) - set(self.workshops)
                workshops_to_delete = self.diff_btw_listAB(db_workshops, self.workshops)
                print("N WORKSHOP TO DELETE :",len(workshops_to_delete))

                for workshop in workshops_to_delete:
                    print("LETS DELETE THIS GUY :", workshop)
                    self.db_session.delete(workshop)
                    self.db_session.commit()                 
                
            # adicionar a diferenca - adicionada uma oficina
            elif len(db_workshops) < len(self.workshops):
                print("WE'VE LESS THAN WE NEED !!")                
                workshops_to_add = self.diff_btw_listAB(self.workshops, db_workshops)
                print("N WORKSHOP TO ADD :",len(workshops_to_add))

                self.db_session.bulk_save_objects(workshops_to_add)
                self.db_session.commit()

            else :
                pass

            # verificar se teve alguma alteracao nos dados adicionados/retirados do inmetro
            print("LET ME CHECK IF WE HAVE SOME UPDATE !!")
            db_workshops = self.db_session.query(Workshops).all()
            workshops_to_update = self.check_and_update_workshops(self.workshops, db_workshops)

            #print("N WORKSHOPS TO UPDATE :", workshops_to_update)
            for ws_up in workshops_to_update:
                if ws_up is not None :
                    if ws_up.google_id == u'' :
                        print("CHANGE GOOGLE ID")
                        print("UPDATE: ", ws_up.num_reg)  

                        self.db_session.query(Workshops).filter(Workshops.num_reg == ws_up.num_reg).update(
                            {Workshops.nome: ws_up.nome,
                            Workshops.site: ws_up.site,
                            Workshops.reg_inicio: ws_up.reg_inicio,
                            Workshops.reg_fim: ws_up.reg_fim, 
                            Workshops.email: ws_up.email, 
                            Workshops.endereco: ws_up.endereco, 
                            Workshops.uf: ws_up.uf, 
                            Workshops.cidade: ws_up.cidade, 
                            Workshops.bairro: ws_up.bairro, 
                            Workshops.cep: ws_up.cep, 
                            Workshops.tel: ws_up.tel, 
                            Workshops.fax: ws_up.fax, 
                            Workshops.resp_oper: ws_up.resp_oper,
                            Workshops.google_id: ws_up.google_id}
                        , synchronize_session=False)
                        self.db_session.commit()
                    else :
                        print("DONT CHANGE GOOGLE ID")
                        print("UPDATE: ", ws_up.num_reg)

                        self.db_session.query(Workshops).filter(Workshops.num_reg == ws_up.num_reg).update(
                            {Workshops.nome: ws_up.nome,
                            Workshops.site: ws_up.site,
                            Workshops.reg_inicio: ws_up.reg_inicio,
                            Workshops.reg_fim: ws_up.reg_fim, 
                            Workshops.email: ws_up.email, 
                            Workshops.endereco: ws_up.endereco, 
                            Workshops.uf: ws_up.uf, 
                            Workshops.cidade: ws_up.cidade, 
                            Workshops.bairro: ws_up.bairro, 
                            Workshops.cep: ws_up.cep, 
                            Workshops.tel: ws_up.tel, 
                            Workshops.fax: ws_up.fax, 
                            Workshops.resp_oper: ws_up.resp_oper}
                        , synchronize_session=False)
                        self.db_session.commit()
                else :
                    pass
            
        except UnmappedInstanceError as e:
            print("Something wrong here: ", str(e))
            self.db_session.rollback()
            raise
        finally:
            print("WE'RE CLOSED!!")
            self.db_session.close()


    @classmethod
    def clean_data(self, data):
        if data is None:
            return data
        else:
            return data.strip()
    
    @classmethod
    def diff_btw_listAB(self, list_A, list_B):
        diff_list = []
        print("LISTA A",len(list_A))
        print("LISTA B",len(list_B))

        #return diff_list = [a for a in list_A if a not in list_B]

        for elmA in list_A:
            found_elm = False

            for elmB in list_B:
                if elmA.num_reg == elmB.num_reg:                    
                    found_elm = True
            
            if found_elm == False:
                print("ELM NOT FOUND IN LISTB ",elmA.num_reg)
                diff_list.append(elmA)

        return diff_list

    @classmethod
    def check_and_update_workshops(self, workshops, db_workshops_list):
        to_update = []
  
        for workshop in workshops:
            ws_to_update = self.check_elm_updated(workshop, db_workshops_list)
            to_update.append(ws_to_update)
            #if self.check_elm_updated(workshop, db_workshops_list):
                #to_update.append(workshop)

        return to_update

    @classmethod  
    def check_elm_updated(self, elm_updated, db_list):
        for db_elm in db_list:
            if db_elm.num_reg == elm_updated.num_reg:                      
                return self.check_values_change(db_elm, elm_updated)

    @classmethod           
    def check_values_change(self, db_elm, elm):
        if db_elm.endereco != elm.endereco :
            db_elm.google_id = u''

            db_attrs = vars(db_elm)
            print ', '.join("%s: %s" % item for item in db_attrs.items())
            
            return db_elm
        
        elif db_elm.nome != elm.nome or db_elm.site != elm.site \
             or db_elm.reg_inicio != elm.reg_inicio.strftime("%Y-%m-%d") \
             or db_elm.reg_fim != elm.reg_fim.strftime("%Y-%m-%d") or db_elm.email != elm.email \
             or db_elm.uf != elm.uf or db_elm.cidade != elm.cidade \
             or db_elm.bairro != elm.bairro or db_elm.cep != elm.cep or db_elm.tel != elm.tel \
             or db_elm.fax != elm.fax or db_elm.resp_oper != elm.resp_oper:

            return db_elm
        else:
            pass