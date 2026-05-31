from mjlab.tasks.velocity.config.g1.env_cfgs import (
    ManagerBasedRlEnvCfg,
    UniformVelocityCommandCfg,
    make_velocity_env_cfg,
    JointPositionActionCfg,
    mdp,
)
from mjlab.managers import SceneEntityCfg
from mjlab.sensor import ContactMatch, ContactSensorCfg
from mjlab.managers.termination_manager import TerminationTermCfg

from atom01_mjlab.config.robot_cfg import get_atom01_robot_cfg
from atom01_mjlab.config.constants import (
    ATOM01_TORSO_BODY,
    ATOM01_LEFT_FOOT_SITE,
    ATOM01_RIGHT_FOOT_SITE,
    ATOM01_LEFT_FOOT_GEOM,
    ATOM01_RIGHT_FOOT_GEOM,
    ATOM01_LOCOMOTION_ACTUATOR_REGEX,
    ATOM01_ILLEGAL_GROUND_CONTACT_BODIES,
)

from atom01_mjlab.terrain.terrain_constants import ATOM01_ROUGH_TERRAIN_CFG


def atom01_rough_env_cfg(play: bool = False) -> ManagerBasedRlEnvCfg:
    cfg = make_velocity_env_cfg()

    # --------------------------------------------------
    # Terrain: custom rough terrain for Atom01
    # --------------------------------------------------
    assert cfg.scene.terrain is not None
    cfg.scene.terrain.terrain_type = "generator"
    cfg.scene.terrain.terrain_generator = ATOM01_ROUGH_TERRAIN_CFG
    cfg.scene.terrain.max_init_terrain_level = 3

    # --------------------------------------------------
    # Robot
    # --------------------------------------------------
    cfg.scene.entities["robot"] = get_atom01_robot_cfg()

    # --------------------------------------------------
    # Contact sensors
    # --------------------------------------------------
    feet_ground_cfg = ContactSensorCfg(
        name="feet_ground_contact",
        primary=ContactMatch(
            mode="body",
            pattern=r"^(left_ankle_roll_link|right_ankle_roll_link)$",
            entity="robot",
        ),
        secondary=ContactMatch(
            mode="body",
            pattern="terrain",
        ),
        fields=("found", "force"),
        reduce="netforce",
        num_slots=1,
        track_air_time=True,
    )

    illegal_body_pattern = "^(" + "|".join(ATOM01_ILLEGAL_GROUND_CONTACT_BODIES) + ")$"
    body_ground_cfg = ContactSensorCfg(
        name="body_ground_contact",
        primary=ContactMatch(
            mode="body",
            pattern=illegal_body_pattern,
            entity="robot",
        ),
        secondary=ContactMatch(
            mode="body",
            pattern="terrain",
        ),
        fields=("found",),
        reduce="none",
        num_slots=1,
    )

    cfg.scene.sensors = tuple(cfg.scene.sensors or ()) + (
        feet_ground_cfg,
        body_ground_cfg,
    )

    # --------------------------------------------------
    # Built-in sensor names from atom01.xml
    # --------------------------------------------------
    cfg.observations["actor"].terms["base_lin_vel"].params["sensor_name"] = "robot/linear-velocity"
    cfg.observations["actor"].terms["base_ang_vel"].params["sensor_name"] = "robot/angular-velocity"

    cfg.observations["critic"].terms["base_lin_vel"].params["sensor_name"] = "robot/linear-velocity"
    cfg.observations["critic"].terms["base_ang_vel"].params["sensor_name"] = "robot/angular-velocity"

    # For the first successful locomotion run, disable actor corruption.
    cfg.observations["actor"].enable_corruption = False

    # --------------------------------------------------
    # Per-robot references
    # --------------------------------------------------
    if cfg.scene.sensors:
        for sensor in cfg.scene.sensors:
            if sensor.name == "terrain_scan":
                sensor.frame.name = ATOM01_TORSO_BODY

    cfg.observations["critic"].terms["foot_height"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        site_names=(ATOM01_LEFT_FOOT_SITE, ATOM01_RIGHT_FOOT_SITE),
    )

    cfg.events["foot_friction"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        geom_names=(ATOM01_LEFT_FOOT_GEOM, ATOM01_RIGHT_FOOT_GEOM),
    )
    cfg.events["base_com"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        body_names=(ATOM01_TORSO_BODY,),
    )

    cfg.rewards["upright"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        body_names=(ATOM01_TORSO_BODY,),
    )

    cfg.rewards["pose"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        joint_names=ATOM01_LOCOMOTION_ACTUATOR_REGEX,
    )
    cfg.rewards["pose"].params["std_standing"] = {
        ".*_thigh_yaw_joint": 0.12,
        ".*_thigh_roll_joint": 0.12,
        ".*_thigh_pitch_joint": 0.20,
        ".*_knee_joint": 0.20,
        ".*_ankle_pitch_joint": 0.20,
        ".*_ankle_roll_joint": 0.12,
        "torso_joint": 0.12,
    }
    cfg.rewards["pose"].params["std_walking"] = {
        ".*_thigh_yaw_joint": 0.20,
        ".*_thigh_roll_joint": 0.20,
        ".*_thigh_pitch_joint": 0.35,
        ".*_knee_joint": 0.35,
        ".*_ankle_pitch_joint": 0.35,
        ".*_ankle_roll_joint": 0.20,
        "torso_joint": 0.18,
    }
    cfg.rewards["pose"].params["std_running"] = {
        ".*_thigh_yaw_joint": 0.28,
        ".*_thigh_roll_joint": 0.28,
        ".*_thigh_pitch_joint": 0.50,
        ".*_knee_joint": 0.50,
        ".*_ankle_pitch_joint": 0.50,
        ".*_ankle_roll_joint": 0.28,
        "torso_joint": 0.24,
    }

    cfg.rewards["body_ang_vel"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        body_names=(ATOM01_TORSO_BODY,),
    )

    cfg.rewards["foot_clearance"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        site_names=(ATOM01_LEFT_FOOT_SITE, ATOM01_RIGHT_FOOT_SITE),
    )
    cfg.rewards["foot_swing_height"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        site_names=(ATOM01_LEFT_FOOT_SITE, ATOM01_RIGHT_FOOT_SITE),
    )
    cfg.rewards["foot_slip"].params["asset_cfg"] = SceneEntityCfg(
        "robot",
        site_names=(ATOM01_LEFT_FOOT_SITE, ATOM01_RIGHT_FOOT_SITE),
    )

    # --------------------------------------------------
    # Viewer
    # --------------------------------------------------
    cfg.viewer.body_name = ATOM01_TORSO_BODY

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------
    joint_action = cfg.actions["joint_pos"]
    assert isinstance(joint_action, JointPositionActionCfg)
    joint_action.scale = 0.15
    joint_action.actuator_names = ATOM01_LOCOMOTION_ACTUATOR_REGEX

    # --------------------------------------------------
    # Commands
    # --------------------------------------------------
    twist_cmd = cfg.commands["twist"]
    assert isinstance(twist_cmd, UniformVelocityCommandCfg)
    twist_cmd.ranges.lin_vel_x = (-0.6, 0.8)
    twist_cmd.ranges.lin_vel_y = (-0.2, 0.2)
    twist_cmd.ranges.ang_vel_z = (-0.35, 0.35)

    # --------------------------------------------------
    # Rewards
    # --------------------------------------------------
    cfg.rewards.pop("angular_momentum", None)

    cfg.rewards["track_linear_velocity"].weight = 1.5
    cfg.rewards["track_angular_velocity"].weight = 1.0
    cfg.rewards["upright"].weight = 2.5
    cfg.rewards["pose"].weight = 1.5
    cfg.rewards["body_ang_vel"].weight = -0.1

    cfg.rewards["air_time"].weight = 0.10
    cfg.rewards["foot_clearance"].weight = -0.5
    cfg.rewards["foot_swing_height"].weight = -0.05
    cfg.rewards["foot_slip"].weight = -0.05
    cfg.rewards["soft_landing"].weight = -1e-5

    # --------------------------------------------------
    # Terminations
    # --------------------------------------------------
    cfg.terminations["illegal_contacts"] = TerminationTermCfg(
        func=mdp.illegal_contact,
        params={"sensor_name": "body_ground_contact"},
    )

    # --------------------------------------------------
    # Make the first successful training easier
    # --------------------------------------------------
    # Remove pushes and startup randomization initially.
    cfg.events.pop("push_robot", None)
    cfg.events.pop("foot_friction", None)
    cfg.events.pop("encoder_bias", None)
    cfg.events.pop("base_com", None)

    if play:
        cfg.scene.num_envs = 1
        twist_cmd.ranges.lin_vel_x = (-0.6, 0.8)
        twist_cmd.ranges.lin_vel_y = (-0.2, 0.2)
        twist_cmd.ranges.ang_vel_z = (-0.35, 0.35)

    return cfg


def atom01_flat_env_cfg(play: bool = False) -> ManagerBasedRlEnvCfg:
    cfg = atom01_rough_env_cfg(play=play)

    cfg.sim.njmax = 300
    cfg.sim.mujoco.ccd_iterations = 50
    cfg.sim.contact_sensor_maxmatch = 64
    cfg.sim.nconmax = None

    assert cfg.scene.terrain is not None
    cfg.scene.terrain.terrain_type = "plane"
    cfg.scene.terrain.terrain_generator = None

    cfg.scene.sensors = tuple(
        s for s in (cfg.scene.sensors or ()) if s.name != "terrain_scan"
    )
    del cfg.observations["actor"].terms["height_scan"]
    del cfg.observations["critic"].terms["height_scan"]

    cfg.curriculum.pop("terrain_levels", None)

    if play:
        twist_cmd = cfg.commands["twist"]
        assert isinstance(twist_cmd, UniformVelocityCommandCfg)
        twist_cmd.ranges.lin_vel_x = (-0.6, 0.8)
        twist_cmd.ranges.lin_vel_y = (-0.2, 0.2)
        twist_cmd.ranges.ang_vel_z = (-0.35, 0.35)

    return cfg