
/**
 * The first thing to know about are types. The available types in Thrift are:
 *
 *  bool        Boolean, one byte
 *  i8 (byte)   Signed 8-bit integer
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 * Did you also notice that Thrift supports C style comments?
 */

namespace py tx
namespace go tx

typedef i32 MyInteger

const i32 INT32CONSTANT = 9853
const map<string,string> MAPCONSTANT = {'hello':'world', 'goodnight':'moon'}

enum TxType {
  Legacy = 0,
  AccessList = 1,
  DynamicFee = 2,
}

struct AccessTuple {
  1: string address,
  2: list<string> storageKeys,
}

struct Transaction {
  1: string sender,
  2: string to,
  3: string value,
  4: i64 gas,
  5: optional string gasPrice,
  6: optional string maxFeePerGas,
  7: optional string maxPriorityFeePerGas,
  8: i64 nonce,
  9: string data,
  10: list<AccessTuple> accessList,
  11: TxType type,
}

/*
 * thrift -gen py -out . tx.thrift
 */