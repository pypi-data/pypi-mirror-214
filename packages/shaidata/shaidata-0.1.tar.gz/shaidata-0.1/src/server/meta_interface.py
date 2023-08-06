import traceback
from sqlalchemy.orm import sessionmaker
import logging
import json
from src.orm.meta_db import DB
from src.orm.meta_session import SessionHandler
from src.orm.meta_model import Server
import src.util.util as util
import sys


class MetaITF:
    def __init__(self, logger: logging.Logger, properties: json):
        self.log = logger
        self.prop = properties
        self.db = DB.create()
        self.session = sessionmaker(bind=self.db.engine)()

    def add(self, json_file):
        server_session = SessionHandler.create(self.session, Server)
        server_data = dict(json.load(json_file))

        # ~~~
        # exists Check                
        is_valid = ""
        if server_session.get_one( {"sv_alias": server_data["sv_alias"]}):
            is_valid += "{}:{}".format("sv_alias is alrady exists in DB", server_data["sv_alias"])
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)

        try:
            # AES
            aes = util.AESCipher(self.prop["aes"]["key"])
            encrypt = aes.encrypt(str(server_data["access_aes"]))
            server_data["access_aes"] = encrypt


            server_data["sv_alias"] = server_data["sv_alias"].replace(' ','_')

            # write json
            self.log.info(f"{server_data=}")
            new_json_path = util.write_json_file(server_data, "server", "add", server_data["sv_alias"])
            server_data["json_path"] = new_json_path
            # insert
            server_session.add(server_data)
            self.session.commit()
            self.log.info("{} created.".format(server_data["sv_alias"]))
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()


    def info(self, _alias):        
        server_session = SessionHandler.create(self.session, Server)
        alias_name = _alias
        aes = util.AESCipher(self.prop["aes"]["key"])
        # ~~~
        # check igt_id exists
        is_valid = ""
        
        if not server_session.get_one( {"sv_alias": alias_name}):
            is_valid = "{}: {}".format("alias is not exists in DB", alias_name)
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~
        
        svr_info = ""
        access_info = ""
        data_v = {}
        try:
            self.log.info(f"{svr_info=}")
            svr_info = server_session.get_one( {"sv_alias": alias_name})

            for key in svr_info.__table__.columns:
                if str(key).replace('server.','') in ('access_aes'):                    
                    data_v[str(key).replace('server.', '')] = str(getattr(svr_info, key.name)).replace("'",'"')                
                else:
                    data_v[str(key).replace('server.', '')] = str(getattr(svr_info, key.name))

            data_v = util.extract_enc_json(data_v,data_v.pop('access_aes'))
            
            self.log.info("{} selected.".format(alias_name))
                        
            self.log.info(f"{data_v=}")            
            
            util.table_printer(data_v,['Column','Value'],[15,70])

            self.log.info("{} detail.".format(alias_name))
            
        except Exception as e:
            self.log.error(traceback.format_exc())            
            raise e
        finally:
            self.session.close()


    def list(self, svr_list_max_display_count):
        server_session = SessionHandler.create(self.session, Server)
        DEFAULT_DISPLAY = 80
        max_display = DEFAULT_DISPLAY
        
        if type(svr_list_max_display_count) == int:
            max_display = DEFAULT_DISPLAY
        else:
            max_display = svr_list_max_display_count[0]
        try:
            self.log.info(f"{svr_list_max_display_count=}")
            
            # select 
            svr_list = server_session.get_all({})
            idx=0
            print("+ {} + {} + {} + {} + {} + ".format("-"*3,"-"*15,"-"*10,"-"*30,"-"*70))
            print("| {} | {} | {} | {} | {} | ".format("%-3s"%"Seq","%-15s"%"sv_alias","%-10s"%"sv_type_cd","%-30s"%"access_aes(syncopation)","%-70s"%"json_path"))
            print("+ {} + {} + {} + {} + {} + ".format("-"*3,"-"*15,"-"*10,"-"*30,"-"*70))
            for member in svr_list:
                if idx == max_display:
                    break;
                idx=idx+1               
                print("| {} | {} | {} | {} | {} |".format("%-3s"%str(idx),"%-15s"%str(member.sv_alias),"%-10s"%str(member.sv_type_cd)
                ,"%-30s"%(str(member.access_aes)[:25]+'...'),"%-70s"%str(member.json_path)))
            print("+ {} + {} + {} + {} + {} + ".format("-"*3,"-"*15,"-"*10,"-"*30,"-"*70))
            
            self.log.info("{} in list. I tried to display {} svr.(default: {})".format(len(svr_list), max_display, DEFAULT_DISPLAY))

        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()



    def delete(self, _sv_alias):
        # self.log.info('sv_alias:',_sv_alias )
        server_session = SessionHandler.create(self.session, Server)        
        
        # ~~~
        # check igt_id exists
        is_valid = ""
        
        if not server_session.get_one( {"sv_alias": _sv_alias}):            
            is_valid = "{}: {}".format("sv_alias is not exists in DB", _sv_alias)
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~

        try:
            sv_data = server_session.get_one( {"sv_alias": _sv_alias})
            # self.log.info(f"{sv_data=}")
            server_session.delete( {"sv_alias": _sv_alias})
            self.session.commit()
            self.log.info("{} deleted.".format(_sv_alias))
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()


    def update(self, inputs):
        server_session = SessionHandler.create(self.session, Server)
        sv_alias, json_file  = inputs.values()
        server_data = dict(json.load(json_file))

        # ~~~
        # Json Data Check
        is_valid = ""        
        
        # check sv_alias exists
        if not server_session.get_one( {"sv_alias": sv_alias} ):
            is_valid = "{}:{}".format("sv_alias is not exists in DB", sv_alias)                        
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)

        if not server_data["sv_alias"] == sv_alias:
            is_valid = "{}: Input sv_alias=={}, File sv_alias=={}".format("sv_alias is not same.", sv_alias,server_data["sv_alias"])
        if is_valid != "":
            self.log.info(is_valid)
            sys.exit(is_valid)
        # ~~~


        try:
            
            # delete old data
            server_session.delete( {"sv_alias": sv_alias})
            self.session.commit()
            self.log.info("{} deleted.".format(sv_alias))

            
            # AES
            aes = util.AESCipher(self.prop["aes"]["key"])
            encrypt = aes.encrypt(str(server_data["access_aes"]))
            server_data["access_aes"] = encrypt


            server_data["sv_alias"] = server_data["sv_alias"].replace(' ','_')

            # write json
            self.log.info(f"{server_data=}")
            new_json_path = util.write_json_file(server_data, "server", "add", server_data["sv_alias"])
            server_data["json_path"] = new_json_path
            # insert
            server_session.add(server_data)
            self.session.commit()
            self.log.info("{} created.".format(server_data["sv_alias"]))

        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()
