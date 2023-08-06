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

#ifndef DAISYKIT_MODELS_POSE_DETECTOR_H_
#define DAISYKIT_MODELS_POSE_DETECTOR_H_

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

/// Human pose estimation model.
class PoseDetector : public NCNNModel, public ImageModel {
 public:
  PoseDetector(const char* param_buffer, const unsigned char* weight_buffer,
               int input_width = 256, int input_height = 256,
               bool use_gpu = false);

  PoseDetector(const std::string& param_file, const std::string& weight_file,
               int input_width = 256, int input_height = 256,
               bool use_gpu = false);

#ifdef __ANDROID__
  PoseDetector(AAssetManager* mgr, const std::string& param_file,
               const std::string& weight_file, int input_width = 256,
               int input_height = 256, bool use_gpu = false);
#endif

  /// Detect single human pose.
  /// This function adds offset_x and offset_y to the keypoints.
  int Predict(const cv::Mat& image, std::vector<types::Keypoint>& keypoints,
              float offset_x = 0, float offset_y = 0);

  /// Detect multiple human poses.
  /// Return 0 on success, otherwise return the number of inference errors.
  int PredictMulti(const cv::Mat& image,
                   const std::vector<types::Object>& objects,
                   std::vector<std::vector<types::Keypoint>>& poses);

  /// Draw keypoints and their joints.
  void DrawKeypoints(cv::Mat& image,
                     const std::vector<types::Keypoint>& keypoints);

 private:
  /// Preprocess image data to obtain net input.
  void Preprocess(const cv::Mat& image, ncnn::Mat& net_input) override;
};

}  // namespace models
}  // namespace daisykit

#endif
