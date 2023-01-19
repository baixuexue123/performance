import time
from proto.tx_pb2 import Transaction


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
        type=2,
        accessList=[],
    )
    start = time.time()
    for i in range(3000000):
        s = m.SerializeToString()
        Transaction().ParseFromString(s)
    print(name, time.time() - start)


if __name__ == '__main__':
    from google.protobuf.internal import api_implementation
    print(api_implementation.Type())

    benchmark("protobuf")
