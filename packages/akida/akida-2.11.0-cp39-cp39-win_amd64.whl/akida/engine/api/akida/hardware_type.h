#pragma once

#include <set>

namespace akida::hw {

enum class BasicType { none, HRC, CNP, FNP, VIT_BLOCK, SKIP_DMA, TNP_B, TNP_R };
enum class Type {
  none,
  HRC,
  CNP1,
  CNP2,
  FNP2,
  FNP3,
  VIT_BLOCK,
  // TODO: skipdmas types will be split into SKIP_DMA_STORE and SKIP_DMA_LOAD
  SKIP_DMA,
  TNP_B,
  TNP_R
};
using Types = std::set<Type>;

}  // namespace akida::hw