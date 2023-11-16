# Vision Module
Vision module processes raw video data for storage in a database.

![vision_flowchart](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/ef67185e-54d5-44fa-84b3-80dfa5ce3121)

## Implementation
1. Train the dataset according to the [YOLOv8](https://docs.ultralytics.com/modes/train/ "YOLOv8 Training"). The pretrained weight used in the case study can be downloaded from [here](https://drive.google.com/file/d/1eIaZ2FTxxMD1w7tQh6qLmMlzAjWHrVFx/view?usp=sharing).
2. Set up dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Run the model with:

   ```
   python run.py --input_path <input_video> --output_path <output_video> --model_weight <model_weight> --zone_path <zone_path_csv>
   ```

Sample video utilized in the case study can be downloaded [here](https://drive.google.com/file/d/179CdYzoFXanoH5mkq5Bu4v-InTrixpEj/view?usp=sharing).

## Transformation Matrix
The transformation matrix we use is based on the scenario depicted in this figure:
![scenario](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/4dfde4b2-89ff-41cb-98ad-d39f1e35cc3c)

To obtain the transformation matrix, modify the values in `perspective_transformation.py` as follows:
```Python
# Interest points in camera (pixel)
top_left_point = (1487, 620)      # (u1, v1)
bottom_left_point = (1625, 310)   # (u3, v3)
top_right_point = (783, 420)      # (u2, v2)
bottom_right_point = (1229, 270)  # (u4, v4)

# Interest points in BIM coordinates (project coordinates)
top_left = (96000, 1110)      # (x1, y1)
bottom_left = (84000, 1110)   # (x3, y3)
top_right = (96000, 7700)     # (x2, y2)
bottom_right = (84000, 7700)  # (x4, y4)
```

## Note
Please note that the codes are specifically designed for the case study in our research. Please adjust it according to your specific requirements.
