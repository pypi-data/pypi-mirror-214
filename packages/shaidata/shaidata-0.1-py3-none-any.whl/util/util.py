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


def extract_enc_json(data_v, enc_json_str):        
    aes = AESCipher(prop["aes"]["key"])
    json_str = str(aes.decrypt(enc_json_str)).replace("'", "\"")      
    for key, value in json.loads(json_str).items():
        data_v[str(key)] = value
    return data_v # return dict


def table_printer(dict_data, header_str, column_len):    
    print("+ {} + {} + ".format("-"*column_len[0],"-"*column_len[1]))
    print("| {} | {} | ".format(("%-"+str(column_len[0])+"s")%header_str[0],("%-"+str(column_len[1])+"s")%header_str[1]))            
    print("+ {} + {} + ".format("-"*column_len[0],"-"*column_len[1]))
    for key, value in dict_data.items():
        print("| {} | {} | ".format("%-15s"%str(key),"%-70s"%str(value)))            
    print("+ {} + {} + ".format("-"*column_len[0],"-"*column_len[1]))

def table_printer_list(list_data, header_str, column_len):    
    print("+ {} +".format("-"*column_len))
    print("| {} | ".format(("%-"+str(column_len)+"s")%header_str))
    print("+ {} +".format("-"*column_len))
    for line in list_data:                                
        print("| {} |".format(("%-"+str(column_len)+"s")%line.strip()),  end = '\n')
    print("+ {} +".format("-"*column_len))

def print_line(col_size = 80 ,char_str = "-"):
    print("{}".format(char_str * col_size))
    