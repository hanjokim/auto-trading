import requests
import time
import math
from machine.base_machine import Machine
import configparser
import json
import base64
import hashlib
import hmac
import urllib

class BithumbMachine(Machine):
    """
    빗썸 거래소와 거래를 위한 클래스입니다.
    BASE_API_URL은 REST API호출의 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 빗썸에서 거래가 가능한 화폐의 종류입니다.
    """
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM", "BTG", "EOS"]
    def __init__(self):
        """
        BithumbMachine 클래스의 최초 호출 메소드 입니다.
        config.ini파일에서 connect_key, secret_key, username을 읽어옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.CLIENT_ID = config['BITHUMB']['connect_key']
        self.CLIENT_SECRET = config['BITHUMB']['secret_key']
        #self.USER_NAME = config['BITHUMB']['username']
        #self.access_token = None
        #self.refresh_token = None
        #self.token_type = None

    def get_ticker(self, currency_type=None):
        """마지막 체결정보(Tick)을 얻기 위한 메소드입니다.

        Args:
            currency_type(str):화폐 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어있습니다.

        Returns:
            결과를 딕셔너리로 반환합니다.
            결과의 필드는 timestamp, last, bid, ask, high, low, volume이 있습니다.
        """
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        ticker_api_path = "/public/ticker/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path)
        response_json = res.json()
        result = {}
        result["timestamp"] = str(response_json['data']["date"])
        result["last"] = response_json['data']["closing_price"]
        result["bid"] = response_json['data']["buy_price"]
        result["ask"] = response_json['data']["sell_price"]
        result["high"] = response_json['data']["max_price"]
        result["low"] = response_json['data']["min_price"]
        result["volume"] = response_json['data']["volume_1day"]
        return result

    def get_filled_orders(self, currency_type=None):
        """체결정보를 얻어오기 위한 메소드입니다.

        Note:
            가장 최근 100개만 받을 수 있습니다.

        Args:
            currency_type(str):화폐 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어있습니다.

        Returns:
           가장 최근 체결정보를 딕셔너리의 리스트 형태로 반환합니다.
        """
        if currency_type is None:
            raise Exception("Need to currency_type")
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        time.sleep(1)
        params = {'offset': 0, 'count': 100}
        orders_api_path = "/public/transaction_history/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path, params=params)
        result = res.json()
        return result
