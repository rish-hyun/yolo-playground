from typing import NamedTuple, Self

import numpy as np

from common.utils.convert import hex_to_rgb, rgb_to_hex

from .constants import (
    DARK_BACKGROUND_COLORS,
    DARK_TEXT_COLOR,
    DEFAULT_PALETTE,
    KEYPOINT_COLORS,
    LIGHT_BACKGROUND_COLORS,
    LIGHT_TEXT_COLOR,
    LIMB_COLORS,
    POSE_PALETTE,
    SKELETON_KEYPOINTS,
)


class Color(NamedTuple):
    r: int
    g: int
    b: int

    @classmethod
    def pick(cls, i: int) -> Self:
        return cls(*hex_to_rgb(DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)]))

    @classmethod
    def light(cls) -> Self:
        return cls(*hex_to_rgb(LIGHT_TEXT_COLOR))

    @classmethod
    def dark(cls) -> Self:
        return cls(*hex_to_rgb(DARK_TEXT_COLOR))

    def is_light(self) -> bool:
        return self in LIGHT_BACKGROUND_COLORS

    def is_dark(self) -> bool:
        return self in DARK_BACKGROUND_COLORS
