import time
import json
from typing import List
from web3 import Web3
from web3.types import HexStr
import msgspec
from thrift.TSerialization import serialize, deserialize
from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory, TBinaryProtocolAcceleratedFactory
from thrift.protocol.TJSONProtocol import TJSONProtocolFactory
from thrift.protocol.TCompactProtocol import TCompactProtocolFactory, TCompactProtocolAcceleratedFactory

from tx.ttypes import Transaction, TxType


PROVIDER = 'http://10.162.1.67:3335'

w3 = Web3(Web3.HTTPProvider(PROVIDER))


def benchmark(name):
    m = Transaction(
        sender='0x19Fb0AC09691b9c0F487A4435f0bD6E9E2F8bd7F',
        to='0xF872ADa8968c981cFb3769D58a03A3c018128B5a',
        value='8000000000000000',
        gas=180747,
        gasPrice='30630619010',
        maxFeePerGas='30630619010',
        maxPriorityFeePerGas='1000000000',
        data='0x3ddf078f000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000213e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        nonce=192,
        type=TxType.DynamicFee,
        accessList=[],
    )
    start = time.time()
    fac = TBinaryProtocolAcceleratedFactory()
    for i in range(3000000):
        result = serialize(m, protocol_factory=fac)
        t = Transaction()
        deserialize(t, result, protocol_factory=fac)
    print(name, time.time() - start)

# TBinaryProtocolFactory 220.84613394737244


if __name__ == '__main__':
    # txn = w3.eth.get_transaction(HexStr('0xec2eeab7026c70462bd1b9486d094a052163abfdc0d390bcd3a71566dc0c5d94'))
    # print(txn)
    benchmark("thrift")
