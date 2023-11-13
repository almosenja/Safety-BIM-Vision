import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import math
import numpy as np
import csv
import torch
import db_management


from ultralytics import YOLO
from datetime import datetime
from time import time
from sort import *
from perspective_transformation import get_projection_matrix


def read_points(file_path):
    """
    Load the safe area points from a CSV file.
    """
    with open(file_path, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        points = [(int(float(row[0])), int(float(row[1]))) for row in reader]
    return points


def project_to_plane(bottom_point):
    """
    Project bottom points of bounding boxes to a plane using a perspective transformation matrix.

    Return:
        A tuple of projected BIM coordinates (x, y).
    """
    matrix = get_projection_matrix()
    x = bottom_point[0]
    y = bottom_point[1]
    pts = np.float32([[x, y]])
    pts_projected = cv2.perspectiveTransform(pts[None, :, :], matrix)
    xo = int(pts_projected[0][0][0])
    yo = int(pts_projected[0][0][1])

    return (xo, yo)


def draw_boxes(frame, class_id, class_names, x1, y1, x2, y2, bottom_point):
    """
    Draw bounding boxes and labels on the frame.
    """
    label = str(class_id) + "-" + class_names[class_id]
    color_map = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (0, 155, 255)]
    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color_map[class_id], -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color_map[class_id], 2)
    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.circle(frame, bottom_point, 3, (255, 255, 255), -1)


def safety_category(class_id, projected_coordinate, safe_zone):
    """
    Return safety category for risk assessment of each worker.

    Return:
        category (int): a category/classification of worker condition.
            1: hardhat vest safe zone
            2: hardhat safe zone
            3: vest safe zone
            4: safe zone
            5: hardhat vest
            6: hardhat
            7: vest
            8: -
    """
    inside_safe_zone = cv2.pointPolygonTest(np.array(safe_zone), projected_coordinate, False)
    if inside_safe_zone > 0:
        if class_id == 0:
            category = 4
        elif class_id == 1:
            category = 2
        elif class_id == 2:
            category = 1
        else:
            category = 3
    else:
        if class_id == 0:
            category = 8
        elif class_id == 1:
            category = 6
        elif class_id == 2:
            category = 5
        else:
            category = 7
    
    return category


def run(input_path, output_path, model_path, safe_zone_points_path, confidence=0.5, height_from_bottom=8, db_path="data.db", db_time_interval=1):
    """
    Run YOLOv8 and SORT algorithms and store the data in database.

    Args:
        input_path (str): path to input folder
        output_path (str): path to output folder
        model_path (str): path to model weight (.pt)
        safe_zone_points_path (str): path to safe zone points (.csv)
        confidence (float): confidence score for object detection to detect, default = 0.5
        height_from_bottom (int): height from bottom edge of bounding box, default = 8
        db_path (str): path to database, default = "data.db"
        db_time_interval (int): time interval for data collection in seconds, default = 1
    """
    class_names = ["w", "wh", "whv", "wv"] # These are classes that we use in the study

    # Read the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error while trying to read video.")

    # Create database and tables if not exist
    db_management.create_temp_table(db_path)
    db_management.create_history_table(db_path)

    # Object detection and tracking models
    model = YOLO(model_path)
    tracker = Sort(max_age=25, min_hits=3, iou_threshold=0.2)

    # Saving data to db time interval
    current_time = time.time()
    next_capture_time = current_time + db_time_interval

    # Initiate safe zone if any
    safe_zone = read_points(safe_zone_points_path)

    # Output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (1920, 1080))

    while cap.isOpened():
        ret, frame = cap.read()
        start = time.perf_counter()

        if ret:
            results = model.predict(frame, stream=True)
            detections = np.empty((0, 6))

            # YOLO object detection
            for i in results:
                boxes = i.boxes

                for box in boxes:
                    # Get object detection results
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    class_name = int(box.cls[0])

                    if conf > confidence:
                        current_array = np.array([x1, y1, x2, y2, conf, class_name])
                        detections = np.vstack((detections, current_array))

            # Empty lists to be stored in database
            person_ids = []
            cam_ids = []
            datetimes = []
            floors = []
            projected_coordinates = []
            classifications = []

            # SORT object tracking
            results_tracker = tracker.update(detections)

            for result in results_tracker:
                # Get object tracking results
                x1, y1, x2, y2, = result[:4]
                x1, y1, x2, y2, = int(x1), int(y1), int(x2), int(y2)
                tracker_id = int(result[-1])
                class_id = int(result[4])
                cx = (x1 + x2) // 2
                by = int(y2 - height_from_bottom)
                bp = (cx, by)

                # Visualize bounding box
                draw_boxes(frame, class_id, class_names, x1, y1, x2, y2, bp)

                # Project to plane
                plane_coordinate = project_to_plane(bp)

                # Classify worker based on safety category
                category = safety_category(class_id, plane_coordinate, safe_zone)

                # Prepare data list which going to be stored in database
                person_ids.append(tracker_id)
                cam_ids.append(1) # For this study, we hardcoded this data since there is only 1 camera
                datetimes.append(datetime.now())
                floors.append(3) # For this study, the floor is hardcoded as the camera location
                projected_coordinates.append(plane_coordinate)
                classifications.append(category)

            # Insert all data to database
            x_projected = [item[0] for item in projected_coordinates]
            y_projected = [item[1] for item in projected_coordinates]

            data_array = np.array([person_ids, cam_ids, datetimes, floors, x_projected, y_projected, classifications]).T
            data_for_db = [tuple(data) for data in data_array]

            if time.time() >= next_capture_time:
                try:
                    # The code looks like redundant but it helps prevent error
                    db_management.add_many_temp(db_path, data_for_db)
                    db_management.delete_temp(db_path)
                    db_management.add_many_temp(db_path, data_for_db)
                    db_management.add_many_history(db_path, data_for_db)
                    print("DATA ADDED SUCCESSFULLY")
                except:
                    print("USED PREVIOUS DATA")
                    pass

                # Update the next capture time
                next_capture_time += db_time_interval

            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:
            break

        # Show FPS
        end = time.perf_counter()
        total_time = end - start
        fps = 1 / total_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        cv2.imshow("Construction Scene", frame)
        out.write(frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_path",
                        default=None,
                        help="Folder to input video")
    
    parser.add_argument("-o", "--output_path",
                        default=None,
                        help="Folder for output video")
    
    parser.add_argument("-m", "--model_weight",
                        default=None,
                        help="Path to the trained weight of model")
    
    parser.add_argument("--zone_path",
                        default=None,
                        help="Path to the safe zone points csv file. Note that \
                              the csv file should not have column headings.")
    
    parser.add_argument("-c", "--confidence",
                        default=0.5,
                        help="Confidence score threshold for object detection")
    
    parser.add_argument("--bottom_point",
                        default=8,
                        help="The height of bottom point from bottom part of \
                              bounding box (ground location) of person in \
                              camera. This point will be used for projection.")
    
    parser.add_argument("--db_path",
                        default="data.db",
                        help="Path to the database")
    
    parser.add_argument("--db_time",
                        default=1,
                        help="Time interval which the model will insert into \
                              the database in second. The default is 1 second \
                              which means that the data will be inserted every\
                              1 second.")
    
    args = parser.parse_args()

    # set torch options
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    run(args.input_path,
        args.output_path,
        args.model_weight,
        args.zone_path,
        args.confidence,
        args.bottom_point,
        args.db_path,
        args.db_time)