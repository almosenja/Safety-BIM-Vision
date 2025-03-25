# Worker Safety Twin

This is repository of paper **"Advancing construction site workforce safety monitoring through BIM and computer vision integration"**.

The project combines Building Information Modeling (BIM) and computer vision technology to facilitate both real-time and non-real-time monitoring of construction sites.

## Implementation
The system implementation contains 3 main modules:

### 1. Vision-based module
`vision_module/run.py` contains computer vision related module for data collection:
* Object detection and classification - [YOLOv8](https://github.com/ultralytics/ultralytics "YOLOv8 GitHub")
* Object tracking - [SORT](https://github.com/abewley/sort "SORT GitHub")
* Perspective projection
* Store data into database

### 2. Data integration module
In this step, we utilized Sqlite to store the data collected from computer vision module. The database named as `data.db` and contains two tables:
* temp_data - for real-time monitoring
* history_data - for non-real-time monitoring

Both of the tables are formatted as follows:
> - person_id (int): object tracker id
> - cam_id (int): camera id
> - floor (int): camera location floor
> - datetime (varchar): data collection time
> - x_location (int): BIM x coordinate after projection
> - y_location (int): BIM y coordinate after projection
> - classification (int): worker safety catogory

### 3. BIM visualization module
This study utilizes Autodesk Revit for the BIM module. Revit includes a built-in visual programming interface, Dynamo, which we employed for preprocessing data from the database and subsequent visualization.

The images of the Dynamo code can be viewed at:
* `BIM_module/DYNAMO_real_time_data_visualization.png` for real-time data
* `BIM_module/DYNAMO_historical_data_visualization.png` for non-real-time data

## Dataset
The object detection dataset contains 3,455 images and randomly split into training, validation, and testing datasets with ratios of 83, 12, and 5%.

The labeling class includes:
> * w - worker only
> * wh - worker using helmet
> * wv - worker using vest
> * whv - worker using helmet and vest

## Accuracy
**Object detection accuracy**
|Class|Precision (%)|Recall (%)|AP@50 (%)|
|-----|------------|---------|--------|
|W    |88.1        |87.3     |90.8    |
|WH   |85.0        |82.7     |87.6    |
|WV   |92.6        |93.7     |96.0    |
|WHV  |87.5        |93.4     |94.9    |
|**Overall**|**88.3**|**89.3**|**92.3**|

**Projection accuracy**

Mean error distance (MED) = 13.2 cm

## Demo
#### Example of real-time visualization
![real-time-testing](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/76cdb2f0-c522-438c-9738-2deffccc55b8)

#### Example of historical data visualization
![historical-visualization](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/57ea26d5-5a15-4ecc-ae6e-8f4717e93936)

#### Example of data shown in BIM
![data-display](https://github.com/almosenja/Safety-BIM-Vision/assets/94098493/819a1841-369c-4756-a4ff-9e81961a4193)

## Citation
```bibtex
@article{kulinan2024advancing,
  title={Advancing construction site workforce safety monitoring through BIM and computer vision integration},
  author={Kulinan, Almo Senja and Park, Minsoo and Aung, Pa Pa Win and Cha, Gichun and Park, Seunghee},
  journal={Automation in Construction},
  volume={158},
  pages={105227},
  year={2024},
  publisher={Elsevier}
}
