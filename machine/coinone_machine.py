import requests
import time
from machine.base_machine import Machine
import configparser
import base64
import json
import hashlib
import hmac


class CoinOneMachine(Machine):
    """
    코인원 거래소와 거래를 위한 클래스입니다.
    BASE_API_URL은 REST API호출의 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 코인원에서 거래가 가능한 화폐의 종류입니다.
    """
    BASE_API_URL = "https://api.coinone.co.kr"
    TRADE_CURRENCY_TYPE = ["btc", "eth", "etc", "bch", "qtum", "krw", "xrp", "iota", "ltc"]

    def __init__(self):
        """
        CoinOneMachine 클래스의 최초 호출 메소드입니다.
        config.ini에서 access_token, secret_key 정보를 읽어옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.access_token = config['COINONE']['access_token']
        self.secret_key = config['COINONE']['secret_key']

    def set_token(self, grant_type="refresh_token"):
        """인증토큰 정보를 만들기 위한 메소드입니다.

        Returns:
            만료시간(expire),인증토큰(access_token),리프레쉬토큰(refresh_token) 을 반환합니다.

        Raises:
            grant_type이 password나 refresh_token이 아닌 경우 Exception을 발생시킵니다.
        """
        token_api_path = "/oauth/refresh_token/"
        url_path = self.BASE_API_URL + token_api_path
        self.expire = 3600

        if grant_type == "refresh_token":
            headers = {"content-type": "application/x-www-form-urlencoded"}
            data = {"access_token": self.access_token}
            res = requests.post(url_path, headers=headers, data=data)
            result = res.json()
            if result["result"] == "success":
                config = configparser.ConfigParser()
                config.read('conf/config.ini')
                self.access_token = result["accessToken"]
                config["COINONE"]["access_token"] = self.access_token
                with open('conf/config.ini', 'w') as configfile:
                    config.write(configfile)
            else:
                raise Exception("Failed set_token")
        else:
            self.access_token = config['COINONE']['access_token']
        return self.expire, self.access_token, self.access_token

    def get_signature(self, encoded_payload, secret_key):
        """
        Args:
            encoded_payload(str): 인코딩된 payload 값입니다.
            secret_key(str): 서명할때 사용할 사용자의 secret_key 입니다.
        Returns:
            사용자의 secret_key로 서명된 데이터를 반환합니다.
        """
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512);
        return signature.hexdigest()

    def get_encoded_payload(self, payload):
        """
        Args:
            payload(str):인코딩할 payload

        Returns:
            인코딩된 payload값을 반환합니다 .
        """
        dumped_json = json.dumps(payload)
        return base64.b64encode(dumped_json.encode('utf-8'))

    def get_nonce(self):
        """Private API 호출 시 사용할 nonce값을 구하는 메소드입니다.

        Returns:
            nonce값을 반환합니다.
        """
        return int(time.time())

    def get_wallet_status(self):
        """사용자의 지갑정보를 조회하는 메소드입니다.

        Returns:
            사용자의 지갑에 화폐별 잔고를 딕셔너리 형태로 반환합니다.
        """
        time.sleep(1)
        wallet_status_api_path = "/v2/account/balance"
        url_path = self.BASE_API_URL + wallet_status_api_path
        payload = {
            "access_token": self.access_token,
            'nonce': self.get_nonce()
        }
        encoded_payload = self.get_encoded_payload(payload)
        signature = self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': signature}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        wallet_status = {currency: result[currency] for currency in self.TRADE_CURRENCY_TYPE}
        return wallet_status

    def buy_order(self, currency_type=None, price=None, qty=None, order_type="limit"):
        """매수 주문을 실행하는 메소드입니다..

        Note:
            화폐 종류마다 최소 주문 수량은 다를 수 있습니다.
            이 메소드는 지정가 거래만 지원합니다.

        Args:
            currency_type(str):화폐 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의되어있습니다.
            price(int): 1개 수량 주문에 해당하는 원화(krw) 값
            qty(float): 주문 수량입니다.

        Returns:
            주문의 상태에 대해 반환합니다.
        """
        if order_type != "limit":
            raise Exception("Coinone order type support only limit.")
        time.sleep(1)
        buy_limit_api_path = "/v2/order/limit_buy/"
        url_path = self.BASE_API_URL + buy_limit_api_path

        payload = {
            "access_token": self.access_token,
            "price": int(price),
            "qty": float(qty),
            "currency": currency_type,
            'nonce': self.get_nonce()
        }

        encoded_payload = self.get_encoded_payload(payload)
        signature = self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': signature}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result
