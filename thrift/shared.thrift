
/**
 * This Thrift file can be included by other Thrift files that want to share
 * these definitions.
 */

namespace py shared
namespace go shared

struct SharedStruct {
  1: i32 key
  2: string value
}

service SharedService {
  SharedStruct getStruct(1: i32 key)
}
