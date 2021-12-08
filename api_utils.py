import requests
import json
import globals as Globals
import crypto_utils as CryptoUtils

public_url = "https://api.crypto.com/v2/public/"
private_url = "https://api.crypto.com/v2/private/"
headers = { 'Content-type': 'applicatoin/json'}

def createAPIRequest(requestType, url):
    req = None
    if requestType.upper() == "GET":
        req = requests.get(url)
    elif requestType.upper() == "PUT":
        req = requests.put(url)
    elif requestType.upper() == "POST":
        req = requests.post(url)
    elif requestType.upper() == "DELETE":
        req = requests.delete(url)
    return req

def publicAPICall(requestType, methodName, params = []):
    final_url = public_url + methodName
    if params:
        final_url += "?" + params
    req = createAPIRequest(requestType, final_url)
    return req

def privateAPICall(methodName, params = [], requestType="GET"):
    req = CryptoUtils.generateSignature(methodName, params)
    return req

def getBuySellPrice(instrumentName):
    response = publicAPICall("GET","get-trades", f"instrument_name={instrumentName}")
    if response and response.content:
        object = json.loads(response.content)
        result = object['result']
        instrument_name = result['instrument_name']
        data = result['data']
        price_average = 0
        for d in data:
            price_average += float(d['p'])
        if(len(data)>0):
            price_average /= len(data)
        sell_price = (price_average*(1.0-Globals.TRADE_TAX))
        buy_price = (price_average*(1.0+Globals.TRADE_TAX))
        return { "average":price_average, "buy":buy_price, "sell":sell_price }

def getAllInstrumentNames(quoteCurrency=""):
    url = publicAPICall("GET","get-instruments")
    req = requests.get(url)
    if req.status_code == 200:
        object = json.loads(req.content)
        data = object["result"]["instruments"]
        instruments_array = []
        for d in data:
            if quoteCurrency == "" or d["quote_currency"] == quoteCurrency:
                instruments_array.append(d["instrument_name"])
        return instruments_array
    return []
