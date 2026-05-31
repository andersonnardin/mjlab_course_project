from pathlib import Path

import mujoco

from mjlab.entity.entity import EntityCfg
from mjlab.entity.entity import EntityArticulationInfoCfg
from mjlab.utils.spec_config import CollisionCfg
from mjlab.actuator.builtin_actuator import BuiltinPositionActuatorCfg

from atom01_mjlab.config.constants import (
    ATOM01_XML_PATH,
    ATOM01_DEFAULT_JOINT_POS,
    ATOM01_BASE_INIT_POS,
    ATOM01_BASE_INIT_QUAT,
)

ATOM01_XML = Path(ATOM01_XML_PATH)


def get_atom01_spec() -> mujoco.MjSpec:
    spec = mujoco.MjSpec.from_file(str(ATOM01_XML))
    return spec


ATOM01_STANDING_KEYFRAME = EntityCfg.InitialStateCfg(
    pos=ATOM01_BASE_INIT_POS,
    rot=ATOM01_BASE_INIT_QUAT,
    lin_vel=(0.0, 0.0, 0.0),
    ang_vel=(0.0, 0.0, 0.0),
    joint_pos=ATOM01_DEFAULT_JOINT_POS,
    joint_vel={".*": 0.0},
)


ATOM01_FULL_COLLISION = CollisionCfg(
    geom_names_expr=(".*",),
    contype=1,
    conaffinity=1,
    condim={
        "^(left|right)_foot_collision$": 3,
        ".*": 1,
    },
    priority={
        "^(left|right)_foot_collision$": 1,
    },
    friction={
        "^(left|right)_foot_collision$": (0.8,),
    },
    solref=None,
    solimp=None,
    disable_other_geoms=False,
)


# Stronger actuation so the robot can actually support itself.
ATOM01_ARTICULATION = EntityArticulationInfoCfg(
    actuators=(
        BuiltinPositionActuatorCfg(
            target_names_expr=(
                ".*_thigh_yaw_joint",
                ".*_thigh_roll_joint",
            ),
            armature=0.02,
            frictionloss=0.0,
            stiffness=80.0,
            damping=5.0,
            effort_limit=120.0,
        ),
        BuiltinPositionActuatorCfg(
            target_names_expr=(
                ".*_thigh_pitch_joint",
                ".*_knee_joint",
            ),
            armature=0.03,
            frictionloss=0.0,
            stiffness=140.0,
            damping=8.0,
            effort_limit=180.0,
        ),
        BuiltinPositionActuatorCfg(
            target_names_expr=(
                ".*_ankle_pitch_joint",
                ".*_ankle_roll_joint",
            ),
            armature=0.02,
            frictionloss=0.0,
            stiffness=70.0,
            damping=4.0,
            effort_limit=90.0,
        ),
        BuiltinPositionActuatorCfg(
            target_names_expr=("torso_joint",),
            armature=0.02,
            frictionloss=0.0,
            stiffness=60.0,
            damping=4.0,
            effort_limit=80.0,
        ),
        BuiltinPositionActuatorCfg(
            target_names_expr=(
                ".*_arm_pitch_joint",
                ".*_arm_roll_joint",
                ".*_arm_yaw_joint",
                ".*_elbow_pitch_joint",
                ".*_elbow_yaw_joint",
            ),
            armature=0.005,
            frictionloss=0.0,
            stiffness=20.0,
            damping=1.5,
            effort_limit=30.0,
        ),
    ),
    soft_joint_pos_limit_factor=0.9,
)


def get_atom01_robot_cfg() -> EntityCfg:
    return EntityCfg(
        init_state=ATOM01_STANDING_KEYFRAME,
        collisions=(ATOM01_FULL_COLLISION,),
        spec_fn=get_atom01_spec,
        articulation=ATOM01_ARTICULATION,
    )