from pathlib import Path

# -------------------------
# XML PATH
# -------------------------
ATOM01_XML_PATH = str(
    Path("/home/user/__REMOTE_WORKSPACE__/policies_ws/mjlab_course_project/src/atom01_mjlab/assets/atom01/mujoco_files/atom01.xml")
)

# -------------------------
# BODY / SITES
# -------------------------
ATOM01_ROOT_BODY = "base_link"
ATOM01_TORSO_BODY = "torso_link"
ATOM01_IMU_SITE = "imu"

ATOM01_LEFT_FOOT_GEOM = "left_foot_collision"
ATOM01_RIGHT_FOOT_GEOM = "right_foot_collision"

ATOM01_LEFT_FOOT_SITE = "left_foot_site"
ATOM01_RIGHT_FOOT_SITE = "right_foot_site"

# Bodies that should NOT touch the ground during normal locomotion.
ATOM01_ILLEGAL_GROUND_CONTACT_BODIES = (
    "left_knee_link",
    "right_knee_link",
    "left_thigh_pitch_link",
    "right_thigh_pitch_link",
    "torso_link",
    "left_arm_pitch_link",
    "right_arm_pitch_link",
    "left_elbow_pitch_link",
    "right_elbow_pitch_link",
)

# -------------------------
# JOINT GROUPS
# -------------------------
ATOM01_LEG_JOINTS = [
    "left_thigh_yaw_joint",
    "left_thigh_roll_joint",
    "left_thigh_pitch_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_thigh_yaw_joint",
    "right_thigh_roll_joint",
    "right_thigh_pitch_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
]

ATOM01_TORSO_JOINTS = [
    "torso_joint",
]

ATOM01_ARM_JOINTS = [
    "left_arm_pitch_joint",
    "left_arm_roll_joint",
    "left_arm_yaw_joint",
    "left_elbow_pitch_joint",
    "left_elbow_yaw_joint",
    "right_arm_pitch_joint",
    "right_arm_roll_joint",
    "right_arm_yaw_joint",
    "right_elbow_pitch_joint",
    "right_elbow_yaw_joint",
]

# Joints we actively command for locomotion.
ATOM01_LOCOMOTION_ACTUATOR_REGEX = (
    ".*_thigh_yaw_joint",
    ".*_thigh_roll_joint",
    ".*_thigh_pitch_joint",
    ".*_knee_joint",
    ".*_ankle_pitch_joint",
    ".*_ankle_roll_joint",
    "torso_joint",
)

# -------------------------
# DEFAULT POSE
# -------------------------
# Stronger crouched stance for balance.
ATOM01_DEFAULT_JOINT_POS = {
    "left_thigh_yaw_joint": 0.0,
    "left_thigh_roll_joint": 0.0,
    "left_thigh_pitch_joint": -0.28,
    "left_knee_joint": 0.55,
    "left_ankle_pitch_joint": -0.27,
    "left_ankle_roll_joint": 0.0,

    "right_thigh_yaw_joint": 0.0,
    "right_thigh_roll_joint": 0.0,
    "right_thigh_pitch_joint": -0.28,
    "right_knee_joint": 0.55,
    "right_ankle_pitch_joint": -0.27,
    "right_ankle_roll_joint": 0.0,

    "torso_joint": 0.0,

    "left_arm_pitch_joint": 0.15,
    "left_arm_roll_joint": 0.0,
    "left_arm_yaw_joint": 0.0,
    "left_elbow_pitch_joint": 0.30,
    "left_elbow_yaw_joint": 0.0,

    "right_arm_pitch_joint": 0.15,
    "right_arm_roll_joint": 0.0,
    "right_arm_yaw_joint": 0.0,
    "right_elbow_pitch_joint": 0.30,
    "right_elbow_yaw_joint": 0.0,
}

# -------------------------
# BASE INIT
# -------------------------
ATOM01_BASE_INIT_POS = (0.0, 0.0, 0.80)
ATOM01_BASE_INIT_QUAT = (1.0, 0.0, 0.0, 0.0)