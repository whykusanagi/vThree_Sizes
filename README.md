# vThree_Sizes - VTuber Character Measurement Calculator

**Automated 3-size measurement calculator for VTuber characters using MediaPipe Pose detection**

[![GitHub](https://img.shields.io/badge/GitHub-whykusanagi-blue)](https://github.com/whykusanagi/vThree_Sizes)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/whykusanagi/vThree_Sizes/blob/main/Vtuber_3_Sizes_Estimator.ipynb)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview

A Jupyter notebook that processes anime character images to extract accurate body measurements (height, bust, waist, underbust, hip) and estimate cup size using MediaPipe Pose detection. Designed for VTuber creators who need precise measurements for character design, costume creation, or 3D modeling.

## Features

- **Automated Measurement**: Extract measurements from character images automatically
- **MediaPipe Integration**: Uses Google's MediaPipe Pose for accurate keypoint detection
- **Cup Size Estimation**: Calculates cup size based on bust-underbust difference
- **Batch Processing**: Process multiple images in a folder simultaneously
- **Visual Annotations**: Generates annotated images showing detected keypoints
- **Google Colab Ready**: Works seamlessly in Google Colab environment

## Quick Start

### Prerequisites

- Python 3.7+
- Jupyter Notebook or Google Colab
- Required libraries: `opencv-python`, `numpy`, `mediapipe`, `matplotlib`, `pandas`

### Installation

#### Google Colab (Recommended)

1. Click the "Open in Colab" badge above
2. Upload your character images to `/content/` folder
3. Run all cells

#### Local Setup

```bash
# Install dependencies
pip install opencv-python numpy mediapipe matplotlib pandas

# Or using conda
conda install opencv numpy matplotlib pandas
pip install mediapipe
```

### Usage

1. **Prepare Images**:
   - Save character images in the specified folder (default: `/content/` for Colab)
   - Images should show full-body view for accurate measurements
   - Supported formats: PNG, JPG, JPEG

2. **Run the Notebook**:
   - Execute cells in sequence
   - The notebook will:
     - Process all images in the folder
     - Extract pose keypoints using MediaPipe
     - Calculate measurements (height, bust, waist, underbust, hip)
     - Estimate cup size
     - Generate a results table

3. **View Results**:
   - Measurements displayed in centimeters
   - Cup size estimation for each outfit variation
   - Annotated images showing detected keypoints

## How It Works

### Measurement Extraction

1. **Pose Detection**: MediaPipe Pose detects 33 body keypoints
2. **Keypoint Extraction**: Identifies specific landmarks (shoulders, hips, etc.)
3. **Width Calculation**: Measures horizontal distances between keypoints
4. **Circumference Estimation**: Converts widths to circumferences using π/2 formula
5. **Unit Conversion**: Converts pixel measurements to centimeters using reference height

### Cup Size Calculation

Cup size is determined by the difference between bust and underbust measurements:

| Difference | Cup Size |
|------------|----------|
| 1.0-2.5 cm | AA |
| 2.6-3.5 cm | A |
| 3.6-5.0 cm | B |
| 5.1-6.5 cm | C |
| 6.6-8.0 cm | D |
| 8.1-9.5 cm | DD/E |
| 9.6-11.0 cm | F |
| 11.1-12.5 cm | G |
| 12.6-14.0 cm | H |

### Reference Height

The default reference height is **175 cm** (based on a tall character model). You can adjust this in the code:

```python
# Change reference height (in cm)
reference_height = 162.5  # Average American woman height
```

The cm/pixel ratio is calculated as:
```
cm_per_pixel = reference_height / nude_height_pixels
```

## Architecture & Data Flow

```mermaid
flowchart TD
  A[Input Images<br/>(PNG/JPG)] --> B[MediaPipe Pose]
  B --> C[Keypoint Extraction]
  C --> D[Measurement Engine]
  D --> E[Reference Height Converter]
  E --> F[Results Table + Annotations]
```

- **Input layer:** Outfit renders or promotional art dropped into `/content/`.
- **Inference layer:** MediaPipe Pose finds 33 landmarks per frame.
- **Computation layer:** Width deltas feed the circumference calculator and cup-size estimator.
- **Output layer:** Pandas aggregates measurements, Matplotlib/OpenCV annotate each sample for QA.

## Customization

### Adjusting Reference Height

Modify the reference height in the conversion calculation:

```python
converted_measurements = {
    key: round(value * (175 / 1410), 1)  # Change 175 to your character's height
    for key, value in measurements.items()
}
```

### Changing Image Folder

Update the `image_folder` variable:

```python
image_folder = "/path/to/your/images/"
```

### Cup Size Thresholds

Modify the `refine_estimate_cup_size` function to adjust cup size ranges:

```python
refined_cup_sizes = {
    (1.0, 2.5): "AA",
    (2.6, 3.5): "A",
    # ... add or modify ranges
}
```

## Docker & Execution Model

- **Primary workflow:** Google Colab (GPU-enabled) is the canonical runtime so contributors get prebuilt Mediapipe/OpenCV wheels.
- **Local fallback:** Use the dependency list above and record OS-specific tweaks. Notebook execution outside Colab is allowed but you must capture any deviation in your PR summary per `CLAUDE.md`.
- **Docker exception:** Because this is a research notebook, there is no official Docker image yet. If you containerize it, document the image choice and GPU requirements in an ADR so future users can reproduce it.

## Output Format

The notebook generates a pandas DataFrame with measurements for each image:

```
                  Height  Bust Circumference  Waist Circumference  \
image1.png       175.0                48.2                 32.9   
image2.png       177.9                47.0                 34.5   

                  Underbust Circumference  Hip Circumference Cup Size  
image1.png                         32.0               32.9        J  
image2.png                         33.5               34.5        H  
```

## Limitations

- **Pose Detection**: Requires clear full-body view; may struggle with unusual poses
- **Measurement Accuracy**: Estimates based on 2D images; 3D measurements may vary
- **Clothing Effects**: Measurements may be affected by clothing or outfit variations
- **Reference Height**: Accuracy depends on correct reference height calibration

## Testing & Validation

- **Date:** 2025-01-26
- **Device:** macOS (Apple Silicon), Python 3.11
- **Dependency install:** `pip install mediapipe opencv-python numpy matplotlib pandas` (resolver warning re: protobuf 4.25.8 vs 5.26.1, non-blocking)
- **Smoke test:**

```text
$ python3 - <<'PY'
import importlib
for pkg in ["cv2","numpy","mediapipe","matplotlib","pandas"]:
    importlib.import_module(pkg)
    print(f"{pkg} ok")
PY

Smoke test results:
 - cv2: ok
 - numpy: ok
 - mediapipe: ok
 - matplotlib: ok
 - pandas: ok
```

This confirms the notebook’s required libraries load successfully in a clean environment. If protobuf conflicts arise, pin protobuf ≥5.26.1 or run inside Colab where the stack is pre-synchronized.

## Contributing

Contributions welcome! Please:
1. Improve measurement accuracy algorithms
2. Add support for additional measurement types
3. Enhance cup size calculation logic
4. Add error handling and validation
5. Submit a pull request

## Related Projects

- [Corrupted Theme](https://github.com/whykusanagi/corrupted-theme) - Glassmorphic design system
- [VTuberHub](https://github.com/whykusanagi/VTuberHub) - Facial tracking relay for VTubers

## License

MIT License - see LICENSE file for details

## Support

For questions or issues:
- Open an issue on GitHub
- Join the Discord: [whykusanagi.xyz/links](https://whykusanagi.xyz/links)

## Donations

If you found this tool helpful, consider supporting development:
[Donate via StreamElements](https://streamelements.com/whykusanagi/tip)

---

**Made with 💎 by [whykusanagi](https://whykusanagi.xyz)**

## Code Quality Notes

### Areas for Improvement

- **Error Handling**: Add try-catch blocks for image processing failures
- **Validation**: Validate image formats and pose detection success
- **Documentation**: Add docstrings to functions
- **Modularization**: Split into separate functions/modules for better organization
- **Testing**: Add unit tests for measurement calculations
- **Configuration**: Move hardcoded values (reference height, thresholds) to config
- **Output Format**: Add option to export results as CSV/JSON
