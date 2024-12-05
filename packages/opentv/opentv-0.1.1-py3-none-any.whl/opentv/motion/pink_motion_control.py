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
import qpsolvers
import yaml

import pink
from pink import solve_ik
from pink.tasks import FrameTask, PostureTask, DampingTask
from pink.barriers import SelfCollisionBarrier

import hppfcl as fcl

class PinkMotionControl:
    def __init__(
        self,
        urdf_path,
        mesh_path,
        arm_indices,
        wrist_name,
        arm_config,
    ):
        self.arm_indices = arm_indices
        self.alpha = float(arm_config['out_lp_alpha'])
        self.dt = float(arm_config['dt'])
        self.scaling_factor = float(arm_config['scaling_factor'])
        self.lm_damping = float(arm_config['base_damping'])

        self.model = pin.buildModelFromUrdf(str(urdf_path))
        self.dof = self.model.nq

        # lock joints
        locked_joint_ids = list(set(range(self.dof)) - set(self.arm_indices))
        locked_joint_ids = [id + 1 for id in locked_joint_ids]  # account for universe joint
        self.model = pin.buildReducedModel(self.model, locked_joint_ids, np.zeros(self.dof))
        self.arm_dof = self.model.nq

        self.lower_limit = self.model.lowerPositionLimit
        self.upper_limit = self.model.upperPositionLimit

        self.geo_model = pin.buildGeomFromUrdf(self.model, str(urdf_path), pin.COLLISION, package_dirs=str(mesh_path))

        self.robot = pin.RobotWrapper(self.model, self.geo_model)

        # obj = pin.GeometryObject('table_0', 0, pin.SE3(np.eye(3), np.array([0.8, 0, 0.1])), fcl.Box(0.6, 0.6, 0.1))
        # self.robot.collision_model.addGeometryObject(obj)
        # self.robot.collision_data = pin.GeometryData(self.robot.collision_model)

        # tableid = self.robot.collision_model.getGeometryId('table_0')
        # for obj in self.robot.collision_model.geometryObjects:
        #     if 'table' in obj.name:
        #         continue
        #     elif 'elbow' in obj.name or 'wrist' in obj.name or 'hand' in obj.name:
        #         pair = pin.CollisionPair(tableid, self.robot.collision_model.getGeometryId(obj.name))
        #         self.robot.collision_model.addCollisionPair(pair)
        # self.robot.collision_data = pin.GeometryData(self.robot.collision_model)
        # self.robot.collision_data.enable_contact = True

        # Current state
        self.qpos = pin.neutral(self.robot.model)
        self.configuration = pink.Configuration(self.robot.model, self.robot.data, self.qpos)
        
        self.wrist_ee_task = FrameTask(
            wrist_name,
            position_cost = 10.0,
            orientation_cost = 1.0,
            lm_damping = self.lm_damping,
            gain = 0.5,
        )

        self.posture_task = PostureTask(
            cost = 1e-3,
        )

        self.damping_task = DampingTask(
            cost = 1e-1,
        )

        self.tasks = [self.wrist_ee_task, self.posture_task, self.damping_task]
        for task in self.tasks:
            task.set_target_from_configuration(self.configuration)

        self.barriers = []

        self.solver = qpsolvers.available_solvers[0]
        # if "clarabel" in qpsolvers.available_solvers:
        #     self.solver = "clarabel"
        # self.solver = "clarabel"
        if "proxqp" in qpsolvers.available_solvers:
            self.solver = "proxqp"

    def control(self, target_pos, target_rot):
        
        wrist_ee_target = self.wrist_ee_task.transform_target_to_world
        target_pos[:2] = target_pos[:2] * self.scaling_factor
        wrist_ee_target.translation = target_pos
        wrist_ee_target.rotation = target_rot

        qpos = self.qpos.copy()

        if len(self.barriers) != 0:
            v = solve_ik(self.configuration, self.tasks, self.dt, solver=self.solver, barriers=self.barriers)
        else:
            v = solve_ik(self.configuration, self.tasks, self.dt, solver=self.solver)

        v_min = 0.5 * (self.lower_limit - qpos) / self.dt
        v_max = 0.5 * (self.upper_limit - qpos) / self.dt
        v = np.clip(v, v_min, v_max)
        
        qpos = pin.integrate(self.robot.model, qpos, v * self.dt)
        self.qpos = pin.interpolate(self.robot.model, self.qpos, qpos, self.alpha)
        self.configuration.update(self.qpos)

        return self.qpos.copy()
    
    def add_collision_box(self, box_pos, box_size, links):
        idx = len(self.barriers)
        obj = pin.GeometryObject(f'box_{idx}', 0, pin.SE3(np.eye(3), box_pos), fcl.Box(*box_size))
        self.robot.collision_model.addGeometryObject(obj)

        boxid = self.robot.collision_model.getGeometryId(f'box_{idx}')
        for obj in self.robot.collision_model.geometryObjects:
            if f'box_{idx}' in obj.name:
                continue
            elif any([link in obj.name for link in links]):
                pair = pin.CollisionPair(boxid, self.robot.collision_model.getGeometryId(obj.name))
                self.robot.collision_model.addCollisionPair(pair)
        self.robot.collision_data = pin.GeometryData(self.robot.collision_model)
        self.robot.collision_data.enable_contact = True

        self.configuration = pink.Configuration(self.robot.model,
                                                self.robot.data,
                                                self.qpos,
                                                collision_model=self.robot.collision_model,
                                                collision_data=self.robot.collision_data
        )

        collision_barrier = SelfCollisionBarrier(
            n_collision_pairs = len(self.robot.collision_model.collisionPairs),
            gain=20.0,
            safe_displacement_gain=1.0,
            d_min=0.01,
        )
        self.barriers.append(collision_barrier)
