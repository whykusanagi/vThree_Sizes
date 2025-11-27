"""Core measurement utilities for vThree_Sizes.

The notebook now imports these helpers so we can unit test the math outside
Colab and avoid duplicating logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


# Default ratio between bust and underbust circumferences.
UNDERBUST_RATIO = 0.88


@dataclass
class MeasurementConfig:
    """Configuration for converting pixel distances to centimeters."""

    reference_height_cm: float = 175.0
    circle_multiplier: float = np.pi / 2  # approximates half-ellipse circumference
    underbust_ratio: float = UNDERBUST_RATIO


def centimeters_per_pixel(height_px: float, reference_height_cm: float) -> float:
    if height_px <= 0:
        raise ValueError("height_px must be positive to compute scale")
    return reference_height_cm / height_px


def width_to_circumference(width_px: float, cm_per_pixel: float, multiplier: float) -> float:
    return round(width_px * cm_per_pixel * multiplier, 2)


def estimate_body_circumferences(
    keypoints: Dict[int, Tuple[int, int]],
    cm_per_pixel: float,
    config: MeasurementConfig,
    landmark_enum=None,
) -> Dict[str, float]:
    """Convert keypoint widths to circumferences."""
    def width(a: int, b: int) -> float:
        return abs(keypoints[a][0] - keypoints[b][0])

    if landmark_enum is None:
        from mediapipe.python.solutions.pose import PoseLandmark as landmark_enum

    bust = width(landmark_enum.LEFT_SHOULDER.value, landmark_enum.RIGHT_SHOULDER.value)
    waist = width(landmark_enum.LEFT_HIP.value, landmark_enum.RIGHT_HIP.value)
    hip = width(landmark_enum.LEFT_HIP.value, landmark_enum.RIGHT_HIP.value)

    bust_circ = width_to_circumference(bust, cm_per_pixel, config.circle_multiplier)
    waist_circ = width_to_circumference(waist, cm_per_pixel, config.circle_multiplier)
    hip_circ = width_to_circumference(hip, cm_per_pixel, config.circle_multiplier)
    underbust_circ = round(bust_circ * config.underbust_ratio, 2)

    return {
        "Bust Circumference": bust_circ,
        "Waist Circumference": waist_circ,
        "Underbust Circumference": underbust_circ,
        "Hip Circumference": hip_circ,
    }


CUP_THRESHOLDS = [
    ((1.0, 2.5), "AA"),
    ((2.6, 3.5), "A"),
    ((3.6, 5.0), "B"),
    ((5.1, 6.5), "C"),
    ((6.6, 8.0), "D"),
    ((8.1, 9.5), "DD/E"),
    ((9.6, 11.0), "F"),
    ((11.1, 12.5), "G"),
    ((12.6, 14.0), "H"),
    ((14.1, 16.0), "I"),
    ((16.1, 18.0), "J"),
    ((18.1, 20.0), "K"),
    ((20.1, 22.0), "L"),
    ((22.1, 24.0), "M"),
    ((24.1, 26.0), "N"),
    ((26.1, 28.0), "O"),
]


def estimate_cup_size(bust_cm: float, underbust_cm: float) -> str:
    diff = bust_cm - underbust_cm
    for (lower, upper), label in CUP_THRESHOLDS:
        if lower <= diff <= upper:
            return label
    return "Unknown"

