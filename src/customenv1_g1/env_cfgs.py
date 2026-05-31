from mjlab.tasks.registry import load_env_cfg
from customenv1_g1.scene_objects.object_constants import (
    get_brutalist_room_cfg,
    get_decorative_sphere_cfg,
)

def customenv1_g1_env_cfg(play: bool = False):
    cfg = load_env_cfg("Mjlab-Tracking-Flat-Unitree-G1", play=play)

    robot_cfg = cfg.scene.entities["robot"]
    robot_cfg.init_state.pos = (0.0, 0.0, 0.0)
    robot_cfg.init_state.lin_vel = (0.0, 0.0, 0.0)
    robot_cfg.init_state.ang_vel = (0.0, 0.0, 0.0)

    cfg.scene.entities["brutalist_room"] = get_brutalist_room_cfg(pos=(0.0, 0.0, 0.0))
    cfg.scene.entities["_decorative_sphere"] = get_decorative_sphere_cfg(pos=(2.0, 5.0, 1.4))

    # NOTE: THIS PATH WILL BE DIFFERENT FOR YOU, BECAUSE DEPENDS ON THE MIMIC TRAINING YOU DID IN PREV UNIT
    cfg.commands["motion"].motion_file = "/home/user/__REMOTE_WORKSPACE__/policies_ws/mjlab_course_project/artifacts/fight1_subject3:v0/motion.npz"
    
    if play:
        cfg.scene.num_envs = 1
        cfg.sim.nconmax = 200

    return cfg