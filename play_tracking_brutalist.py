import threading
import torch
from dataclasses import asdict

from mjlab.envs.manager_based_rl_env import ManagerBasedRlEnv
from mjlab.tasks.registry import load_env_cfg, load_rl_cfg, load_runner_cls
from mjlab.rl.vecenv_wrapper import RslRlVecEnvWrapper
from mjlab.viewer import ViserPlayViewer


TASK = "Mjlab-Tracking-CustomEnv2-Unitree-G1"
CHECKPOINT_PATH = "/home/user/__REMOTE_WORKSPACE__/policies_ws/mjlab_course_project/logs/rsl_rl/g1_tracking/2026-05-30_11-07-10/model_14000.pt"
DEVICE = "cuda"


class TeleopState:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset_requested = False
        self.quit_requested = False

    def request_reset(self):
        with self.lock:
            self.reset_requested = True

    def consume_reset(self):
        with self.lock:
            v = self.reset_requested
            self.reset_requested = False
            return v

    def request_quit(self):
        with self.lock:
            self.quit_requested = True

    def should_quit(self):
        with self.lock:
            return self.quit_requested


def teleop_input_loop(state: TeleopState):
    print("\nTracking viewer commands:")
    print("  r     -> reset env")
    print("  quit  -> exit\n")

    while not state.should_quit():
        try:
            line = input("> ").strip().lower()
        except EOFError:
            state.request_quit()
            break

        if not line:
            continue

        if line == "r":
            state.request_reset()
        elif line == "quit":
            state.request_quit()
            break
        else:
            print("Unknown command.")


class TeleopPolicy:
    def __init__(self, raw_env, base_policy, state: TeleopState):
        self.raw_env = raw_env
        self.base_policy = base_policy
        self.state = state

    def __call__(self, obs):
        if self.state.consume_reset():
            self.raw_env.reset()

        with torch.no_grad():
            return self.base_policy(obs)


def main():
    env_cfg = load_env_cfg(TASK, play=True)
    env_cfg.scene.num_envs = 1

    raw_env = ManagerBasedRlEnv(cfg=env_cfg, device=DEVICE, render_mode=None)
    agent_cfg = load_rl_cfg(TASK)
    env = RslRlVecEnvWrapper(raw_env, clip_actions=agent_cfg.clip_actions)

    runner_cls = load_runner_cls(TASK)
    runner = runner_cls(env, asdict(agent_cfg), device=DEVICE)
    runner.load(CHECKPOINT_PATH, load_cfg={"actor": True}, strict=True, map_location=DEVICE)
    base_policy = runner.get_inference_policy(device=DEVICE)

    state = TeleopState()
    input_thread = threading.Thread(target=teleop_input_loop, args=(state,), daemon=True)
    input_thread.start()

    policy = TeleopPolicy(raw_env, base_policy, state)

    try:
        ViserPlayViewer(env, policy).run()
    finally:
        state.request_quit()
        env.close()


if __name__ == "__main__":
    main()