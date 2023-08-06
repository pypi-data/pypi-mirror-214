from pathlib import Path
from Crypto.Cipher import AES
import base64
import json
from shutil import copyfile
prop = {}


def get_project_path():
    return Path(__file__).parent.parent.parent


def get_prop():
    global prop
    if prop == {}:
        prop = json.load(open(Path.joinpath(get_project_path(), "config/config.json")))
    return prop


def b64_encode(enc, encoding):
    return base64.b64encode(enc).decode(encoding)


def b64_decode(enc):
    return base64.b64decode(enc)


def copy_file(src, dst):
    copyfile(src, dst)


def write_json_file(jsn, _command, _purpose, _id):
    write_path = Path.joinpath(get_project_path(), "src/{}/json/{}_{}.json".format(_command, _id, _purpose))
    with open(write_path, "w") as json_file:
        json.dump(jsn, json_file, sort_keys=True, indent=4)
    return write_path

def delete_json_file(jsn, _command, _purpose, _id):
    write_path = Path.joinpath(get_project_path(), "src/{}/json/{}_{}.json".format(_command, _id, _purpose))
    with open(write_path, "w") as json_file:
        json.dump(jsn, json_file, sort_keys=True, indent=4)
    return write_path


class AESCipher(object):
    def __init__(self, key):
        # 최초 sha256 hash key 만들때 사용
        # self.key = hashlib.sha256((key + 'security').encode()).digest()    # 256bit hash key
        self.key = b64_decode(key)
        self.block_size = int(prop['aes']['block_size'])
        self.encoding = prop['general']['encoding']

    def pad(self, _s):
        return _s + (self.block_size - len(_s) % self.block_size) \
            * chr(self.block_size - len(_s) % self.block_size).encode()

    @staticmethod
    def un_pad(_s):
        return _s[:-ord(_s[len(_s) - 1:])]

    def __iv(self):
        return chr(0) * int(prop['aes']['block_size'])

    def encrypt(self, message):
        message = message.encode()
        raw = self.pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode(self.encoding))
        enc = cipher.encrypt(raw)
        return b64_encode(enc, self.encoding)

    def decrypt(self, enc):
        enc = b64_decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode(self.encoding))
        dec = cipher.decrypt(enc)
        return self.un_pad(dec).decode(self.encoding)

def print_line(col_size , char_str = "-"):
    print(str(char_str) * int(col_size))
    