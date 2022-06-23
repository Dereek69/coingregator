#!/usr/bin/env python3

from enum import Enum
from typing import Union
from fastapi import FastAPI, Query
from redis_manager import RedisManager


COINS_FILE = "/coin_list"
COINS = []
with open(COINS_FILE, "r") as file:
    COINS = {f.strip(): f.strip() for f in file.readlines()}
Coins = Enum("Coins", COINS)


class CoinglassOperation(str, Enum):
    funding_rates_u = "funding_rates_u"
    funding_rates_c = "funding_rates_c"


REDIS_URL = "redis://redis"
redis = RedisManager(REDIS_URL)

frontend = FastAPI()


@frontend.get("/coinglass/open_interest")
async def coinglass(coin: Union[Coins, None] = None):
    def response_editor(json_list: list):
        result = []
        for j in json_list:
            elaborated = {
                "symbol": j["symbol"],
            }
            for exch in j["data"]:
                if exch["exchangeName"] == "All":
                    elaborated["openInterest"] = exch["openInterest"]
                    elaborated["avgFundingRate"] = exch["avgFundingRate"]
                    elaborated["h24Change"] = exch["h24Change"]
                elif exch["exchangeName"] == "Binance":
                    elaborated["binanceOpenInterest"] = exch["openInterest"]
                elif exch["exchangeName"] == "FTX":
                    elaborated["ftxOpenInterest"] = exch["openInterest"]
            result.append(elaborated)
        return result

    if coin is None:
        return await redis.request("open_interest", COINS, response_editor)
    else:
        return await redis.request("open_interest", [coin.name], response_editor)


@frontend.get("/coinglass/{operation}")
async def coinglass(operation: CoinglassOperation, coin: Union[Coins, None] = None):
    def response_editor(json_list: list):
        result = []
        for j in json_list:
            result.append(j)
        return result

    if coin is None:
        return await redis.request(operation.name, COINS, response_editor)
    else:
        return await redis.request(operation.name, [coin.name], response_editor)


@frontend.get("/coingecko")
async def coingecko(page: Union[int, None] = Query(default=None, ge=1, le=6)):
    redis_key_prefix = "coingecko"

    def response_editor(json_list: list):
        result = []
        for j in json_list:
            result.extend(j)
        return result

    if page is None:
        return await redis.request(redis_key_prefix, [*range(1, 7)], response_editor)
    else:
        return await redis.request(redis_key_prefix, [page], response_editor)
