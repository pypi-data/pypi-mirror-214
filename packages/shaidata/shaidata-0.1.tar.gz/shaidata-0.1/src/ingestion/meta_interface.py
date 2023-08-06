from dataclasses import asdict
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence
import logging
import json
import sys
from croniter import croniter
from src.orm.meta_db import DB
from src.orm.meta_session import SessionHandler
from src.orm.meta_model import Ingestion, Ing_svr_vw, IngestionExe
import src.util.util as util
import paramiko
from datetime import datetime
import textwrap
import funcy
from croniter import croniter
from crontab import CronTab


class MetaITF:
    def __init__(self, logger: logging.Logger, properties: json):
        self.log = logger
        self.prop = properties
        self.db = DB.create()
        self.session = sessionmaker(bind=self.db.engine)()

    def new_id(self):
        with self.db.connect() as conn:
            return '{}{}'.format("IGT", str(conn.execute(Sequence("igt_seq"))).zfill(6))

    def add(self, json_file):
        ingestion_session = SessionHandler.create(self.session, Ingestion)
        igt_data = dict(json.load(json_file))

        
        # Json Data Check
        is_valid = ""
        if not croniter.is_valid(igt_data["cron_exp"]):
            is_valid = "{}:{}".format("Invalid Cron Exp", igt_data["cron_exp"])
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)

        # check duplicated IGT_ID
        if ingestion_session.get_one( {"igt_id": igt_data["igt_id"]}):
            is_valid += "{}:{}".format("IGT_ID is alrady exists in DB", igt_data["igt_id"])
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)

        

        try:
            # get new ID
            #igt_data["igt_id"] = self.new_id()

            # AES
            aes = util.AESCipher(self.prop["aes"]["key"])
            encrypt = aes.encrypt(str(igt_data["exe_aes"]))
            igt_data["exe_aes"] = encrypt
            igt_data["input_json"] = aes.encrypt(str(igt_data["input_json"]))

            # write json
            self.log.info(f"{igt_data=}")
            new_json_path = util.write_json_file(igt_data, "ingestion", "add", igt_data["igt_id"])
            igt_data["json_path"] = new_json_path

            # insert
            ingestion_session.add(igt_data)
            self.session.commit()
            self.log.info("{} created.".format(igt_data["igt_id"]))
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()




    def delete(self, _igt_id):
        self.log.info('igt_id:',_igt_id )
        ingestion_session = SessionHandler.create(self.session, Ingestion)
        igt_data = _igt_id
        
        # ~~~
        # check igt_id exists
        is_valid = ""
        
        if not ingestion_session.get_one( {"igt_id": _igt_id}):
            is_valid = "{}:{}".format("Invalid IGT ID", _igt_id)                        
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~

        try:
            self.log.info(f"{igt_data=}")
            ingestion_session.delete( {"igt_id": _igt_id})
            self.session.commit()
            self.log.info("{} deleted.".format(_igt_id))
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()



    def list(self, igt_list_max_display_count):
        ingestion_session = SessionHandler.create(self.session,Ingestion)
        aes = util.AESCipher(self.prop["aes"]["key"])
        DEFAULT_DISPLAY = 80
        max_display = DEFAULT_DISPLAY
        
        if type(igt_list_max_display_count) == int:
            max_display = DEFAULT_DISPLAY
        else:
            max_display = igt_list_max_display_count[0]
        
        try:
            self.log.info(f"{igt_list_max_display_count=}")
            
            # select 
            
            igt_list=ingestion_session.get_all({})            

            if max_display > len(igt_list):
                max_display = len(igt_list)
            
            idx=0
            print("+ {} + {} + {} + {} + {} + {} + {} + {} + {} + {} + ".format("-"*3,"-"*10,"-"*7,"-"*15,"-"*15,"-"*10,"-"*15,"-"*30,"-"*10,"-"*13))
            print("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                "%-3s"%"Seq", "%-10s"%"IGT ID", "%-7s"%"Version",
                "%-15s"%"Sc_nm", "%-15s"%"Svc_nm", "%-10s"%"Sv_alias",
                "%-15s"%"Cron_exp", "%-30s"%"exe_aes", "%-10s"%"ac_id", "%-13s"%"data_id"))
            print("+ {} + {} + {} + {} + {} + {} + {} + {} + {} + {} + ".format("-"*3,"-"*10,"-"*7,"-"*15,"-"*15,"-"*10,"-"*15,"-"*30,"-"*10,"-"*13))
            for member in igt_list:
                if idx == max_display:
                    break;
                idx=idx+1
                print("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    "%-3s"%str(idx),"%-10s"%str(member.igt_id),"%-7s"%str(member.version),
                    "%-15s"%str(member.sc_nm),"%-15s"%str(member.svc_nm),"%-10s"%str(member.sv_alias),
                    "%-15s"%str(member.cron_exp),"%-30s"%(str(aes.decrypt(member.exe_aes))[:25]+'...')
                    ,"%-10s"%str(member.ac_id),"%-13s"%str(member.data_id)))
            print("+ {} + {} + {} + {} + {} + {} + {} + {} + {} + {} + ".format("-"*3,"-"*10,"-"*7,"-"*15,"-"*15,"-"*10,"-"*15,"-"*30,"-"*10,"-"*13))
            
            self.log.info("{} in list. I tried to display {} igt.(default: {})".format(len(igt_list),max_display,DEFAULT_DISPLAY))

        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()


    def update(self, inputs):
        ingestion_session = SessionHandler.create(self.session, Ingestion)
        _igt_id, json_file  = inputs.values()
        igt_data = dict(json.load(json_file))

        # ~~~
        # Json Data Check
        is_valid = ""
        if not croniter.is_valid(igt_data["cron_exp"]):
            is_valid = "{}:{}".format("Invalid Cron Exp", igt_data["cron_exp"])
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        
        # check igt_id exists
        if not ingestion_session.get_one( {"igt_id": _igt_id} ):
            is_valid = "{}:{}".format("IGT_ID is not exists in DB", _igt_id)                        
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)

        if not igt_data["igt_id"] == _igt_id:
            is_valid = "{}: Input IGT_ID=={}, File IGT_ID=={}".format("igt_id is not same.", _igt_id,igt_data["igt_id"])
        if is_valid != "":
            self.log.info(is_valid)
            sys.exit(is_valid)
        # ~~~


        try:
            #get legacy version
            legacy_version=ingestion_session.raw_sql( """
            select igt_id ,version ,sv_alias ,sc_nm ,svc_nm ,ac_id ,exe_aes ,cron_exp ,post_igt_id ,json_path ,input_json
            from shai_data_meta.ingestion
            where igt_id = '{}' and version = (select max(version) from shai_data_meta.ingestion where igt_id = '{}' )""".format(_igt_id, _igt_id))
            
            data_t = str(legacy_version[0]).replace("'",'"').replace("None",'""')            
            data_t = json.loads(data_t)
            new_version = data_t['version'] + 1

            # delete old data
            #ingestion_session.delete( {"igt_id": _igt_id})
            #self.session.commit()
            #self.log.info("{} deleted.".format(_igt_id))

            #set igt_id, new_version
            igt_data["igt_id"] = _igt_id
            igt_data["version"] = new_version

            # AES
            aes = util.AESCipher(self.prop["aes"]["key"])
            igt_data["exe_aes"] = aes.encrypt(str(igt_data["exe_aes"]))
            igt_data["input_json"] = aes.encrypt(str(igt_data["input_json"]))

            # write new json
            self.log.info(f"{igt_data=}")
            new_json_path = util.write_json_file(igt_data, "ingestion", "add", igt_data["igt_id"])
            igt_data["json_path"] = new_json_path

            # insert
            ingestion_session.add(igt_data)
            self.session.commit()
            self.log.info("{} updated(new version inserted).".format(igt_data["igt_id"]))
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.session.rollback()
            raise e
        finally:
            self.session.close()

 
    def info(self, _igt_id):        
        ingestion_session = SessionHandler.create(self.session, Ingestion)
        igt_data = _igt_id
        aes = util.AESCipher(self.prop["aes"]["key"])
        # ~~~
        # check igt_id exists
        is_valid = ""
        
        if not ingestion_session.get_one( {"igt_id": _igt_id}):
            is_valid = "{}: {}".format("IGT_ID is not exists in DB", _igt_id)
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~

        data_v={}
        try:
            self.log.info(f"{igt_data=}")            
            ingestion_info = ingestion_session.get_one( {"igt_id": _igt_id})
            for key in ingestion_info.__table__.columns:
                data_v[key.name]=getattr(ingestion_info, key.name)
            
            data_v['exe_aes'] = aes.decrypt(data_v['exe_aes'])

            if data_v['input_json'] != None:  #  추가정보인 input_json이 있다면.
                data_v = util.extract_enc_json(data_v,data_v['input_json']) # data_v = util.extract_enc_json(data_v,data_v.pop('input_json'))

            util.table_printer(data_v,['Column','Value'],[15,70])
            
            
            self.log.info("{} selected.".format(_igt_id))
        except Exception as e:
            self.log.error(traceback.format_exc())            
            raise e
        finally:
            self.session.close()


    def exec(self, _igt_id):        
        ing_svr_vw_session = SessionHandler.create(self.session, Ing_svr_vw)
        vw_data = _igt_id
        aes = util.AESCipher(self.prop["aes"]["key"])

        # ~~~
        # check igt_id exists
        is_valid = ""
        
        VALUE_LENGTH = 100

        if not ing_svr_vw_session.get_one( {"igt_id": _igt_id}):
            is_valid = "{}: {}".format("IGT_ID is not exists in DB", _igt_id)
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~

        # Init Vars 
        exe_aes = ""
        access_aes = ""

        data_v = {} # View data: dataset from View(ing_svr_vw)
        data_t = {} # Task execution: for ingestion_exe
        #data_j = {} # Json: for json input

        stdout_msg = ''
        stderr_msg = ''
        
        INPUT_JSON_EXISTS = False

        TASK_INFO_READ_ERR = "error occured while read task info file."
        TASK_EXECUTOR_ERR = "error occured while execute remote command."

        try:
            self.log.info(f"{vw_data=}")  
            
            # 최종 버전을 가져와야 할 필요가 있음.
            ingestion_info = ing_svr_vw_session.raw_sql( """
            select igt_id, data_id, exe_aes, cron_exp, post_igt_id, sv_alias, access_aes, sv_type_cd, version, input_json, sc_nm, svc_nm
            from ing_svr_vw where igt_id = '{}'
            and version = (select max(version) from ing_svr_vw where igt_id = '{}')
            """.format(_igt_id,_igt_id))            

            # get values
            data_v = str(ingestion_info[0]).replace("'",'"').replace("None",'""')
            
            data_v = json.loads(data_v)
            

            data_v['exe_aes'] = aes.decrypt(data_v['exe_aes'])
            data_v = util.extract_enc_json(data_v, data_v['access_aes'])

            if len(data_v['input_json']) > 0: 
                INPUT_JSON_EXISTS = True
            

            if INPUT_JSON_EXISTS:            #  추가정보인 input_json이 있다면.
                data_v['input_json'] = json.loads(aes.decrypt(data_v['input_json']).replace("'",'"'))
                #len(data_v['input_json'])
                #data_v = util.extract_enc_json(data_v, data_v['input_json'])                
            
                
            
            util.table_printer(data_v,['Column','Value'],[15,70])
         
            self.log.info(f"{data_v=}") 

            # copy key:value
            #data_j = {k: v for k, v in data_v.items() if k in {'igt_id','sc_nm','svc_nm','ac_id'}}
            #self.log.info(f"{data_j=}") 
            
            # 파라미터 전체를 전달.
            input_json_enc = aes.encrypt(json.dumps(data_v))

            # execute command. 
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(data_v['hostname'], data_v['ssh_port'], username=data_v['user']) # password-less ssh환경을 전제조건으로 함.
            
            stdin, stdout, stderr = ssh.exec_command(data_v['exe_aes'])


            if INPUT_JSON_EXISTS:  #  원격 ssh 실행시에 전달해야할 추가정보인 input_json이 있다면                
                temp_list=[aes.decrypt(input_json_enc)]
                util.table_printer_list(temp_list,'Parameters',90)
                stdin.write(input_json_enc)
                stdin.flush()
                stdin.channel.shutdown_write()
                data_v['total_cmd'] = data_v['exe_aes'] + ' < ' + input_json_enc
            else:
                data_v['total_cmd'] = data_v['exe_aes']
            
            stdout_msg = stdout.readlines()
            if len(stdout_msg) > 0:
                util.table_printer_list(stdout_msg, "Stdout Result", 80)
                


            stderr_msg = stderr.readlines()
            if len(stderr_msg) > 0:
                util.table_printer_list(stderr_msg, "Stderr Result", 80)
                stdout_msg.insert(0,TASK_EXECUTOR_ERR) # 원격지에 executor를 실행할때 오류가 발생했음을 알림.
            

            ingestion_exe_session = SessionHandler.create(self.session, IngestionExe)
                        
            if len(stdout_msg) > 0: # stdout_msg이 존재할때만 task_info를 읽는다.(오류 발생시 task_info 파일이 생성되지 않음.)
                log_tail_cmd = 'tail -n 1 ' + stdout_msg[0] # task info full path의 경로에서 마지막 줄을 read
                tmp_lst=[log_tail_cmd]
                util.table_printer_list(tmp_lst ,'read task info CLI', 80)
            
                stdin, stdout, stderr = ssh.exec_command(log_tail_cmd)
                cat_msg = stdout.readlines()
                stdout_msg.insert(0, '\n[stdout]\n') # stdout_msg 첫줄에 헤더를 입힌다.

            if len(stderr_msg) > 0: # 오류가 있다면 task_info를 읽은 결과가 아니라, error라고 기록한다.
                cat_msg = [TASK_INFO_READ_ERR]
                stderr_msg.insert(0, '\n[stderr]\n') # stderr_msg 첫줄에 헤더를 입힌다.
                print('[log_tail_cmd Will not execute]')

            data_t["log"]            = '\n'.join(stdout_msg)
            if len(cat_msg) > 0:
                if cat_msg[0] != TASK_INFO_READ_ERR:
                    data_t["log"] = data_t["log"] + '\n'.join(stderr_msg)

            #create dataset  
            data_t = {k: v for k, v in data_v.items() if k in {'igt_id', 'version', 'post_igt_id'}} # copy key:value          
            data_t["igt_exe_num"]    = "1"
            data_t["exe_dtm"]        = datetime.now()
            data_t["upd_dtm"]        = datetime.now()
            #data_t["end_dtm"]        = NULL
            data_t["elapsed"]        = ''
            data_t["manual_yn"]      = 'Y'
            data_t["igt_stat_cd"]    = '00S'            
            data_t["task_info_path"] = stdout_msg[1] # 첫줄에는 stdout 이라는 header가 들어간다.
            data_t["task_info"]      = '\n'.join(cat_msg)            


            #insert executed info
            # 이미 존재하는 execution이면 insert 전에 igt_exe_num + 1 로 수정
            if ingestion_exe_session.get_one( {"igt_id":  data_t["igt_id"]}):
                div_msg = "{}: {}".format("IGT_ID is already exists in DB", data_t["igt_id"])

                # igt와 version까지 동일한 row을 얻어와야함.(PK cols)
                lecacy_data = ingestion_exe_session.raw_sql("select max(igt_exe_num) igt_exe_num from ingestion_exe where igt_id = '" 
                + _igt_id + "' and version = '" + str(data_t["version"])  + "'")

                data_e = str(lecacy_data[0]).replace("'",'"').replace("None",'""')            
                data_e = json.loads(data_e)
                
                
                # get execute_times
                last_igt_exe_num = 0

                if data_e['igt_exe_num'] == None or data_e['igt_exe_num'] == "":
                    data_e['igt_exe_num'] = 0

                elif last_igt_exe_num < int(data_e['igt_exe_num']):
                    last_igt_exe_num = int(data_e['igt_exe_num'])
                
                data_t["igt_exe_num"] = last_igt_exe_num + 1

            else:            
                div_msg = "{} {}".format("IGT_ID not exists in DB. This is first Execution of ", data_t["igt_id"])               
            
            self.log.info(f"{data_t=}")             

            ingestion_exe_session.add(data_t)                
            self.session.commit()            

            print("+ {} + {} + ".format("-"*15,"-"*70))
            print("| {} | ".format("%-88s"%"Database Dataset"))
            util.table_printer(data_t, ['Key','Value'], [15,70])
            
            self.log.info("{} logging.".format(data_t["igt_id"]))
            tmp_lst = [data_v['total_cmd']]
            util.table_printer_list(tmp_lst, 'Total Command', 90)
        except Exception as e:
            self.log.error(traceback.format_exc())            
            raise e

        finally:
            self.session.close()
            ssh.close()

    def info(self, _igt_id):        
        ingestion_session = SessionHandler.create(self.session, Ingestion)
        igt_data = _igt_id
        aes = util.AESCipher(self.prop["aes"]["key"])
        # ~~~
        # check igt_id exists
        is_valid = ""
        
        if not ingestion_session.get_one( {"igt_id": _igt_id}):
            is_valid = "{}: {}".format("IGT_ID is not exists in DB", _igt_id)
        if is_valid != "":
            self.log.error(is_valid)
            sys.exit(is_valid)
        # ~~~

        data_v={}
        try:
            self.log.info(f"{igt_data=}")            
            ingestion_info = ingestion_session.get_one( {"igt_id": _igt_id})
            for key in ingestion_info.__table__.columns:
                data_v[key.name]=getattr(ingestion_info, key.name)
            
            data_v['exe_aes'] = aes.decrypt(data_v['exe_aes'])

            if data_v['input_json'] != None:  #  추가정보인 input_json이 있다면.
                data_v = util.extract_enc_json(data_v,data_v['input_json']) # data_v = util.extract_enc_json(data_v,data_v.pop('input_json'))

            util.table_printer(data_v,['Column','Value'],[15,70])
            
            
            self.log.info("{} selected.".format(_igt_id))
        except Exception as e:
            self.log.error(traceback.format_exc())            
            raise e
        finally:
            self.session.close()