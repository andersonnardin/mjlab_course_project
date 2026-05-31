from atom01_mjlab.tasks.velocity.env_cfgs import (
    atom01_flat_env_cfg,
    atom01_rough_env_cfg,
)
from atom01_mjlab.tasks.velocity.rl_cfg import atom01_ppo_runner_cfg

from mjlab.tasks.registry import register_mjlab_task
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner


register_mjlab_task(
    task_id="Mjlab-Velocity-Flat-Atom01-V2",
    env_cfg=atom01_flat_env_cfg(),
    play_env_cfg=atom01_flat_env_cfg(play=True),
    rl_cfg=atom01_ppo_runner_cfg(),
    runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
    task_id="Mjlab-Velocity-Rough-Atom01-V2",
    env_cfg=atom01_rough_env_cfg(),
    play_env_cfg=atom01_rough_env_cfg(play=True),
    rl_cfg=atom01_ppo_runner_cfg(),
    runner_cls=VelocityOnPolicyRunner,
)