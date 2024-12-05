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
import numpy as np
from typing import List

from .motion.pink_motion_control import PinkMotionControl
from .motion.pinocchio_motion_retarget import PinocchioVectorOptimizer
# from core.motion.pinocchio_motion_retarget_jax import PinocchioVectorOptimizerJax
from .utils.motion_utils import LPFilter, LPSE3Filter, LPConstrainedSE3Filter

from pytransform3d import rotations

import yaml

def categorize_and_map_value(
    array: np.ndarray,
    value_range: List[float],
    min_distance: float = 0.05,
    max_distance: float = 0.08,
) -> float:
    distance = np.linalg.norm(array[0] - array[1])
    clamped_distance = max(min_distance, min(distance, max_distance))
    mapped_value = (clamped_distance - min_distance) * (
        (value_range[1] - value_range[0]) / (max_distance - min_distance)
    ) + value_range[0]
    return mapped_value

class RobotController:
    def __init__(self, asset_dir, config_dir):
        self.default_urdf_dir = Path(asset_dir)
        self.default_config_dir = Path(config_dir)
        self.dof = 0
        self._qpos = None

        self.body_indices = None
        self.left_arm_indices = None
        self.right_arm_indices = None
        self.right_hand_indices = None
        self.left_hand_indices = None
        self.with_hand = False

        # Controllers
        # self.body_controller = None
        self.left_arm_controller = None
        self.right_arm_controller = None
        self.left_hand_controller = None
        self.right_hand_controller = None

        # Filters
        self.head_filter = None
        # self.body_filter = None
        self.left_wrist_filter = None
        self.right_wrist_filter = None
        self.left_fingertip_pos_filter = None
        self.right_fingertip_pos_filter = None

        self.configured = None

        self._head_rot_mat = np.zeros((3, 3))
        self.euler = np.zeros(3)

    def set_urdf_dir(self,  urdf_dir):
        path = Path(urdf_dir)
        if not path.exists():
            raise ValueError(f"URDF dir {urdf_dir} not exists.")
        self.default_urdf_dir = path

    def set_config_dir(self, config_dir):
        path = Path(config_dir)
        if not path.exists():
            raise ValueError(f"Config dir {config_dir} not exists.")
        self.default_config_dir = path

    def load_config(self, config_file_name):
        robot_config_path = self.default_config_dir / Path(config_file_name)
        with Path(robot_config_path).open('r') as f:
            cfg = yaml.safe_load(f)['robot_cfg']
        self.name = cfg['name']
        self.urdf_path = self.default_urdf_dir / Path(cfg['urdf_path'])
        self.mesh_path = self.default_urdf_dir / Path(cfg['mesh_path'])
        self.body_indices = cfg['body_indices']
        self.left_arm_indices = cfg['left_arm_indices']
        self.right_arm_indices = cfg['right_arm_indices']
        self.left_hand_indices = cfg.get('left_hand_indices', [])
        self.right_hand_indices = cfg.get('right_hand_indices', [])

        self.ee_type = cfg.get('ee_type', 'hand')

        #! gripper mode
        if self.ee_type == 'gripper':
            self.human_hand_indices = cfg['human_hand_indices']
            ee_config = cfg["ee"]

            self.left_gripper_range = ee_config["left_ee"]["gripper_range"]
            self.right_gripper_range = ee_config["right_ee"]["gripper_range"]
            self.gripper_type = cfg["gripper_type"]

        self.with_hand = len(self.right_hand_indices) + len(self.left_hand_indices) > 0

        self.dof = len(self.body_indices) + len(self.right_arm_indices) + len(self.left_arm_indices) + len(self.right_hand_indices) + len(self.left_hand_indices)
        self._qpos = np.zeros(self.dof)

        # h1_inspire: 51 = 6 left leg + 6 right leg + 1 torso + 7 left arm + 12 left hand + 7 right arm + 12 right hand
        # h1: 19 = 5 left leg + 5 right leg + 1 torso + 4 left arm + 4 right arm
        # gr1: 32 = 3 waist + 3 head + 7 left arm + 7 right arm + 6 left leg + 6 right leg

        self.head_pos = np.asarray(cfg['head_pos'])
        self.left_wrist_name = cfg['left_wrist_name']
        self.right_wrist_name = cfg['right_wrist_name']

        # Configure body controller & filter
        # body_controller_path = cfg['body']['model_path']
        # self.body_controller = torch.load(body_controller_path)
        self.head_filter = LPSE3Filter(cfg['body']['in_lp_alpha'])

        # Configure arm controller & filter
        arm_config = cfg['arm']
        self.left_arm_controller = PinkMotionControl(
            self.urdf_path,
            self.mesh_path,
            self.left_arm_indices,
            self.left_wrist_name,
            arm_config,
        )
        self.right_arm_controller = PinkMotionControl(
            self.urdf_path,
            self.mesh_path,
            self.right_arm_indices,
            self.right_wrist_name,
            arm_config,
        )
        self.left_wrist_filter = LPConstrainedSE3Filter(arm_config['in_lp_alpha'])
        self.right_wrist_filter = LPConstrainedSE3Filter(arm_config['in_lp_alpha'])

        hand_config = cfg.get('hand', None)
        if hand_config is not None:
            if not self.with_hand:
                raise ValueError("Hand indices not provided.")
            left_config = hand_config['left_hand']
            right_config = hand_config['right_hand']

            self.left_fingertip_pos_filter = LPFilter(left_config['in_lp_alpha'])
            self.right_fingertip_pos_filter = LPFilter(right_config['in_lp_alpha'])

            # Configure hand controller & filter
            if self.ee_type == 'hand':
                
                self.left_hand_controller = PinocchioVectorOptimizer(
                    self.urdf_path,
                    self.left_hand_indices,
                    self.left_wrist_name,
                    left_config,
                )
                self.right_hand_controller = PinocchioVectorOptimizer(
                    self.urdf_path,
                    self.right_hand_indices,
                    self.right_wrist_name,
                    right_config,
                )
                if left_config.get('mimic'):
                    self.left_hand_controller.set_joint_mimic(left_config['mimic'])
                if right_config.get('mimic'):
                    self.right_hand_controller.set_joint_mimic(right_config['mimic'])

        self.configured = True
        self.cfg = cfg
        self.arm_cfg = arm_config
        self.hand_config = hand_config

    def update(self,
               head2world_mat,
               left_wrist2world_mat,
               right_wrist2world_mat,
               left_fingertip2wrist_pos,
               right_fingertip2wrist_pos):
        if not self.configured:
            raise ValueError('Robot Controller has not been configured.')

        # Update body qpos
        self._head_rot_mat = self.head_filter.next(head2world_mat)[:3, :3]
        self.euler = rotations.intrinsic_euler_zyx_from_active_matrix(self._head_rot_mat)

        # body_qpos = self.body_controller(self.qpos, head_pos, head_rot)
        # body_qpos = self.body_filter.next(body_qpos)
        body_qpos = np.zeros(len(self.body_indices))

        # Update arm qpos
        left_wrist_mat = self.left_wrist_filter.next(left_wrist2world_mat)
        right_wrist_mat = self.right_wrist_filter.next(right_wrist2world_mat)
        left_arm_qpos = self.left_arm_controller.control(
            left_wrist_mat[:3, 3] + self.head_pos,
            left_wrist_mat[:3, :3],
        )
        right_arm_qpos = self.right_arm_controller.control(
            right_wrist_mat[:3, 3] + self.head_pos,
            right_wrist_mat[:3, :3],
        )

        if self.with_hand:
            left_fingertip_pos = self.left_fingertip_pos_filter.next(left_fingertip2wrist_pos)
            right_fingertip_pos = self.right_fingertip_pos_filter.next(right_fingertip2wrist_pos)
            last_left_hand_qpos = self._qpos[self.left_hand_indices].copy()
            last_right_hand_qpos = self._qpos[self.right_hand_indices].copy()

            # Update hand qpos
            if self.ee_type == "hand":
                
                left_hand_qpos = self.left_hand_controller.retarget(
                    left_fingertip_pos,
                    last_left_hand_qpos,
                )
                right_hand_qpos = self.right_hand_controller.retarget(
                    right_fingertip_pos,
                    last_right_hand_qpos,
                )

            elif self.ee_type == "gripper":
                left_hand_qpos = categorize_and_map_value(
                    left_fingertip_pos[self.human_hand_indices], self.left_gripper_range
                )
                right_hand_qpos = categorize_and_map_value(
                    right_fingertip_pos[self.human_hand_indices], self.right_gripper_range
                )
            
        # udpate qpos
        self._qpos[self.body_indices] = body_qpos
        self._qpos[self.left_arm_indices] = left_arm_qpos
        self._qpos[self.right_arm_indices] = right_arm_qpos
        if self.with_hand:
            self._qpos[self.left_hand_indices] = left_hand_qpos
            self._qpos[self.right_hand_indices] = right_hand_qpos
        # if self.waist_index is not None:
        #     # print("waist_qpos: ", waist_qpos)
        #     self._qpos[self.waist_index] = waist_qpos

    @property
    def qpos(self):
        return self._qpos.astype(np.float32).copy()

    @property
    def ypr(self):
        return self.euler

    @property
    def head_rot_mat(self):
        return self._head_rot_mat
    
    def compute_err(self, robot_states):
        left_arm_state = np.concatenate((robot_states[0:4], robot_states[8:11]))
        right_arm_state = np.concatenate((robot_states[4:8], robot_states[11:14]))
        # left_arm_state = robot_actions[0:7]
        # right_arm_state = robot_actions[13:20]
        return (self.left_arm_controller.compute_err(left_arm_state) + self.right_arm_controller.compute_err(right_arm_state)) / 2
    
    def add_collision_box(self, box_pos, box_size):
        if self.arm_cfg.get('left_links') and self.arm_cfg.get('right_links'):
            self.left_arm_controller.add_collision_box(box_pos, box_size, self.arm_cfg['left_links'])
            self.right_arm_controller.add_collision_box(box_pos, box_size, self.arm_cfg['right_links'])
        else:
            return
