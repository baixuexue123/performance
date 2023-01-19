# serialize

## protobuf-python

pip install protobuf 安装的是pure python版的

cpp扩展版的需要自己编译

先按照 这个编译 cpp版本的 https://github.com/protocolbuffers/protobuf/blob/v21.12/src/README.md

> 注意 要make install 安装libprotobuf.so

然后build python版的

```shell
python setup.py build --cpp_implementation
# or
python setup.py install --cpp_implementation

# 打包wheel
python setup.py bdist_wheel --cpp_implementation
```

## upb

https://github.com/protocolbuffers/upb

pip install 安装 >= 4 版本 已经集成了upb c扩展 (自测：速度是pure-python版的30倍， 是自己编译 c++版本的 3倍)

