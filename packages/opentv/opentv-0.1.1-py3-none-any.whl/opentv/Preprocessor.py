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
import math
import numpy as np

from .constants.constants_avp import h1_head_mat, right_inspire2hand, left_inspire2hand
from .constants.constants_vuer import grd_yup2grd_zup, hand2inspire
from .utils.motion_utils import mat_update, fast_mat_inv

from pytransform3d import rotations


class AVPPreprocessor:
    def __init__(self):
        pass
    
    def process(self, data):
        # data = streamer.latest
        head_mat = np.array(data['head']).reshape(4, 4, order="F")
        right_wrist_mat = np.array(data['rightWrist']).reshape(4, 4, order="F")
        left_wrist_mat = np.array(data['leftWrist']).reshape(4, 4, order="F")

        # check data validity
        if (head_mat == np.eye(4)).all() or (right_wrist_mat == np.eye(4)).all() or (left_wrist_mat == np.eye(4)).all():
            return None
        
        head_mat = h1_head_mat @ head_mat

        rel_right_wrist_mat = right_wrist_mat @ right_inspire2hand  # wTr = wTh @ hTr
        # rel_right_wrist_mat = fast_mat_inv(head_mat) @ rel_right_wrist_mat  # hTr = (wTh)^-1 @ wTr
        rel_right_wrist_mat = h1_head_mat @ rel_right_wrist_mat  # sTr = sTc @ cTr; cTr = hTr

        rel_left_wrist_mat = left_wrist_mat @ left_inspire2hand
        # rel_left_wrist_mat = fast_mat_inv(head_mat) @ rel_left_wrist_mat
        rel_left_wrist_mat = h1_head_mat @ rel_left_wrist_mat

        rel_left_wrist_mat[0:3, 3] = rel_left_wrist_mat[0:3, 3] - head_mat[0:3, 3]
        rel_right_wrist_mat[0:3, 3] = rel_right_wrist_mat[0:3, 3] - head_mat[0:3, 3]

        right_fingers = np.array(data["rightSkeleton"]["joints"]).reshape(25, 4, 4)[:, 3, 0:3]
        rel_right_fingers = right_fingers @ right_inspire2hand[0:3, 0:3]

        left_fingers = np.array(data['leftSkeleton']["joints"]).reshape(25, 4, 4)[:, 3, 0:3]
        rel_left_fingers = left_fingers @ left_inspire2hand[0:3, 0:3]

        return head_mat, rel_left_wrist_mat, rel_right_wrist_mat, rel_left_fingers, rel_right_fingers

    def get_hand_gesture(self, streamer):
        data = streamer.latest
        left_fingers = data['left_fingers'][:, 0:3, 3] @ left_inspire2hand[0:3, 0:3]
        right_fingers = data["right_fingers"][:, 0:3, 3] @ right_inspire2hand[0:3, 0:3]
        all_fingers = np.concatenate([left_fingers, right_fingers], axis=0)
        return all_fingers


class VuerPreprocessor:
    def __init__(self):
        self.vuer_head_mat = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 1.5],
                                  [0, 0, 1, -0.2],
                                  [0, 0, 0, 1]])
        self.vuer_right_wrist_mat = np.array([[1, 0, 0, 0.5],
                                         [0, 1, 0, 1],
                                         [0, 0, 1, -0.5],
                                         [0, 0, 0, 1]])
        self.vuer_left_wrist_mat = np.array([[1, 0, 0, -0.5],
                                        [0, 1, 0, 1],
                                        [0, 0, 1, -0.5],
                                        [0, 0, 0, 1]])

    def process(self, tv):
        self.vuer_head_mat = mat_update(self.vuer_head_mat, tv.head_matrix.copy())
        self.vuer_right_wrist_mat = mat_update(self.vuer_right_wrist_mat, tv.right_hand.copy())
        self.vuer_left_wrist_mat = mat_update(self.vuer_left_wrist_mat, tv.left_hand.copy())

        # change of basis
        head_mat = grd_yup2grd_zup @ self.vuer_head_mat @ fast_mat_inv(grd_yup2grd_zup)
        right_wrist_mat = grd_yup2grd_zup @ self.vuer_right_wrist_mat @ fast_mat_inv(grd_yup2grd_zup)
        left_wrist_mat = grd_yup2grd_zup @ self.vuer_left_wrist_mat @ fast_mat_inv(grd_yup2grd_zup)

        rel_left_wrist_mat = left_wrist_mat @ hand2inspire
        rel_left_wrist_mat[0:3, 3] = rel_left_wrist_mat[0:3, 3] - head_mat[0:3, 3]
        # rel_left_wrist_mat = fast_mat_inv(head_mat) @ rel_left_wrist_mat

        rel_right_wrist_mat = right_wrist_mat @ hand2inspire  # wTr = wTh @ hTr
        rel_right_wrist_mat[0:3, 3] = rel_right_wrist_mat[0:3, 3] - head_mat[0:3, 3]
        # rel_right_wrist_mat = fast_mat_inv(head_mat) @ rel_right_wrist_mat  # hTr = (wTh)^-1 @ wTr

        # homogeneous
        left_fingers = np.concatenate([tv.left_landmarks.copy().T, np.ones((1, tv.left_landmarks.shape[0]))])
        right_fingers = np.concatenate([tv.right_landmarks.copy().T, np.ones((1, tv.right_landmarks.shape[0]))])

        # change of basis
        left_fingers = grd_yup2grd_zup @ left_fingers
        right_fingers = grd_yup2grd_zup @ right_fingers

        rel_left_fingers = fast_mat_inv(left_wrist_mat) @ left_fingers
        rel_right_fingers = fast_mat_inv(right_wrist_mat) @ right_fingers
        rel_left_fingers = (hand2inspire.T @ rel_left_fingers)[0:3, :].T
        rel_right_fingers = (hand2inspire.T @ rel_right_fingers)[0:3, :].T

        return head_mat, rel_left_wrist_mat, rel_right_wrist_mat, rel_left_fingers, rel_right_fingers

    def get_hand_gesture(self, tv):
        self.vuer_right_wrist_mat = mat_update(self.vuer_right_wrist_mat, tv.right_hand.copy())
        self.vuer_left_wrist_mat = mat_update(self.vuer_left_wrist_mat, tv.left_hand.copy())

        # change of basis
        right_wrist_mat = grd_yup2grd_zup @ self.vuer_right_wrist_mat @ fast_mat_inv(grd_yup2grd_zup)
        left_wrist_mat = grd_yup2grd_zup @ self.vuer_left_wrist_mat @ fast_mat_inv(grd_yup2grd_zup)

        left_fingers = np.concatenate([tv.left_landmarks.copy().T, np.ones((1, tv.left_landmarks.shape[0]))])
        right_fingers = np.concatenate([tv.right_landmarks.copy().T, np.ones((1, tv.right_landmarks.shape[0]))])

        # change of basis
        left_fingers = grd_yup2grd_zup @ left_fingers
        right_fingers = grd_yup2grd_zup @ right_fingers

        rel_left_fingers = fast_mat_inv(left_wrist_mat) @ left_fingers
        rel_right_fingers = fast_mat_inv(right_wrist_mat) @ right_fingers
        rel_left_fingers = (hand2inspire.T @ rel_left_fingers)[0:3, :].T
        rel_right_fingers = (hand2inspire.T @ rel_right_fingers)[0:3, :].T
        all_fingers = np.concatenate([rel_left_fingers, rel_right_fingers], axis=0)

        return all_fingers
    
    def sub_waist(self, head_mat, left_wrist_mat, right_wrist_mat, left_fingers, right_fingers, waist_angle=None):
        if waist_angle is None:
            return head_mat, left_wrist_mat, right_wrist_mat, left_fingers, right_fingers

        head_pos = head_mat[:3, 3].copy()

        waist_mat = np.eye(4)
        waist_mat[:3, :3] = rotations.matrix_from_axis_angle([0, 0, 1, waist_angle])

        head_mat[:3, :3] = waist_mat[:3, :3] @ head_mat[:3, :3]

        left_wrist_mat = waist_mat @ left_wrist_mat

        right_wrist_mat = waist_mat @ right_wrist_mat

        return head_mat, left_wrist_mat, right_wrist_mat, left_fingers, right_fingers
