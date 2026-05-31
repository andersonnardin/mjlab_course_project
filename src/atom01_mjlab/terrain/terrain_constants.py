import mjlab.terrains as terrain_gen
from mjlab.terrains import TerrainImporterCfg
from mjlab.terrains.terrain_generator import TerrainGeneratorCfg


ATOM01_ROUGH_TERRAIN_CFG = TerrainGeneratorCfg(
    size=(8.0, 8.0),
    border_width=8.0,
    num_rows=8,
    num_cols=8,
    sub_terrains={
        "pyramid_slope": terrain_gen.HfPyramidSlopedTerrainCfg(
            proportion=0.40,
            slope_range=(0.05, 0.15),
        ),
        "random_rough": terrain_gen.HfRandomUniformTerrainCfg(
            proportion=0.40,
            noise_range=(0.0, 0.05),
            noise_step=0.01,
            downsampled_scale=0.2,
        ),
        "wave_terrain": terrain_gen.HfWaveTerrainCfg(
            proportion=0.20,
            amplitude_range=(0.02, 0.06),
            num_waves=2,
        ),
    },
    add_lights=True,
)


def atom01_rough_terrain_cfg(num_envs: int = 1) -> TerrainImporterCfg:
    return TerrainImporterCfg(
        terrain_type="generator",
        terrain_generator=ATOM01_ROUGH_TERRAIN_CFG,
        max_init_terrain_level=3,
        num_envs=num_envs,
    )