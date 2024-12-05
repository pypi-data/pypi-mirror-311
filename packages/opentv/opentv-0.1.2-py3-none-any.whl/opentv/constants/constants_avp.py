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
import numpy as np

right_inspire2hand = np.array([[0, 1, 0, 0],
                               [1, 0, 0, 0],
                               [0, 0, -1, 0],
                               [0, 0, 0, 1]])

left_inspire2hand = np.array([[0, -1, 0, 0],
                              [-1, 0, 0, 0],
                              [0, 0, -1, 0],
                              [0, 0, 0, 1]])

h1_head_mat = np.array([[0, 0, -1, 0],
                        [-1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]])
