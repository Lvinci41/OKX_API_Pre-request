import base64
import datetime as dt
import hmac
import requests

pk = open("pk.txt","r")
keys = pk.readlines()
APIKEY = keys[0].strip()
APISECRET = keys[1].strip()
PASS = keys[2].strip()
BASE_URL = 'https://www.okx.com'

def send_signed_request(http_method, url_path, payload={}):

    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3]+'Z'
    
    def signature(timestamp, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)
    
    # set request header
    def get_header(request='GET', endpoint='', body:dict=dict()):
        cur_time = get_time()
        header = dict()
        header['CONTENT-TYPE'] = 'application/json'
        header['OK-ACCESS-KEY'] = APIKEY
        header['OK-ACCESS-SIGN'] = signature(cur_time, request, endpoint , body, APISECRET)
        header['OK-ACCESS-TIMESTAMP'] = str(cur_time)
        header['OK-ACCESS-PASSPHRASE'] = PASS
        return header

    url = BASE_URL + url_path
    header = get_header(http_method, url_path, payload)
    print(url)
    print(header)
    response = requests.get(url, headers=header)
    response.json()
    return response.json()

result = send_signed_request("GET", "/api/v5/account/balance", payload={})
print(result)
