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
from pathlib import Path
from threading import Lock
from typing import List, Optional, Dict

import numpy as np
import pinocchio as pin
import hppfcl
import yaml

from opentv.motion.pinocchio_base import BaseControl

from scipy.spatial.transform import Rotation as R


# def load_convex_mesh(file_name: str):
#     loader = hppfcl.MeshLoader()
#     bvh: hppfcl.BVHModelBase = loader.load(file_name)
#     bvh.buildConvexHull(True, "Qt")
#     return bvh.convex


class PinocchioMotionControl(BaseControl):
    def __init__(
        self,
        urdf_path,
        arm_indices,
        wrist_name,
        arm_config,
    ):
        super().__init__(urdf_path, arm_indices, wrist_name, arm_config['out_lp_alpha'])
        self.scaling_factor = float(arm_config['scaling_factor'])
        self.base_damping = float(arm_config['base_damping'])
        self.max_damping = float(arm_config['max_damping'])
        self.ik_eps = float(arm_config['eps'])
        self.dt = float(arm_config['dt'])

        # create collision shapes
        # if self.collision:
        #     self.left_finger_ids = [frame_mapping[name] for name in left_fingers]
        #     self.right_finger_ids = [frame_mapping[name] for name in right_fingers]
        #     self.left_finger_shapes = []
        #     self.right_finger_shapes = []
        #     for mesh_name in left_finger_meshes:
        #         finger_mesh_path = Path(mesh_path) / mesh_name
        #         self.left_finger_shapes.append(load_convex_mesh(str(finger_mesh_path)))
        #     for mesh_name in right_finger_meshes:
        #         finger_mesh_path = Path(mesh_path) / mesh_name
        #         self.right_finger_shapes.append(load_convex_mesh(str(finger_mesh_path)))
        #     self.table_shape = hppfcl.Box(0.8, 0.8, 0.12)
        #     self.table_T = hppfcl.Transform3f()
        #     self.table_T.setTranslation(np.array([0.8, 0, 0.1]))
        #     self.table_T.setRotation(pin.SE3.Identity().rotation)

    def control(self, target_pos, target_rot, n_trial=1):

        target_pos[:2] = target_pos[:2] * self.scaling_factor
        self.oMdes = pin.SE3(target_rot, target_pos)
        qpos = self.qpos.copy()

        ik_qpos = qpos.copy()
        err = float('inf')
        for i in range(n_trial):
            ik_qpos, ik_err = self.ik_clik(ik_qpos, self.oMdes, self.wrist_id, len(self.arm_indices) >= 6)
            if ik_err < err:
                err = ik_err
                qpos = ik_qpos.copy()
            if ik_err < self.ik_eps:
                break
            random_config = np.random.uniform(self.lower_limit, self.upper_limit)
            ik_qpos = random_config

        qpos = np.clip(qpos, self.lower_limit, self.upper_limit)
        self.qpos = pin.interpolate(self.model, self.qpos, qpos, self.alpha)

        return self.qpos.copy()

    def ik_clik(self, qpos, oMdes, wrist_id, full_ik=True, iter=100):
        prev_qpos = qpos.copy()
        for k in range(iter):
            pin.forwardKinematics(self.model, self.data, qpos)
            wrist_pose = pin.updateFramePlacement(self.model, self.data, wrist_id)
            iMd = wrist_pose.actInv(oMdes)
            err = pin.log(iMd).vector
            # degraded ik if arm dof < 6
            # if not full_ik:
            #     err[3:5] = 0
            if np.linalg.norm(err) < self.ik_eps:
                break

            J = pin.computeFrameJacobian(self.model, self.data, qpos, wrist_id)
            J = -np.dot(pin.Jlog6(iMd.inverse()), J)

            W = ((0.5 * err.T @ err) + self.base_damping) * np.eye(self.arm_dof)
            H = J.T @ J + W
            g = J.T @ err
            v = -np.linalg.solve(H, g)

            v_min = 0.5 * (self.lower_limit - qpos) / self.dt
            v_max = 0.5 * (self.upper_limit - qpos) / self.dt
            v = np.clip(v, v_min, v_max)

            # try:
            #     cond = np.linalg.cond(J)
            # except np.linalg.LinAlgError:
            #     cond = np.inf
            #
            # if cond > 100:
            #     damping = min(self.base_damping * (cond / 100), self.max_damping)
            # else:
            #     damping = self.base_damping

            # # Nullspace
            # JJT = J @ J.T
            # pinvJ = J.T @ np.linalg.inv(JJT + damping * np.eye(6))
            #
            # Nj = np.eye(len(qpos)) - pinvJ @ J
            #
            # Jp =J[:3, :]
            # # pinvJp = Jp.T @ np.linalg.inv(Jp @ Jp.T + damping * np.eye(3))
            # pinvJp = np.linalg.inv(Jp.T @ Jp + damping * np.eye(self.arm_dof)) @ Jp.T
            #
            # Np = np.eye(len(qpos)) - pinvJp @ Jp
            #
            # vp = pinvJp @ err[:3]
            #
            # Jo = J[3:, :]
            # JoNp = Jo @ Np
            #
            # # vo = JoNp.T @ np.linalg.solve(JoNp @ JoNp.T + damping * np.eye(3), err[3:] - Jo @ vp)
            # vo = np.linalg.solve(JoNp.T @ JoNp)
            #
            # v = vp + Np @ vo
            #
            # manipulability = np.linalg.det(JJT + 1e-10 * np.eye(6))
            # if manipulability < 1e-5:
            #     vs = 0.001 * (self.mid_range - qpos) * np.log(1e-5 / manipulability)
            #     v = v + Nj @ vs

            qpos = pin.integrate(self.model, qpos, v * self.dt)
            # qpos = np.clip(qpos, self.lower_limit, self.upper_limit)

        pin.forwardKinematics(self.model, self.data, qpos)
        wrist_pose = pin.updateFramePlacement(self.model, self.data, wrist_id)
        iMd = wrist_pose.actInv(oMdes)
        err = pin.log(iMd).vector

        return qpos, np.linalg.norm(err)

    # def check_collision(self, qpos):
    #     left_collision = False
    #     right_collision = False
    #
    #     pin.forwardKinematics(self.model, self.data, qpos)
    #
    #     col_req = hppfcl.CollisionRequest()
    #     col_res = hppfcl.CollisionResult()
    #
    #     # check left finger contacts with table
    #     for left_finger_id, left_finger_shape in zip(self.left_finger_ids, self.left_finger_shapes):
    #         left_finger_pose = pin.updateFramePlacement(self.model, self.data, left_finger_id)
    #         hppfcl.collide(self.table_shape, self.table_T, left_finger_shape, left_finger_pose, col_req, col_res)
    #         if col_res.isCollision():
    #             left_collision = True
    #
    #     # check right finger contact with table
    #     for right_finger_id, right_finger_shape in zip(self.right_finger_ids, self.right_finger_shapes):
    #         right_finger_pose = pin.updateFramePlacement(self.model, self.data, right_finger_id)
    #         hppfcl.collide(self.table_shape, self.table_T, right_finger_shape, right_finger_pose, col_req, col_res)
    #         if col_res.isCollision():
    #             right_collision = True
    #     return left_collision, right_collision

    def compute_err(self, arm_state):
        # print('qpos:', self.qpos)
        # print('state:', arm_state)
        err = np.zeros(6)
        pin.forwardKinematics(self.model, self.data, arm_state)
        wrist_pose = pin.updateFramePlacement(self.model, self.data, self.wrist_id)
        iMd = wrist_pose.actInv(self.oMdes)
        err[0:3] = iMd.translation
        err[3:6] = R.from_matrix(iMd.rotation).as_euler('xyz', degrees=False)
        # import ipdb; ipdb.set_trace()
        # err = pin.log(iMd).vector
        return np.array(err)