from pathlib import Path
import mujoco

from mjlab.entity.entity import EntityCfg

_THIS_DIR = Path(__file__).resolve().parent


def _load_xml(name: str) -> mujoco.MjSpec:
    return mujoco.MjSpec.from_file(str(_THIS_DIR / "xmls" / name))


def make_fixed_cfg(
    xml_name: str,
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return EntityCfg(
        spec_fn=lambda: _load_xml(xml_name),
        init_state=EntityCfg.InitialStateCfg(
            pos=pos,
            rot=rot,
        ),
    )


def make_free_cfg(
    xml_name: str,
    body_name: str,
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    def _spec_fn() -> mujoco.MjSpec:
        spec = _load_xml(xml_name)

        target_body = None
        for body in spec.bodies:
            if body.name == body_name:
                target_body = body
                break

        if target_body is None:
            raise ValueError(
                f"Body '{body_name}' not found in XML '{xml_name}'"
            )

        target_body.pos[:] = pos
        target_body.quat[:] = rot

        return spec

    return EntityCfg(spec_fn=_spec_fn)


# -------------------------------------------------------------------
# Fixed primitive objects
# -------------------------------------------------------------------

def get_box_cfg(
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("box.xml", pos, rot)


def get_ramp_cfg(
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("ramp.xml", pos, rot)


def get_cylinder_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("cylinder.xml", pos, rot)


def get_sphere_cfg(
    pos=(0.0, 0.0, 0.5),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("sphere.xml", pos, rot)


def get_capsule_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("capsule.xml", pos, rot)


def get_ellipsoid_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("ellipsoid.xml", pos, rot)

def get_plane_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("plane.xml", pos, rot)

def get_wall_cfg(
    pos=(0.0, 0.0, 2.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("wall.xml", pos, rot)


def get_ball_pit_cfg(
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("ball_pit.xml", pos, rot)


# -------------------------------------------------------------------
# Dynamic freejoint objects
# -------------------------------------------------------------------

def get_sphere_red_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_free_cfg("sphere_red.xml", "sphere_body", pos, rot)



def get_sphere_blue_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_free_cfg("sphere_blue.xml", "sphere_body", pos, rot)


def get_sphere_green_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_free_cfg("sphere_green.xml", "sphere_body", pos, rot)


def get_sphere_yellow_cfg(
    pos=(0.0, 0.0, 1.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_free_cfg("sphere_yellow.xml", "sphere_body", pos, rot)


def get_grass_field_cfg(
    pos=(0.0, 0.0, 0.0),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_fixed_cfg("grass_field.xml", pos, rot)


def get_football_cfg(
    pos=(0.0, 0.0, 0.5),
    rot=(1.0, 0.0, 0.0, 0.0),
) -> EntityCfg:
    return make_free_cfg("football.xml", "football_body", pos, rot)