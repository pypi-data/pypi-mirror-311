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
from abc import abstractmethod
from typing import List, Optional, Dict
from pathlib import Path

import nlopt
import numpy as np
import pinocchio as pin
import torch

from opentv.motion.pinocchio_base import BaseOptimizer

class PinocchioVectorOptimizer(BaseOptimizer):
    def __init__(
        self,
        urdf_path,
        hand_indices,
        wrist_link_name,
        hand_config,
        huber_delta=0.02,
        norm_delta=4e-3,
    ):
        super().__init__(urdf_path, hand_indices, wrist_link_name, hand_config['out_lp_alpha'])
        self.origin_link_names = hand_config['target_origin_link_names']
        self.task_link_names = hand_config['target_task_link_names']
        self.target_link_human_indices = hand_config['target_link_human_indices']
        self.dex_pilot = hand_config.get('dex_pilot', None)
        self.huber_loss = torch.nn.SmoothL1Loss(beta=huber_delta, reduction="none")
        self.norm_delta = norm_delta
        self.scaling = hand_config['scaling_factor']

        # Computation cache for better performance
        # For one link used in multiple vectors, e.g. hand palm, we do not want to compute it multiple times
        self.computed_link_names = list(set(self.origin_link_names).union(set(self.task_link_names)))
        self.origin_link_indices = torch.tensor(
            [self.computed_link_names.index(name) for name in self.origin_link_names]
        )
        self.task_link_indices = torch.tensor([self.computed_link_names.index(name) for name in self.task_link_names])

        # Sanity check and cache link indices
        self.robot_link_indices = self.get_link_indices(self.computed_link_names)

        # Use local jacobian if target link name <= 2, otherwise first cache all jacobian and then get all
        # This is only for the speed but will not affect the performance
        if len(self.computed_link_names) <= 40:
            self.use_sparse_jacobian = True
        else:
            self.use_sparse_jacobian = False
        self.opt.set_ftol_abs(1e-6)

    def _get_objective_function(self, target_pos: np.ndarray, last_qpos: np.ndarray):
        # qpos = np.zeros(self.hand_dof)
        qpos = last_qpos

        # transform target pos to wrist frame
        target_pos = target_pos @ self.wrist_link_pose.rotation.T + self.wrist_link_pose.translation

        target_origin_pos = target_pos[self.target_link_human_indices[0], :]
        target_task_pos = target_pos[self.target_link_human_indices[1], :]
        target_vec = target_task_pos - target_origin_pos
        if isinstance(self.scaling, list):
            torch_target_vec = torch.as_tensor(target_vec) * torch.as_tensor(self.scaling).view(target_vec.shape[0], -1)
        else:
            torch_target_vec = torch.as_tensor(target_vec) * self.scaling
        torch_target_vec.requires_grad_(False)

        target_vec_dist = np.linalg.norm(target_vec, axis=1)
        proj_weights = np.ones(len(self.origin_link_indices), dtype=np.float32)

        # Dexpilot configuration
        if self.dex_pilot is not None:
            for i, temp in enumerate(self.dex_pilot):
                if temp is None:
                    pass
                cond_sign, cond_thres, proj_dist, proj_weight = temp
                conditioned = False
                if cond_sign == '<':
                    conditioned = target_vec_dist[i] < cond_thres
                elif cond_sign == '<=':
                    conditioned = target_vec_dist[i] <= cond_thres
                elif cond_sign == '==':
                    conditioned = target_vec_dist[i] == cond_thres
                elif cond_sign == '>=':
                    conditioned = target_vec_dist[i] >= cond_thres
                elif cond_sign == '>':
                    conditioned = target_vec_dist[i] > cond_thres
                elif cond_sign == '!=':
                    conditioned = target_vec_dist[i] != cond_thres
                if conditioned:
                    proj_weights[i] = float(proj_weight)
                    torch_target_vec[i] = float(proj_dist)

        proj_weights = torch.as_tensor(proj_weights)

        def objective(x: np.ndarray, grad: np.ndarray) -> float:
            qpos[:] = x
            pin.forwardKinematics(self.model, self.data, qpos)
            target_link_poses = [pin.updateFramePlacement(self.model, self.data, index)
                                 for index in self.robot_link_indices]
            body_pos = np.array([pose.translation for pose in target_link_poses])

            # Torch computation for accurate loss and grad
            torch_body_pos = torch.as_tensor(body_pos)
            torch_body_pos.requires_grad_()

            # Index link for computation
            origin_link_pos = torch_body_pos[self.origin_link_indices, :]
            task_link_pos = torch_body_pos[self.task_link_indices, :]
            robot_vec = task_link_pos - origin_link_pos

            # Loss term for kinematics retargeting based on 3D position error
            vec_dist = torch.norm(robot_vec - torch_target_vec, dim=1, keepdim=False)
            huber_distance = (self.huber_loss(vec_dist, torch.zeros_like(vec_dist)) * proj_weights).mean()
            result = huber_distance.cpu().detach().item()

            if grad.size > 0:
                if self.use_sparse_jacobian:
                    jacobians = []
                    for i, index in enumerate(self.robot_link_indices):
                        link_spatial_jacobian = pin.computeFrameJacobian(self.model, self.data, qpos, index).reshape((6, -1))[:3, :]
                        link_rot = pin.updateFramePlacement(self.model, self.data, index).rotation
                        link_kinematics_jacobian = link_rot @ link_spatial_jacobian
                        jacobians.append(link_kinematics_jacobian)
                    jacobians = np.stack(jacobians, axis=0)
                else:
                    raise ValueError('Full jacobian is not supported')

                if len(self.mimic_factors) != 0:
                    for i, m in enumerate(self.mimic_factors):
                        p_idx = self.parent_joint_indices[i]
                        c_idx = self.child_joint_indices[i]
                        jacobians[:, :, p_idx] = jacobians[:, :, p_idx] + m * jacobians[:, :, c_idx]
                        jacobians[:, :, c_idx] = 0

                huber_distance.backward()
                grad_pos = torch_body_pos.grad.cpu().numpy()[:, None, :]
                grad_qpos = np.matmul(grad_pos, np.array(jacobians))
                grad_qpos = grad_qpos.mean(1).sum(0)

                grad_qpos += 2 * self.norm_delta * (x - last_qpos)

                grad[:] = grad_qpos[:]
                if len(self.mimic_factors) != 0:
                    grad[self.child_joint_indices] = self.mimic_factors * grad[self.parent_joint_indices]

            return result

        return objective

    def retarget(self, ref_value, last_qpos=None):
        if last_qpos is None:
            last_qpos = np.zeros(self.dof)
        objective_fn = self._get_objective_function(ref_value, np.array(last_qpos).astype(np.float32))
        return self.optimize(objective_fn, last_qpos)