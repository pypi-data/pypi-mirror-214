# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AccessMethodHistory(Base):
    __tablename__ = 'access_method_history'

    sc_nm = Column(String(128), primary_key=True, nullable=False, comment='source(vendor) name')
    svc_nm = Column(String(128), primary_key=True, nullable=False, comment='service name')
    version = Column(INTEGER(11), primary_key=True, nullable=False)
    crat_dtm = Column(DateTime, nullable=False)
    ex_stat_cd = Column(CHAR(3), nullable=False, server_default=text("'00S'"))
    access_aes = Column(Text, nullable=False)


class AssetClass(Base):
    __tablename__ = 'asset_classes'

    acg_nm = Column(String(64), primary_key=True, nullable=False, comment='asset class group')
    ac_nm = Column(String(128), primary_key=True, nullable=False, comment='asset class name')
    ac_desc = Column(String(256))


class Ingestion(Base):
    __tablename__ = 'ingestion'

    igt_id = Column(String(9), primary_key=True, nullable=False, comment='Ingestion ID')
    version = Column(INTEGER(11), primary_key=True, nullable=False, default=1, comment='Ingestion version')
    sv_alias = Column(String(64), nullable=False)
    sc_nm = Column(String(128), nullable=False)
    svc_nm = Column(String(128), nullable=False)
    ac_id = Column(String(9), nullable=False)
    exe_aes = Column(Text, nullable=False, comment='execute info')
    cron_exp = Column(String(32), nullable=False)
    post_igt_id = Column(String(9), comment='post ingestion job')
    json_path = Column(String(128), nullable=False, comment='Ingestion json path')
    input_json = Column(String(128), nullable=True, comment='input param json path')
    data_id = Column(String(80), nullable=True, default='unset_id', comment='sub data-source identifier')

class IngestionExe(Base):
    __tablename__ = 'ingestion_exe'

    igt_id = Column(String(9), primary_key=True, nullable=False, comment='Ingestion ID')
    version = Column(INTEGER(11), primary_key=True, nullable=False, comment='Ingestion version')
    igt_exe_num = Column(BIGINT(20), primary_key=True, nullable=False, comment='exe number')
    exe_dtm = Column(DateTime, nullable=False, comment='start time')
    upd_dtm = Column(DateTime, comment='update time')
    end_dtm = Column(DateTime, comment='end time')
    elapsed = Column(String(8), comment='HH:mm:ss')
    manual_yn = Column(CHAR(1), server_default=text("'N'"), comment='manual exe YN')
    igt_stat_cd = Column(CHAR(3), comment='pipe_code : stat')
    log = Column(Text)
    task_info_path = Column(String(256), comment='task.info full path')
    task_info = Column(Text)
    post_igt_id = Column(String(9), comment='post ingestion job')


class PipeCode(Base):
    __tablename__ = 'pipe_code'
    __table_args__ = {'comment': 'code table'}

    cd_g = Column(String(32), primary_key=True, nullable=False)
    cd = Column(String(8), primary_key=True, nullable=False)
    val = Column(String(64))


class PreIngestionItem(Base):
    __tablename__ = 'pre_ingestion_items'

    igt_id = Column(String(9), primary_key=True, nullable=False, comment='Ingestion ID')
    version = Column(INTEGER(11), primary_key=True, nullable=False, comment='Ingestion version')
    igt_exe_num = Column(BIGINT(20), primary_key=True, nullable=False, comment='exe number')
    post_exe_type = Column(String(8), primary_key=True, nullable=False, comment='bulk/step')
    item = Column(String(256), primary_key=True, nullable=False)


class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'comment': 'server list'}

    sv_alias = Column(String(64), primary_key=True, comment='server alias')
    sv_type_cd = Column(CHAR(3), nullable=False, comment='server type')
    access_aes = Column(Text, nullable=False, comment='server access info')
    json_path = Column(String(128), nullable=False, comment='server json path')


class Source(Base):
    __tablename__ = 'source'
    __table_args__ = {'comment': 'data source'}

    sc_nm = Column(String(128), primary_key=True, comment='source(vendor) name')
    sc_desc = Column(String(256), comment='source description')
    idcode = Column(String(32), comment='Identification Code Name')


class SourceService(Base):
    __tablename__ = 'source_service'

    sc_nm = Column(String(128), primary_key=True, nullable=False, comment='source(vendor) name')
    svc_nm = Column(String(128), primary_key=True, nullable=False, comment='service name')
    method = Column(String(32), nullable=False, server_default=text("'API'"))
    sc_desc = Column(String(256), comment='service description')
    access_aes = Column(Text, nullable=False, comment='service access info')
    access_method = Column(Text, comment='get access info')


class Ing_svr_vw(Base):
    __tablename__ = 'ing_svr_vw'
    igt_id = Column(String(9), primary_key=True, nullable=False, comment='Ingestion ID')    
    svc_nm = Column(String(128), nullable=False)
    sc_nm = Column(String(128), nullable=False)    
    ac_id = Column(String(9), nullable=False)
    exe_aes = Column(Text, nullable=False, comment='execute info')
    cron_exp = Column(String(32), nullable=False)
    post_igt_id = Column(String(9), comment='post ingestion job')
    sv_alias = Column(String(64), primary_key=True, comment='server alias')    
    access_aes = Column(Text, nullable=False, comment='server access info')
    sv_type_cd = Column(CHAR(3), nullable=False, comment='server type')
    version = Column(INTEGER(11), primary_key=True, nullable=False, default=1, comment='Ingestion version')
    input_json = Column(String(128), nullable=True, comment='input param json path')
    data_id = Column(String(80), nullable=True, default='unset_id', comment='sub data-source identifier')