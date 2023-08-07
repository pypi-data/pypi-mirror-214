import json
import requests
import os

config_file = 'config.json'
required_fields = ['tokenid', 'apikey', 'service']

class ConfigurationFileError(Exception):
    pass

class CollectPayment:
    @staticmethod
    def initialize(amount, custom_data):
        if not os.path.exists(config_file):
            raise ConfigurationFileError("Le fichier 'config.json' de configuration est manquant. Consulter la documentation afin d'obtenir ce fichier.")

        with open(config_file, 'r') as f:
            config = json.load(f)

        for field in required_fields:
            if field not in config:
                raise ConfigurationFileError(f"Le champ '{field}' est manquant dans le fichier de configuration.")

        url = "https://kaliapay.com/api/generate-mobpay-qrcode/"
        data = {
            "apikey": config['apikey'],
            "service": config['service'],
            "amount": amount,
            "custom_data": custom_data
        }
        headers = {"Authorization": f"Token {config['tokenid']}"}

        try:
            req = requests.post(url, data=data, headers=headers)
            req.raise_for_status()  # Gère les exceptions en cas de code d'erreur HTTP
            result = req.json()
        except requests.exceptions.RequestException as e:
            result = {"code": 00, "response": str(e)}
        
        return result

    @staticmethod
    def get_transaction_status(reference):
        if not os.path.exists(config_file):
            raise ConfigurationFileError("Le fichier 'config.json' de configuration est manquant. Consulter la documentation afin d'obtenir ce fichier.")

        with open(config_file, 'r') as f:
            config = json.load(f)

        for field in required_fields:
            if field not in config:
                raise ConfigurationFileError(f"Le champ '{field}' est manquant dans le fichier de configuration.")

        url = f"https://kaliapay.com/api/get-express-transaction-details/{reference}/"
        headers = {"Authorization": f"Token {config['tokenid']}"}

        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()  # Gère les exceptions en cas de code d'erreur HTTP
            result = req.json()
        except requests.exceptions.RequestException as e:
            result = {"code": 00, "response": str(e)}
        
        return result
