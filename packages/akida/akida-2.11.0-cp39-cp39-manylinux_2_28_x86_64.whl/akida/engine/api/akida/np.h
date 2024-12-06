#pragma once
#include <string>
#include <vector>

#include "hardware_ident.h"
#include "hardware_type.h"
#include "infra/system.h"

namespace akida::np {

constexpr bool is_cnp(hw::Type type) {
  return type == hw::Type::CNP1 || type == hw::Type::CNP2;
}

constexpr bool is_fnp(hw::Type type) {
  return type == hw::Type::FNP2 || type == hw::Type::FNP3;
}

struct Info {
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const Info& other) const {
    return ident == other.ident && types == other.types;
  }
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const Info& other) const { return !(*this == other); }
  hw::Ident ident;
  hw::Types types;
};

struct SkipDmaInfo : Info {
  explicit SkipDmaInfo(const hw::Ident& id, const uint8_t num_ch)
      : total_channels(num_ch) {
    if (id.row != 1 || id.id != 3) {
      const std::string err_msg =
          "Invalid Skip DMA ID: Expected row = 1 and id = 3, but received row "
          "= " +
          std::to_string(id.row) + " and id = " + std::to_string(id.id);
      panic(err_msg.c_str());
    }
    ident = id;
    types = {hw::Type::SKIP_DMA};
  }
  SkipDmaInfo(const SkipDmaInfo&) = default;
  SkipDmaInfo(SkipDmaInfo&&) noexcept = default;
  SkipDmaInfo& operator=(const SkipDmaInfo&) = delete;
  SkipDmaInfo& operator=(SkipDmaInfo&&) noexcept = delete;
  ~SkipDmaInfo() = default;
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const SkipDmaInfo& other) const {
    return Info::operator==(other) && channel_idx == other.channel_idx;
  }
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const SkipDmaInfo& other) const { return !(*this == other); }
  // number of channels in skipdma
  const uint8_t total_channels;
  // channel id being used
  uint8_t channel_idx{};
};

/**
 * The layout of a mesh of Neural Processors
 */
struct Mesh final {
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const Mesh& other) const {
    return dma_event == other.dma_event && dma_conf == other.dma_conf &&
           nps == other.nps && skip_dmas == other.skip_dmas;
  }
  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const Mesh& other) const { return !(*this == other); }

  hw::Ident dma_event{};                /**<The DMA event endpoint */
  hw::Ident dma_conf{};                 /**<The DMA configuration endpoint */
  std::vector<Info> nps{};              /**<The available Neural Processors */
  std::vector<SkipDmaInfo> skip_dmas{}; /**<The available skip dmas */
};

}  // namespace akida::np
