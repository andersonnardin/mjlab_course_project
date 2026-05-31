from customenv1_g1.env_cfgs import customenv1_g1_env_cfg
from customenv1_g1.rl_cfg import customenv1_g1_ppo_runner_cfg

from mjlab.tasks.registry import register_mjlab_task
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner


register_mjlab_task(
    task_id="Mjlab-Velocity-CustomEnv2-Unitree-G1",
    env_cfg=customenv1_g1_env_cfg(),
    play_env_cfg=customenv1_g1_env_cfg(play=True),
    rl_cfg=customenv1_g1_ppo_runner_cfg(),
    runner_cls=VelocityOnPolicyRunner,
)