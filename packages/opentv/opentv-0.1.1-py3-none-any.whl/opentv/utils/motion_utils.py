# Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the MIT License [see LICENSE for details].

from typing import Optional

import numpy as np
import pinocchio as pin
from pytransform3d import rotations


class LPFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.y = None
        self.is_init = False

    def next(self, x):
        if not self.is_init:
            self.y = x
            self.is_init = True
            return self.y.copy()
        self.y = self.y + self.alpha * (x - self.y)
        return self.y.copy()

    def reset(self):
        self.y = None
        self.is_init = False


class LPRotationFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.is_init = False

        self.y = None

    def next(self, x: np.ndarray):
        assert x.shape == (4,)

        # assuming dealing with w, x, y, z quaternions

        if not self.is_init:
            self.y = x
            self.is_init = True
            return self.y.copy()

        self.y = rotations.quaternion_slerp(self.y, x, self.alpha, shortest_path=True)
        return self.y.copy()

    def reset(self):
        self.y = None
        self.is_init = False


class LPSE3Filter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.is_init = False

        self.y = None

    def next(self, x):
        if not self.is_init:
            self.y = pin.SE3(x)
            self.is_init = True
            return np.array(self.y)

        self.y = pin.SE3.Interpolate(self.y, pin.SE3(x), self.alpha)
        return np.array(self.y)

    def reset(self):
        self.y = None
        self.is_init = False


class LPConstrainedSE3Filter:
    def __init__(self, alpha, dt=1/60):
        self.alpha = alpha
        self.dt = dt
        self.is_init = False

        self.prev_pos = None
        self.prev_vel = None

        self.max_vel = np.array([1e2, 1e2, 1e2, 1e2, 1e2, 1e2])
        self.max_acc = np.array([1e3, 1e3, 1e3, 1e3, 1e3, 1e3])

    def next(self, target):
        if not self.is_init:
            self.prev_pos = pin.SE3(target)
            self.prev_vel = np.zeros(6)
            self.prev_acc = np.zeros(6)
            self.is_init = True
            return np.array(self.prev_pos)

        ip_pos = pin.SE3.Interpolate(self.prev_pos, pin.SE3(target), self.alpha)
        ip_vel = pin.log(ip_pos.actInv(self.prev_pos)).vector / self.dt
        ip_acc = (ip_vel - self.prev_vel) / self.dt

        acc = np.clip(ip_acc, -self.max_acc, self.max_acc)
        vel = np.clip(self.prev_vel + acc * self.dt, -self.max_vel, self.max_vel)
        pos = self.prev_pos * (~pin.exp(vel * self.dt))  # Caution! * means matrix multiplication in pinocchio

        self.prev_pos = pos
        self.prev_vel = vel

        return np.array(self.prev_pos)

    def reset(self):
        self.y = None
        self.is_init = False


def mat_update(prev_mat, mat):
    if np.linalg.det(mat) == 0:
        return prev_mat
    else:
        return mat


def fast_mat_inv(mat):
    ret = np.eye(4)
    ret[:3, :3] = mat[:3, :3].T
    ret[:3, 3] = -mat[:3, :3].T @ mat[:3, 3]
    return ret
