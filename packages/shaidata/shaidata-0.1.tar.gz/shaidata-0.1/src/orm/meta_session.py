import json
import datetime
import time
import logging
import traceback
from dataclasses import asdict
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.util.logger import Logger
import src.util.util as utils

prop = utils.get_prop()
log = Logger(prop).init_logger()


class SchemaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return time.strftime('%Y-%m-%dT%H:%M:%SZ', obj.utctimetuple())
        return json.JSONEncoder.default(self, obj)


class SessionHandler:
    __instance = None

    def __init__(self, session, model):
        SessionHandler.__instance = self
        self.model = model
        self.session = session

    @staticmethod
    def create(session, model):
        try:
            SessionHandler.__instance = SessionHandler(session, model)
        except Exception as e:
            log.error(traceback.format_exc())
            raise e
        return SessionHandler.__instance

    @staticmethod
    def to_json(record_obj):
        return json.dumps(asdict(record_obj), cls=SchemaEncoder, ensure_ascii=False)

    def add(self, record_dict):
        try:
            record_model = self.model(**record_dict)
            self.session.add(record_model)
        except Exception as e:
            log.error(traceback.format_exc())
            raise e

    def insert_many(self, record_list):
        statements = [pg_insert(self.model).values(record_dict).on_conflict_do_nothing() for record_dict in record_list]
        return [self.session.execute(statement) for statement in statements]

    def add_many(self, record_list):
        return self.session.add_all([self.model(**record_dict) for record_dict in record_list])

    def update(self, query_dict, update_dict):
        return self.session.query(self.model).filter_by(**query_dict).update(update_dict)

    def upsert(self, record_dict, set_dict, constraint):
        statement = pg_insert(self.model).values(record_dict).on_conflict_do_update(
            constraint=constraint,
            set=set_dict
        )
        return self.session.execute(statement)

    def get(self, id, to_json=None):
        result = self.session.query(self.model).get(id)
        return asdict(result) if to_json is None else to_json(result)
        #return result

    def get_one(self, query_dict, to_json=None):
        result = self.session.query(self.model).filter_by(**query_dict).first()
        #return asdict(result) if to_json is None else to_json(result)
        return result

    def get_latest(self, query_dict, to_json=None):
        result = self.session.query(self.model).filter_by(**query_dict).order_by(self.model.updated_at.desc()).first()
        return None if result is None else (asdict(result) if to_json is None else to_json(result))

    def get_count(self, query_dict, to_json=None):
        return self.session.query(self.model).filter_by(**query_dict).count()

    def get_all(self, query_dict, to_json=None):
        results = self.session.query(self.model).filter_by(**query_dict).all()
        #return [asdict(result) if to_json is None else to_json(result) for result in results]
        return results

    def raw_sql(self, query_str, to_json=None):
        resultset = self.session.execute(query_str)
        return resultset.mappings().all()  # return as "list include dict"
        """
        results_as_dict = resultset.mappings().all()
        #return results_as_dict
        dict_result={}
        dict_result 
        return [ for result in results_as_dict]
        #return [asdict(results_as_dict) if to_json is None else to_json(results_as_dict) for results_as_dict in results_as_dict]
        """

    def delete(self, query_dict):
        return self.session.query(self.model).filter_by(**query_dict).delete()
