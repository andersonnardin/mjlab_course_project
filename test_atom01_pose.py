import mujoco
import mujoco.viewer
from atom01_mjlab.config.constants import ATOM01_XML_PATH
from atom01_mjlab.config.default_pose import ATOM01_DEFAULT_JOINT_POS

model = mujoco.MjModel.from_xml_path(ATOM01_XML_PATH)
data = mujoco.MjData(model)

joint_name_to_qpos = {}
for j in range(model.njnt):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, j)
    qpos_adr = model.jnt_qposadr[j]
    joint_name_to_qpos[name] = qpos_adr

# Base pose
data.qpos[0:3] = [0.0, 0.0, 0.78]
data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]

# Joint pose
for joint_name, value in ATOM01_DEFAULT_JOINT_POS.items():
    data.qpos[joint_name_to_qpos[joint_name]] = value

mujoco.mj_forward(model, data)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()