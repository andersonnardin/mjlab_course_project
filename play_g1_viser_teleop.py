import threading
import torch
from dataclasses import asdict

from mjlab.envs.manager_based_rl_env import ManagerBasedRlEnv
from mjlab.tasks.registry import load_env_cfg, load_rl_cfg, load_runner_cls
from mjlab.rl.vecenv_wrapper import RslRlVecEnvWrapper
from mjlab.viewer import ViserPlayViewer
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner


TASK = "Mjlab-Velocity-CustomEnv2-Unitree-G1"
CHECKPOINT_PATH = "./logs/rsl_rl/g1_velocity/2026-05-29_16-39-23/model_1000.pt"
DEVICE = "cuda:0"

LIN_X_STEP = 0.8
LIN_Y_STEP = 0.2
ANG_Z_STEP = 0.35


def set_twist_command(env, cmd: torch.Tensor) -> None:
    cm = env.command_manager

    if hasattr(cm, "set_command"):
        cm.set_command("twist", cmd)
        return

    term = None
    if hasattr(cm, "_terms") and isinstance(cm._terms, dict) and "twist" in cm._terms:
        term = cm._terms["twist"]
    elif hasattr(cm, "terms") and isinstance(cm.terms, dict) and "twist" in cm.terms:
        term = cm.terms["twist"]

    if term is not None:
        for attr in ("command", "command_buf", "commands", "_command", "_command_buf"):
            if hasattr(term, attr):
                target = getattr(term, attr)
                if isinstance(target, torch.Tensor):
                    target.copy_(cmd)
                    return

    raise RuntimeError("Could not override twist command.")


class TeleopState:
    def __init__(self):
        self.lock = threading.Lock()
        self.lin_x = 0.0
        self.lin_y = 0.0
        self.ang_z = 0.0
        self.reset_requested = False
        self.quit_requested = False

    def set_cmd(self, x: float, y: float, z: float):
        with self.lock:
            self.lin_x = x
            self.lin_y = y
            self.ang_z = z

    def get_cmd(self):
        with self.lock:
            return self.lin_x, self.lin_y, self.ang_z

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
    print("\nTeleop commands:")
    print("  w  -> forward")
    print("  s  -> backward")
    print("  a  -> turn left")
    print("  d  -> turn right")
    print("  q  -> strafe left")
    print("  e  -> strafe right")
    print("  x  -> stop")
    print("  r  -> reset env")
    print("  cmd <lin_x> <lin_y> <ang_z>  -> exact command")
    print("  p  -> print current command")
    print("  quit -> exit\n")

    while not state.should_quit():
        try:
            line = input("> ").strip().lower()
        except EOFError:
            state.request_quit()
            break

        if not line:
            continue

        if line == "w":
            state.set_cmd(LIN_X_STEP, 0.0, 0.0)
        elif line == "s":
            state.set_cmd(-LIN_X_STEP, 0.0, 0.0)
        elif line == "a":
            state.set_cmd(0.0, 0.0, ANG_Z_STEP)
        elif line == "d":
            state.set_cmd(0.0, 0.0, -ANG_Z_STEP)
        elif line == "q":
            state.set_cmd(0.0, LIN_Y_STEP, 0.0)
        elif line == "e":
            state.set_cmd(0.0, -LIN_Y_STEP, 0.0)
        elif line == "x":
            state.set_cmd(0.0, 0.0, 0.0)
        elif line == "r":
            state.request_reset()
        elif line == "p":
            x, y, z = state.get_cmd()
            print(f"Current command: lin_x={x:.3f}, lin_y={y:.3f}, ang_z={z:.3f}")
        elif line.startswith("cmd "):
            parts = line.split()
            if len(parts) == 4:
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    state.set_cmd(x, y, z)
                except ValueError:
                    print("Invalid numbers.")
            else:
                print("Usage: cmd <lin_x> <lin_y> <ang_z>")
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
            self.state.set_cmd(0.0, 0.0, 0.0)

        x, y, z = self.state.get_cmd()
        cmd = torch.tensor([[x, y, z]], dtype=torch.float32, device=self.raw_env.device)
        set_twist_command(self.raw_env, cmd)

        with torch.no_grad():
            return self.base_policy(obs)


def main():
    env_cfg = load_env_cfg(TASK, play=True)
    env_cfg.scene.num_envs = 1

    raw_env = ManagerBasedRlEnv(cfg=env_cfg, device=DEVICE, render_mode=None)
    agent_cfg = load_rl_cfg(TASK)

    env = RslRlVecEnvWrapper(raw_env, clip_actions=agent_cfg.clip_actions)

    runner_cls = load_runner_cls(TASK)
    if runner_cls is None:
        runner_cls = VelocityOnPolicyRunner

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