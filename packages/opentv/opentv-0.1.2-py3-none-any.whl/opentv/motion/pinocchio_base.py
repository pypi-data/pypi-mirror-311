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

# import casadi
import nlopt
import numpy as np
import pinocchio as pin
# import pinocchio.casadi as cpin


class BaseControl:

    def __init__(
        self,
        urdf_path,
        arm_indices,
        wrist_name,
        alpha,
    ):
        self.arm_indices = arm_indices
        self.alpha = float(alpha)

        self.model = pin.buildModelFromUrdf(str(urdf_path))
        self.dof = self.model.nq

        # lock joints
        locked_joint_ids = list(set(range(self.dof)) - set(self.arm_indices))
        locked_joint_ids = [id + 1 for id in locked_joint_ids]  # account for universe joint
        self.model = pin.buildReducedModel(self.model, locked_joint_ids, np.zeros(self.dof))
        self.arm_dof = self.model.nq

        self.lower_limit = self.model.lowerPositionLimit
        self.upper_limit = self.model.upperPositionLimit
        self.mid_range = (self.upper_limit + self.lower_limit) / 2
        self.data: pin.Data = self.model.createData()

        self.wrist_id = self.model.getFrameId(wrist_name)

        # Current state
        self.qpos = pin.neutral(self.model)
        pin.forwardKinematics(self.model, self.data, self.qpos)
        self.wrist_pose: pin.SE3 = pin.updateFramePlacement(
            self.model, self.data, self.wrist_id
        )

    def get_current_qpos(self):
        return self.qpos.copy()

    def set_current_qpos(self, qpos):
        self.qpos = qpos.copy()

    def get_joint_names(self):
        # Pinocchio by default add a dummy joint name called "universe"
        names = list(self.model.names)
        return names[1:]

    @abstractmethod
    def control(self, target_pos, target_rot):
        pass


# class BaseControlCasadi:
#     def __init__(
#         self,
#         urdf_path,
#         arm_indices,
#         wrist_name,
#         alpha,
#     ):
#         self.arm_indices = arm_indices
#         self.alpha = float(alpha)

#         self.model = pin.buildModelFromUrdf(str(urdf_path))
#         self.dof = self.model.nq

#         # lock joints
#         locked_joint_ids = list(set(range(self.dof)) - set(self.arm_indices))
#         locked_joint_ids = [id + 1 for id in locked_joint_ids]  # account for universe joint
#         self.model = pin.buildReducedModel(self.model, locked_joint_ids, np.zeros(self.dof))
#         self.arm_dof = self.model.nq

#         self.lower_limit = self.model.lowerPositionLimit
#         self.upper_limit = self.model.upperPositionLimit
#         self.mid_range = (self.upper_limit + self.lower_limit) / 2
#         self.data: pin.Data = self.model.createData()

#         self.wrist_id = self.model.getFrameId(wrist_name)

#         # Current state
#         self.qpos = pin.neutral(self.model)
#         pin.forwardKinematics(self.model, self.data, self.qpos)
#         self.wrist_pose: pin.SE3 = pin.updateFramePlacement(
#             self.model, self.data, self.wrist_id
#         )
#         self.init_data = np.array(self.qpos)

#         # Creating Casadi models and data for symbolic computing
#         self.cmodel = cpin.Model(self.model)
#         self.cdata = self.cmodel.createData()

#         # Creating symbolic variables
#         self.cq = casadi.SX.sym("q", self.arm_dof, 1) 
#         self.cTf = casadi.SX.sym("tf_l", 4, 4)
#         cpin.framesForwardKinematics(self.cmodel, self.cdata, self.cq)

#         # Define the error function
#         self.error = casadi.Function(
#             "error",
#             [self.cq, self.cTf],
#             [
#                 cpin.log6(
#                     self.cdata.oMf[self.wrist_id].inverse() * cpin.SE3(self.cTf)
#                 ).vector,
#             ],
#         )

#         # Defining the optimization problem
#         self.opti = casadi.Opti()
#         self.var_q = self.opti.variable(self.arm_dof)
#         self.param_q_ik_last = self.opti.parameter(self.arm_dof)
#         self.param_tf = self.opti.parameter(4, 4)
#         self.totalcost = casadi.sumsqr(self.error(self.var_q, self.param_tf))
#         self.regularization = casadi.sumsqr(self.var_q)
#         self.smooth_cost = casadi.sumsqr(self.var_q - self.param_q_ik_last)

#         self.opti.set_value(self.param_q_ik_last, self.init_data)

#         # Setting optimization constraints and goals
#         self.opti.subject_to(self.opti.bounded(
#             self.lower_limit,
#             self.var_q,
#             self.upper_limit)
#         )
#         # self.opti.minimize(20 * self.totalcost + self.regularization)
#         self.opti.minimize(20 * self.totalcost + 0.001*self.regularization + 0.1*self.smooth_cost)

#         opts = {
#             'ipopt':{
#                 'print_level':0,
#                 'max_iter':30,
#                 'tol':5e-3
#             },
#             'print_time':False
#         }
#         self.opti.solver("ipopt", opts)

#     def get_current_qpos(self):
#         return self.qpos.copy()

#     def set_current_qpos(self, qpos):
#         self.qpos = qpos.copy()

#     def get_joint_names(self):
#         # Pinocchio by default add a dummy joint name called "universe"
#         names = list(self.model.names)
#         return names[1:]

#     @abstractmethod
#     def control(self, target_pos, target_rot):
#         pass


class BaseOptimizer:

    def __init__(
        self,
        urdf_path,
        hand_indices,
        wrist_link_name,
        alpha,
    ):
        self.model = pin.buildModelFromUrdf(str(urdf_path))
        self.dof = self.model.nq
        self.hand_indices = hand_indices

        # lock joints
        locked_joint_ids = list(set(range(self.dof)) - set(self.hand_indices))
        locked_joint_ids = [id + 1 for id in locked_joint_ids]  # account for universe joint
        self.model = pin.buildReducedModel(self.model, locked_joint_ids, np.zeros(self.dof))
        self.hand_dof = self.model.nq

        self.data = self.model.createData()
        self.wrist_link_name = wrist_link_name
        self.alpha = float(alpha)

        # update model placement
        self.wrist_link_id = self.model.getFrameId(wrist_link_name)
        pin.forwardKinematics(self.model, self.data, pin.neutral(self.model))
        self.wrist_link_pose = pin.updateFramePlacement(
            self.model, self.data, self.wrist_link_id
        )

        # opt related settings
        self.opt = nlopt.opt(nlopt.LD_SLSQP, self.hand_dof)
        self.set_joint_limit()
        # self.opt.set_maxeval(100)

        # mimic joints
        self.parent_joint_indices = np.array([])
        self.child_joint_indices = np.array([])
        self.mimic_factors = np.array([])

    def set_joint_limit(self,):
        lower_limit = self.model.lowerPositionLimit
        upper_limit = self.model.upperPositionLimit
        self.opt.set_lower_bounds(lower_limit.tolist())
        self.opt.set_upper_bounds(upper_limit.tolist())

    def set_joint_mimic(self, mimic_config, tol=1e-2):
        parent_joint_names = mimic_config['parent_joints']
        child_joint_names = mimic_config['child_joints']
        mimic_factors = mimic_config['mimic_factors']
        if len(parent_joint_names) != len(child_joint_names) or len(parent_joint_names) != len(mimic_factors):
            raise ValueError("Expect lists to be of the same length")
        n_mimic = len(mimic_factors)
        tols = np.ones(n_mimic) * tol
        parent_joint_indices = []
        child_joint_indices = []
        for parent_joint_name in parent_joint_names:
            idx = self.model.getJointId(parent_joint_name)
            if idx > self.hand_dof:
                raise ValueError(f"Joint {parent_joint_name} given does not appear to be in robot XML.")
            parent_joint_indices.append(idx - 1)
        for child_joint_name in child_joint_names:
            idx = self.model.getJointId(child_joint_name)
            if idx > self.hand_dof:
                raise ValueError(f"Joint {child_joint_name} given does not appear to be in robot XML.")
            child_joint_indices.append(idx - 1)
        self.parent_joint_indices = np.array(parent_joint_indices, dtype=int)
        self.child_joint_indices = np.array(child_joint_indices, dtype=int)
        self.mimic_factors = np.array(mimic_factors)

    def get_last_result(self):
        return self.opt.last_optimize_result()

    def get_link_indices(self, target_link_names):
        target_link_indices = []
        for target_link_name in target_link_names:
            idx = self.model.getFrameId(target_link_name)
            if idx >= len(self.model.frames):
                raise ValueError(f"Body {target_link_name} given does not appear to be in robot XML.")
            target_link_indices.append(idx)
        return target_link_indices

    @abstractmethod
    def retarget(self, ref_value, fixed_qpos, last_qpos=None):
        pass

    def optimize(self, objective_fn, last_qpos):
        self.opt.set_min_objective(objective_fn)
        try:
            qpos = self.opt.optimize(last_qpos)
        except RuntimeError as e:
            print(e)
            return np.array(last_qpos)
        return pin.interpolate(self.model, np.array(last_qpos), qpos, self.alpha)