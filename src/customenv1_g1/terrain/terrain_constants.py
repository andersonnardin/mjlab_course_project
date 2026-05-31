import mjlab.terrains as terrain_gen
from mjlab.terrains import TerrainImporterCfg
from mjlab.terrains.terrain_generator import TerrainGeneratorCfg


OBSTACLE_TERRAIN_CFG = TerrainGeneratorCfg(
    size=(6.0, 6.0),
    border_width=6.0,
    num_rows=5,
    num_cols=5,
    sub_terrains={
        # Stairs going up
        "stairs_up": terrain_gen.BoxPyramidStairsTerrainCfg(
            proportion=0.2,
            step_height_range=(0.05, 0.2),
            step_width=0.4,
            platform_width=2.0,
            border_width=0.3,
        ),

        # Stairs going down (inverted)
        "stairs_down": terrain_gen.BoxInvertedPyramidStairsTerrainCfg(
            proportion=0.2,
            step_height_range=(0.05, 0.2),
            step_width=0.4,
            platform_width=2.0,
            border_width=0.3,
        ),

        # Random stair blocks (irregular)
        "random_stairs": terrain_gen.BoxRandomStairsTerrainCfg(
            proportion=0.15,
            step_width=0.6,
            step_height_range=(0.05, 0.25),
            platform_width=1.5,
            border_width=0.3,
        ),

        # Random obstacles (walls / blocks)
        "obstacles": terrain_gen.BoxRandomSpreadTerrainCfg(
            proportion=0.15,
            num_boxes=20,
            box_width_range=(0.2, 1.0),
            box_length_range=(0.2, 2.0),
            box_height_range=(0.1, 0.4),
            platform_width=1.5,
            border_width=0.3,
        ),

        # Stepping stones (jumping terrain)
        "stepping_stones": terrain_gen.BoxSteppingStonesTerrainCfg(
            proportion=0.15,
            stone_size_range=(0.4, 0.8),
            stone_distance_range=(0.2, 0.5),
            stone_height=0.2,
            stone_height_variation=0.1,
            stone_size_variation=0.2,
            displacement_range=0.1,
            floor_depth=2.0,
            platform_width=1.5,
            border_width=0.3,
        ),

        # Narrow beams (balance challenge)
        "narrow_beams": terrain_gen.BoxNarrowBeamsTerrainCfg(
            proportion=0.15,
            num_beams=8,
            beam_width_range=(0.2, 0.6),
            beam_height=0.2,
            spacing=0.8,
            platform_width=1.5,
            border_width=0.3,
            floor_depth=2.0,
        ),
    },
    add_lights=True,
)


def custom_terrain_cfg(num_envs: int = 1) -> TerrainImporterCfg:
    return TerrainImporterCfg(
        terrain_type="generator",
        terrain_generator=OBSTACLE_TERRAIN_CFG,
        max_init_terrain_level=3,
        num_envs=num_envs,
    )