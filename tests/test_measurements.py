from measurements import (
    MeasurementConfig,
    centimeters_per_pixel,
    estimate_body_circumferences,
    estimate_cup_size,
)


class DummyLandmarks:
    LEFT_SHOULDER = type("L", (), {"value": 0})
    RIGHT_SHOULDER = type("R", (), {"value": 1})
    LEFT_HIP = type("Lh", (), {"value": 2})
    RIGHT_HIP = type("Rh", (), {"value": 3})
    LEFT_ANKLE = type("La", (), {"value": 4})
    NOSE = type("N", (), {"value": 5})


def test_centimeters_per_pixel():
    assert round(centimeters_per_pixel(1410, 175), 4) == 0.1241


def test_estimate_body_circumferences():
    keypoints = {
        0: (100, 10),  # left shoulder
        1: (200, 10),  # right shoulder
        2: (110, 50),  # left hip
        3: (190, 50),  # right hip
    }
    cm_per_px = centimeters_per_pixel(1000, 175)
    config = MeasurementConfig()
    res = estimate_body_circumferences(keypoints, cm_per_px, config, DummyLandmarks)
    assert res["Bust Circumference"] > res["Underbust Circumference"]
    assert res["Hip Circumference"] > 0


def test_estimate_cup_size():
    assert estimate_cup_size(90, 82) == "D"
    assert estimate_cup_size(82, 82) == "Unknown"

