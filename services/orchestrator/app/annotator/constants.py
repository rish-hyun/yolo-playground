DEFAULT_PALETTE: list[str] = [
    "#042AFF",
    "#0BDBEB",
    "#F3F3F3",
    "#00DFB7",
    "#111F68",
    "#FF6FDD",
    "#FF444F",
    "#CCED00",
    "#00F344",
    "#BD00FF",
    "#00B4FF",
    "#DD00BA",
    "#00FFFF",
    "#26C000",
    "#01FFB3",
    "#7D24FF",
    "#7B0068",
    "#FF1B6C",
    "#FC6D2F",
    "#A2FF0B",
]

POSE_PALETTE: list[str] = [
    "#FF8000",
    "#FF9933",
    "#FFB266",
    "#E6E600",
    "#FF99FF",
    "#99CCFF",
    "#FF66FF",
    "#FF33FF",
    "#66B2FF",
    "#3399FF",
    "#FF9999",
    "#FF6666",
    "#FF3333",
    "#99FF99",
    "#66FF66",
    "#33FF33",
    "#00FF00",
    "#0000FF",
    "#FF0000",
    "#FFFFFF",
]

_limb_color_indices = [9, 9, 9, 9, 7, 7, 7, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16]
LIMB_COLORS: list[str] = [POSE_PALETTE[i] for i in _limb_color_indices]

_kpt_color_indices = [16, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9]
KEYPOINT_COLORS: list[str] = [POSE_PALETTE[i] for i in _kpt_color_indices]

# Light Colors
LIGHT_TEXT_COLOR: str = "#FFFFFF"
LIGHT_BACKGROUND_COLORS: list[str] = [
    "#FFFF00",
    "#F3F3F3",
    "#0BFFA2",
    "#DD6FFF",
    "#44F300",
    "#B3FF01",
    "#EBDB0B",
    "#B7DF00",
    "#00EDCC",
]

# Dark Colors
DARK_TEXT_COLOR: str = "#681F11"
DARK_BACKGROUND_COLORS: list[str] = [
    "#68007B",
    "#FF2A04",
    "#2F6DFC",
    "#00C026",
    "#FF00BD",
    "#4F44FF",
    "#FFB400",
    "#BA00DD",
    "#FF247D",
    "#681F11",
    "#6C1BFF",
]

SKELETON_KEYPOINTS: list[tuple[int, int]] = [
    (16, 14),
    (14, 12),
    (17, 15),
    (15, 13),
    (12, 13),
    (6, 12),
    (7, 13),
    (6, 7),
    (6, 8),
    (7, 9),
    (8, 10),
    (9, 11),
    (2, 3),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (5, 7),
]
