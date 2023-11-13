# BIM Module
BIM module consists data preprocessing obtained from vision-based module and visualize it.
![BIM_flowchart](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/713fa066-f674-4219-abd1-ae3374efbcc9)

## Implementation
To run the code, we need Dynamo code add-ons as follows:
> * Slingshot
> * archilab

We also need to import the "worker" and "trail" families:
* `worker.rfa` - 3D family that represent worker model
* `trail.rfa` - 3D family that represent worker's track (for non-real-time visualization)

Workers will automatically classified based on the category obtained in risk assessment step (see the paper). These categories were hard-coded using Python in Dynamo:
* `risk_assessment_low_elevation.py` - worker floor location < 1.8 m
* `risk_assessment_high_elevation.py` - worker floor location ≥  1.8 m
