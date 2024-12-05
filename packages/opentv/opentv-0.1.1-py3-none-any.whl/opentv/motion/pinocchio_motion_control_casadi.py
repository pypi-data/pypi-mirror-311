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
import pinocchio.casadi as cpin  
# import hppfcl
import yaml

from opentv.motion.pinocchio_base import BaseControlCasadi

class PinocchioMotionControlCasadi(BaseControlCasadi):
    def __init__(
        self,
        urdf_path,
        arm_indices,
        wrist_name,
        arm_config,
    ):
        super().__init__(urdf_path, arm_indices, wrist_name, arm_config['out_lp_alpha'])
        self.scaling_factor = float(arm_config['scaling_factor'])

    def control(self, target_pos, target_rot):

        target_pos[:2] = target_pos[:2] * self.scaling_factor
        oMdes = pin.SE3(target_rot, target_pos)

        self.opti.set_initial(self.var_q, self.init_data)
        self.opti.set_value(self.param_tf, np.array(oMdes))

        try:
            # sol = self.opti.solve()
            sol = self.opti.solve_limited()
            sol_q = self.opti.value(self.var_q)

            # self.vis.display(sol_q)
            self.init_data = sol_q
            self.qpos = pin.interpolate(self.model, self.qpos, sol_q, self.alpha)

            return self.qpos.copy()
        
        except Exception as e:
            print(f"ERROR in convergence, plotting debug info.{e}")
            # sol_q = self.opti.debug.value(self.var_q)   # return original value
            return self.qpos.copy()