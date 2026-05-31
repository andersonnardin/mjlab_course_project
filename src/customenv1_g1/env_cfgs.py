from mjlab.tasks.velocity.config.g1.env_cfgs import unitree_g1_rough_env_cfg
from customenv1_g1.terrain.terrain_constants import custom_terrain_cfg


def customenv1_g1_env_cfg(play: bool = False):
    cfg = unitree_g1_rough_env_cfg(play=play)

    cfg.scene.terrain = custom_terrain_cfg(num_envs=cfg.scene.num_envs)

    # Increase contact capacity for rough custom terrain
    cfg.sim.nconmax = 200
    cfg.sim.contact_sensor_maxmatch = 500

    if play:
        cfg.scene.num_envs = 1

        if cfg.scene.terrain is not None and cfg.scene.terrain.terrain_generator is not None:
            cfg.scene.terrain.terrain_generator.curriculum = False
            cfg.scene.terrain.terrain_generator.num_rows = 3
            cfg.scene.terrain.terrain_generator.num_cols = 3
            cfg.scene.terrain.terrain_generator.border_width = 6.0

    return cfg