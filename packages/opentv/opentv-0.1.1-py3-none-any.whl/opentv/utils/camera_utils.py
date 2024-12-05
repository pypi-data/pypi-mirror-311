"""
Copyright [2024] [Xuxin Cheng, Jialong Li]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import cv2
import numpy as np

class OpticalFlowStablizer:
    def __init__(self):
        self.prev_left_gray = None
        self.prev_right_gray = None
        self.is_init = False

    def next(self, left_bgr, right_bgr):
        cur_left_gray = cv2.cvtColor(left_bgr, cv2.COLOR_BGR2GRAY)
        cur_right_gray = cv2.cvtColor(right_bgr, cv2.COLOR_BGR2GRAY)
        if not self.is_init:
            self.prev_left_gray = cur_left_gray
            self.prev_right_gray = cur_right_gray
            self.is_init = True
            return left_bgr, right_bgr

        left_flow = cv2.calcOpticalFlowFarneback(self.prev_left_gray, cur_left_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        right_flow = cv2.calcOpticalFlowFarneback(self.prev_right_gray, cur_right_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        left_translation = np.mean(left_flow, axis=(0, 1))
        right_translation = np.mean(right_flow, axis=(0, 1))
        transforms = np.array([[1, 0, (left_translation[0] + right_translation[0]) / 2],
                                     [0, 1, (left_translation[1] + right_translation[1]) / 2]], dtype=np.float32)

        left_stablized = cv2.warpAffine(left_bgr, transforms, (left_bgr.shape[1], left_bgr.shape[0]))
        right_stablized = cv2.warpAffine(right_bgr, transforms, (right_bgr.shape[1], right_bgr.shape[0]))

        self.prev_left_gray = cur_left_gray
        self.prev_right_gray = cur_right_gray
        return left_stablized, right_stablized

    def reset(self):
        self.prev_left_gray = None
        self.prev_right_gray = None
        self.transforms = np.zeros((2, 3), dtype=np.float32)
        self.is_init = False