import util as utils
import json


prop = utils.get_prop()
"""
aes = utils.AESCipher(prop['aes']['key'])
print(aes.key)
print(type(aes.key))

b64 = utils.b64_encode(aes.key, prop['general']['encoding'])
print(b64)
# /QVvzk+5hiu9jdp2RZAlp7jVbnAXSF65+bgXOs06zJw=
print(type(b64))
aes_key = utils.b64_decode(b64)
print(aes_key)
"""

aes = utils.AESCipher("/QVvzk+5hiu9jdp2RZAlp7jVbnAXSF65+bgXOs06zJw=")


print("-------------")
encrypt = aes.encrypt("shaidata")
print(encrypt)
decrypt = aes.decrypt(encrypt)
print(decrypt)


temp_str = aes.decrypt("Cskyu5hxKuKYPf0xnPuarkOBMNfqBgXGrTtRLUWz3fxMh0cWuBSZB/WDkibZofu6sl4u+p310APZcSt2b1Kv5M4CjUvZsvuKFJ667SXujiUBLkZpsaVqBcVm9uKG9hS5MNTeH/CBEb5e1D9IMXwSseXr++sKLkLRkMCiqSXT+g9+X+g9+m/VCejMRe0RifvF0+K2mblxVrHd6zAVR7+hcA==") # .replace("'",'"')
print('temp_str: ',temp_str)



data_j = {}
# json.load(data_v['input_json'])
data_j['igt_id'] = '1'

# data_j['access_aes'] = data_v['access_aes']            

for key, value in json.loads(temp_str).items():
    data_j[str(key)] = str(value)

# print(data_j)
            
            

