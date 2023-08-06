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

#ifndef DAISYKIT_COMMON_TYPES_FACE_EXTENDED_H_
#define DAISYKIT_COMMON_TYPES_FACE_EXTENDED_H_
#include "daisykit/common/types/face.h"

#include <opencv2/opencv.hpp>

#include <vector>

namespace daisykit {
namespace types {

/// Extended face object with aligned face and feature vector.
/// This is used for face recognition.
class FaceExtended : public Face {
 public:
  float liveness_score;

  cv::Mat aligned_face;  /// Aligned face. For increasing recognition accuracy,
                         /// the face should be aligned before recognition.
  std::vector<float> feature;  /// Feature vector for face recognition
};

}  // namespace types
}  // namespace daisykit

#endif
