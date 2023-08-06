// Copyright 2021 The DaisyKit Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef DAISYKIT_COMMON_TYPES_FACE_H_
#define DAISYKIT_COMMON_TYPES_FACE_H_

#include "daisykit/common/types/box.h"
#include "daisykit/common/types/keypoint.h"

#include <vector>

namespace daisykit {
namespace types {

/// Human face data type.
/// Also includes other information such as wearing mask or not, facial landmark
class Face : public Box {
 public:
  float confidence = 1.0;                 /// Confidence of face
  float wearing_mask_prob = -1;           /// Probability of wearing a mask
  std::vector<types::Keypoint> landmark;  /// Keypoints

  float Area() const { return w * h; }
};

}  // namespace types
}  // namespace daisykit

#endif
