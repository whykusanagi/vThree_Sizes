# vThree_Sizes Character Measurement Calculation
Calculator for vtubers to determine their 3 sizes accurately.
This notebook processes an anime character image to extract height, bust, waist, underbust, and hip measurements using Mediapipe Pose.

# How to Use the Notebook

## Prerequisites

Ensure the following Python libraries are installed:

- `opencv-python`
- `numpy`
- `mediapipe`
- `matplotlib`
- `pandas`

Install them using pip:
bash
```
pip install opencv-python numpy mediapipe matplotlib pandas
```
Steps to Use

1. Prepare the Input Image
- Save the character image in the specified path in the code (default: "/mnt/data/Corrupted_fullbody.png").

2. Run the Notebook
- Open the notebook in Jupyter, VSCode, or any Python notebook environment.
- Execute the cells in sequence to:
- Process the image.
- Extract character measurements (height, bust, waist, underbust, hip).
- Calculate the estimated cup size using refined thresholds.

3. View Outputs
- The notebook will generate:
- A table displaying all measurements in centimeters.
- The estimated cup size for each outfit variation.
- Visual annotations of the character image for validation.

4. Customization
- Modify the image_path or reference height in the code as needed.
- Adjust the measurement thresholds in the cup size calculation section to fit your specific use case.

Notes
- The cup size calculation uses standard thresholds based on the difference between bust and underbust measurements.
- Ensure the image contains a full-body view of the character for accurate results.


### Conversion Explanation
- The reference character height is set to **175 cm**. As my character is tall and based on the male vtuber model she is derived from.
- The **Nude** height in pixels (1410 pixels) is used as the baseline for conversion.
- The **cm/pixel ratio** is calculated as:
  
  \[
  cm\_per\_pixel = \frac{175}{1410} \approx 0.1241 \text{ cm/pixel}
  \]

You can change the calculation as needed, but if your character is smaller you can adjust the parameter to the average height.
The average American woman is approximately 5 feet 4 inches (162.5 cm) according to the CDC.

### Cup Size Calculation
- Cup size is determined by the difference between the bust and underbust measurements, following standard thresholds:
  - **AA**: 1.0-2.5 cm
  - **A**: 2.6-3.5 cm
  - **B**: 3.6-5.0 cm
  - **C**: 5.1-6.5 cm
  - **D**: 6.6-8.0 cm
  - **DD/E**: 8.1-9.5 cm
  - **F**: 9.6-11.0 cm
  - **G**: 11.1-12.5 cm
  - **H**: 12.6-14.0 cm

### Output Data Table
The final table provides measurements in centimeters for each outfit variation, including the estimated cup size.

If you found this tool helpful, donate so I can spend more time building random projects like this for the community. 
![Donate](https://s3.whykusanagi.xyz/Simple_Header_Image.png)(https://streamelements.com/whykusanagi/tip)
