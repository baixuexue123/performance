import time
import json
import orjson
import cysimdjson
import simdjson
import msgspec
from typing import List, Optional


class Transaction(msgspec.Struct):
    sender: str
    to: str
    value: str
    gas: int
    data: str
    nonce: int
    type: int
    accessList: List
    gasPrice:  Optional[str] = None
    maxFeePerGas: Optional[str] = None
    maxPriorityFeePerGas:  Optional[str] = None


m = dict(
    sender='0x19Fb0AC09691b9c0F487A4435f0bD6E9E2F8bd7F',
    to='0xF872ADa8968c981cFb3769D58a03A3c018128B5a',
    value='8000000000000000',
    gas=180747,
    gasPrice='30630619010',
    maxFeePerGas='30630619010',
    maxPriorityFeePerGas='1000000000',
    data='0x3ddf078f000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000213e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    nonce=192,
    type=2,
    accessList=[],
)


def test(name):
    a = Transaction(**m)
    start = time.time()
    dec = msgspec.json.Decoder(Transaction)
    for i in range(3000000):
        msg = msgspec.json.encode(a)
        dec.decode(msg)
    print(name, time.time() - start)


def benchmark(name, dumps, loads):
    start = time.time()
    for i in range(3000000):
        result = dumps(m)
        loads(result)
    print(name, time.time() - start)


if __name__ == "__main__":

    parser1 = cysimdjson.JSONParser()
    parser2 = simdjson.Parser()

    test("msgspec.struct")
    benchmark("msgspec", msgspec.json.encode, msgspec.json.decode)
    benchmark("cysimdjson", json.dumps, parser1.parse_string)
    benchmark("simdjson", json.dumps, parser2.parse)
    benchmark("orjson", lambda s: str(orjson.dumps(s), "utf-8"), orjson.loads)
    benchmark("Python", json.dumps, json.loads)
    # orjson only outputs bytes, but often we need unicode:

# python3.10
# cysimdjson 18.088396072387695
# simdjson 17.81083393096924
# orjson 5.00632119178772
# Python 31.241437911987305