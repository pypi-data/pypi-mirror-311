import os
import yaml
from os import path as op
from cryptography.fernet import Fernet

INDY_CARE_CONFIG_FILE = op.join(op.abspath(op.dirname(__file__)), "config.yml")
INDY_CARE_CONFK_FILE = op.join(op.abspath(op.dirname(__file__)), ".inc_confk")

SERIAL_STRING = b"gAAAAABnRrZq1SKvT8lCM6wQ8K3q8_b1atMKT9NTkgsyQ7OauLxO6_4d9QZmD_FmbQWNzUSE0KrXlRS7-MLXix4mmFMCRsGFB-AY-9f-3H_QMxKT1hhuqhg3OFA1oNh3uASM8Qq4sfUflFZrViLXgeI3nTanVBM2BX3fAgvyTYadSim6YTstSBe3mnL4nyWmOn0_yYAYnhPJI4glAj5BuqY1OoCbKY87ZvOQ_k5xJMM6Sz1YtInvAvMbaoKbyBj_nk1kAdzBuWW2JY3n6qlvnRw05YsaVovXf4NLsn-fT-EDl8KU_5aSx1ahbrWEqXtP3PByElQluQKuCb3odj9PuKzoRkXainvC53fFUOZmBEt-vlyXNBiavVJYPf2ZN5GdZ0hYjzIMXsKxCNlVWyRb9rWGqc7RMZ0lQkofieXgYfoSspUPPfDnKpQFmxGgYHOlwl12nzyJyjQe"

def load_config() -> dict:
    try:
        with open(INDY_CARE_CONFIG_FILE, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data["rtsp"]:
                data["rtsp"] = f'{data["rtsp_url"]}'
            else:
                pass
            print("Load IndyCARE configuration file")
        with open(INDY_CARE_CONFK_FILE, 'rb') as f:
            conf_k = f.read()
        # conf_k = os.getenv("IDC_CONFK")        
        if not conf_k:
            raise ValueError("IDC_CONFK not found!")
        cipher = Fernet(conf_k)
        addition_config = yaml.safe_load(cipher.decrypt(SERIAL_STRING))
        data.update(addition_config)
    except:
        print("Cannot load yaml config!!!")
        
    return data

# print(load_config())
