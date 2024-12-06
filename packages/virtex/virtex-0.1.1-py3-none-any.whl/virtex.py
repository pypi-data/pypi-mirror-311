# /// script
# dependencies = [
#   "requests",
#   "python-dotenv",
#   "pandas",
#   "websocket-client",
# ]
# ///
import threading
import requests as req
import logging
import os
import websocket
import pandas as pd
import socket
import urllib.parse

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

BASE_URL = "http://{host}:{port}/{base_endpoint}{endpoint}"
BASE_ENDPOINT = ""
HOST = "localhost"
PORT = 4000
SIM_PORT = 4001


# TODO: Add error handling
def get(api_key, api_secret, host, port, base_endpoint, endpoint):
    url = f"{BASE_URL.format(host=host, port=port, base_endpoint=base_endpoint, endpoint=endpoint)}"
    log.info("GET - %s", url)
    response = req.get(url, headers={"X-API-KEY": api_key, "X-API-SECRET": api_secret})
    try:
        return response.json()
    except:
        log.info("%s - %s", response, response.text)
        return None


def post(api_key, api_secret, host, port, base_endpoint, endpoint, json):
    url = f"{BASE_URL.format(host=host, port=port, base_endpoint=base_endpoint, endpoint=endpoint)}"
    log.info("POST - %s", url)
    response = req.post(
        url, json=json, headers={"X-API-KEY": api_key, "X-API-SECRET": api_secret}
    )
    try:
        return response.json()
    except:
        log.info("%s - %s", response, response.text)
        return None


def patch(api_key, api_secret, host, port, base_endpoint, endpoint, json):
    url = f"{BASE_URL.format(host=host, port=port, base_endpoint=base_endpoint, endpoint=endpoint)}"
    log.info("PATCH - %s", url)
    response = req.patch(
        url, json=json, headers={"X-API-KEY": api_key, "X-API-SECRET": api_secret}
    )
    try:
        return response.json()
    except:
        log.info("%s - %s", response, response.text)
        return None


def delete(api_key, api_secret, host, port, base_endpoint, endpoint, json):
    url = f"{BASE_URL.format(host=host, port=port, base_endpoint=base_endpoint, endpoint=endpoint)}"
    log.info("DELETE - %s", url)
    response = req.delete(
        url, json=json, headers={"X-API-KEY": api_key, "X-API-SECRET": api_secret}
    )
    try:
        return response.json()
    except:
        log.info("%s - %s", response, response.text)
        return None


class Virtex:
    def __init__(
        self,
        api_key,
        api_secret,
        host=HOST,
        port=PORT,
        base_endpoint=BASE_ENDPOINT,
        sim_port=SIM_PORT,
    ):
        self.api_key = api_key
        self.api_secret = api_secret

        self.host = host
        self.port = port
        self.sim_port = sim_port
        self.base_endpoint = base_endpoint
        self.messages = []

    def get(self, endpoint, port=None):
        return get(
            self.api_key,
            self.api_secret,
            self.host,
            port or self.port,
            self.base_endpoint,
            endpoint,
        )

    def post(self, endpoint, json={}, host=None, port=None):
        return post(
            self.api_key,
            self.api_secret,
            host or self.host,
            port or self.port,
            self.base_endpoint,
            endpoint,
            json,
        )

    def patch(self, endpoint, json={}, host=None, port=None):
        return patch(
            self.api_key,
            self.api_secret,
            host or self.host,
            port or self.port,
            self.base_endpoint,
            endpoint,
            json,
        )

    def delete(self, endpoint, json={}, host=None, port=None):
        return delete(
            self.api_key,
            self.api_secret,
            host or self.host,
            port or self.port,
            self.base_endpoint,
            endpoint,
            json,
        )

    def ping(self):
        return self.get("ping")

    def me(self):
        return self.get("me")

    def entities(self, id=None, query=None):
        if id:
            return self.get(f"entities/{id}")
        if query:
            return self.get(f"entities?{query}")
        return self.get("entities")

    def entity_accounts(self, entity=None):
        if entity:
            return self.get(f"entities/{entity}/accounts")
        return self.get("accounts")

    def accounts(self, id=None):
        if id:
            return self.get(f"accounts/{id}")
        return self.get("accounts")

    def get_account(self, name, entity):
        return self.get(f"accounts?name={name}")

    def positions(self, account=None, asset=None):
        positions = []
        if account and asset:
            positions = self.get(f"accounts/{account}/positions/{asset}")
        elif account:
            positions = self.get(f"accounts/{account}/positions")
        elif asset:
            positions = self.get(f"positions/{asset}")
        else:
            positions = self.get("positions")
        return pd.DataFrame(positions)

    def orders(self, orderId=None, account=None, query=None):
        if orderId:
            return self.get(f"orders/{orderId}")

        orders = []
        if account:
            orders = self.get(f"accounts/{account}/orders")
        if query:
            orders = self.get(f"orders?{query}")
        else:
            orders = self.get("orders")
        return pd.DataFrame(orders)

    def get_token(self):
        return self.post("users/tokens")

    def new_order(
        self,
        msgType="D",
        side=None,
        symbol=None,
        quantity=None,
        price=None,
        exDestination="binance",
        target_strategy="DMA",
        account=1,
        order=None,
    ):
        if order:
            return self.post("orders", json=order)

        if side is None:
            raise TypeError("Missing Side")

        if symbol is None:
            raise TypeError("Missing Symbol")

        if quantity is None:
            raise TypeError("Missing Quantity")

        if price is None:
            raise TypeError("Missing Price")

        order = {"side": side, "symbol": symbol, "orderQty": quantity, "price": price}
        if exDestination:
            order["exDestination"] = exDestination
        if target_strategy:
            order["target_strategy"] = target_strategy
        if account:
            order["account"] = account

        return self.post("orders", json=order)

    def buy(
        self,
        symbol,
        quantity,
        price,
        exDestination="binance",
        target_strategy="DMA",
        account=1,
    ):
        return self.new_order(
            "BUY",
            symbol,
            quantity,
            price,
            exDestination=exDestination,
            target_strategy=target_strategy,
            account=account,
        )

    def sell(
        self,
        symbol,
        quantity,
        price,
        exDestination="binance",
        target_strategy="DMA",
        account=1,
    ):
        return self.new_order(
            "SELL",
            symbol,
            quantity,
            price,
            exDestination=exDestination,
            target_strategy=target_strategy,
            account=account,
        )

    def cancel(self, clOrdId):
        return self.delete(f"orders/{clOrdId}")

    def on_message(self, ws, message):
        log.info("IN: %s", message)
        self.messages.append(message)

    def get_messages(self):
        return pd.DataFrame(self.messages)

    def listen_ws(self, trace=False):
        websocket.enableTrace(trace)
        token = self.get_token()["token"]
        uri = f"ws://{self.host}:4000/websocket/{token}"
        ws = websocket.WebSocketApp(uri, on_message=self.on_message)
        ws.run_forever()  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly

    def listen(self, trace=False):
        t1 = threading.Thread(target=self.listen_ws, args=(trace,))
        t1.start()

    def instruments(self, query=None, symbol=None, venue=None, base=None, quote=None):
        query = {}
        if venue:
            query["venue"] = venue
        if base:
            query["base"] = base
        if quote:
            query["quote"] = quote
        if(symbol):
            query["symbol"] = symbol

        if(query != {}):
            url = f"instruments?{urllib.parse.urlencode(query)}"
            log.debug(f"Query: {url}")
            return self.get(url)
        return self.get("instruments")


def init(host=None):
    if host is None:
        host = os.getenv("VIRTEX_API_HOST", "localhost")
    return Virtex(os.getenv("VIRTEX_API_KEY"), os.getenv("VIRTEX_API_SECRET"), host)


if __name__ == "__main__":
    logging.basicConfig(encoding="utf-8", level=logging.INFO)
    instance = init('demo.virtex.co')
    instance.listen_ws()
