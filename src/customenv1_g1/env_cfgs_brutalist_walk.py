from mjlab.tasks.velocity.config.g1.env_cfgs import unitree_g1_flat_env_cfg
from customenv1_g1.scene_objects.object_constants import (
    get_brutalist_room_cfg,
    get_decorative_sphere_cfg,
)

def customenv1_g1_env__brutalist_cfg(play: bool = False):
    cfg = unitree_g1_flat_env_cfg(play=play)

    # --------------------------------------------------
    # CHANGE ROBOT SPAWN HEIGHT
    # --------------------------------------------------
    robot_cfg = cfg.scene.entities["robot"]

    # Raise robot (example: +0.3 meters)
    robot_cfg.init_state.pos = (0.0, 0.0, 0.76)

    # Optional: also reset velocity (good practice)
    robot_cfg.init_state.lin_vel = (0.0, 0.0, 0.0)
    robot_cfg.init_state.ang_vel = (0.0, 0.0, 0.0)

    # --------------------------------------------------
    # Scene
    # --------------------------------------------------
    cfg.scene.entities["brutalist_room"] = get_brutalist_room_cfg(pos=(0.0, 0.0, 0.0))
    #cfg.scene.entities["_decorative_sphere"] = get_decorative_sphere_cfg(pos=(2.0, 0.0, 1.4))

    if play:
        cfg.scene.num_envs = 1
        cfg.sim.nconmax = 200

    return cfg