import logging
import sqlalchemy
import json
from src.util.util import AESCipher
import src.util.util as utils


class DB:
    __instance = None  # for singleton

    def __init__(self):
        if DB.__instance is None:
            DB.__instance = self
        self.engine = self.create_engine()

    @staticmethod
    def create():
        if DB.__instance is None:
            DB.__instance = DB()
        return DB.__instance

    @staticmethod
    def create_engine():
        prop = utils.get_prop()
        aes = AESCipher(prop['aes']['key'])
        password = aes.decrypt(prop['meta']['password'])

        return sqlalchemy.create_engine(
          'mysql+{engine}://{user}:{password}@{host}:{port}/{database}'
          .format(
            engine=prop['meta']['engine'],
            user=prop['meta']['user'],
            password=password,
            host=prop['meta']['host'],
            port=prop['meta']['port'],
            database=prop['meta']['database']
          ), echo=prop['meta']['orm_echo'])

    def connect(self):
        return self.engine.connect()

