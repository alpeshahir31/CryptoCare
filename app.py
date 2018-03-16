# -*- coding: utf-8 -*-
# -*- File: app.py -*-
# -*- Author: aB9 -*-
# -*- Date: 03/12 -*-

#######################
## Known bugs:
##1. Index Page should refresh with the latest values when we come from details page
####################

from flask import Flask, render_template
import requests
import ObjCryptoCurrency

app = Flask(__name__)

   

#From CryptoCurrency Object
CrCurrency = ObjCryptoCurrency.CryptoCurrency
CrCurrencyDetails = ObjCryptoCurrency.CryptoCurrencyDetails
crc_list  = ObjCryptoCurrency.cryptocurrencies_list

#List to store CryptoCurrency data fetched from the server
cryptocurrencies_data =[]


#Index.html page
@app.route("/")
def index():
    
    for currency in crc_list:
        #URL to get current price data
        URL = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(crc_list[currency])
        response = requests.get(URL)
        
        #Request successful
        if response.status_code == 200:
            json_response = response.json()
            #store data into cryptocurrency_data list
            if json_response['Response'] == 'Success':
                data = json_response['Data'][0]
                cryptocurrencies_data.append(CrCurrency(crc_list[currency], currency, data['time'],data['close'],data['high'],data['low'],data['open'],data['volumefrom'],data['volumeto']))
            else:
                return render_template('error_page.html')
        #Error occurred
        else:
            return render_template('error_page.html')
    
    return render_template('index.html', cryptocurrencies = cryptocurrencies_data)

#CryptoCurrency_in_details.html page
@app.route("/<cryptocurrency_asset_id>")
def cryptocurrency_in_details(cryptocurrency_asset_id):
    currency = CrCurrency()
    currency_details = CrCurrencyDetails()
    currency_name = ""
    for c_name, c_id in crc_list.items():
        if c_id== cryptocurrency_asset_id:
            currency_name  = c_name 
    
    #URL to get cryptocurrency data in detail
    URL = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(cryptocurrency_asset_id)
    response = requests.get(URL)
    
        
    #Request successful
    if response.status_code == 200:
        json_response = response.json()
        #store data into cryptocurrency_data list
        if json_response['Response'] == 'Success':
            data = json_response['Data'][0]
            currency = CrCurrency(cryptocurrency_asset_id, currency_name, data['time'],data['close'],data['high'],data['low'],data['open'],data['volumefrom'],data['volumeto'])
            
        else:
            return render_template('error_page.html')
    #Error occurred
    else:
        return render_template('error_page.html')
    
    
    #URL to get cryptocurrency data in detail
    URL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(cryptocurrency_asset_id)
    response = requests.get(URL)
        
    #Request successful
    if response.status_code == 200:
        json_response = response.json()
        values_dict = json_response["RAW"][""+cryptocurrency_asset_id]["USD"]    
        display_values_dict = json_response["DISPLAY"][""+cryptocurrency_asset_id]["USD"]
        
        currency_details= CrCurrencyDetails(values_dict,display_values_dict)
        
    #Error occurred
    else:
        return render_template('error_page.html')
    
    return render_template('cryptocurrency_in_details.html',currency = currency,currency_details = currency_details)


if __name__ == "__main__":
    app.run()