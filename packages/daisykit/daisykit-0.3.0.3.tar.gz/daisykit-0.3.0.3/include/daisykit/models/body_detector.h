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

#ifndef DAISYKIT_MODELS_BODY_DETECTOR_H_
#define DAISYKIT_MODELS_BODY_DETECTOR_H_

#include "daisykit/common/types.h"
#include "daisykit/models/image_model.h"
#include "daisykit/models/ncnn_model.h"

#include <opencv2/opencv.hpp>

#include <string>
#include <vector>

#ifdef __ANDROID__
#include <android/asset_manager_jni.h>
#endif

namespace daisykit {
namespace models {

/// Human body detection model.
class BodyDetector : public NCNNModel, public ImageModel {
 public:
  BodyDetector(const char* param_buffer, const unsigned char* weight_buffer,
               int input_width = 320, int input_height = 320,
               bool use_gpu = false);

  BodyDetector(const std::string& param_file, const std::string& weight_file,
               int width = 320, int height = 320, bool use_gpu = false);

#ifdef __ANDROID__
  BodyDetector(AAssetManager* mgr, const std::string& param_file,
               const std::string& weight_file, int width = 320,
               int height = 320, bool use_gpu = false);
#endif

  /// Detect human bodies.
  /// Return 0 on success, otherwise return error code.
  int Predict(const cv::Mat& image,
              std::vector<daisykit::types::Object>& objects);

 private:
  /// Preprocess image data to obtain net input.
  void Preprocess(const cv::Mat& image, ncnn::Mat& net_input) override;

  int input_width_;
  int input_height_;
};

}  // namespace models
}  // namespace daisykit

#endif
