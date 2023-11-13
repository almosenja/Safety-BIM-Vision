import cv2
import numpy as np

def get_projection_matrix():
    """
    Return a homography matrix for camera projection.
    """
    # Interest points in camera (pixel)
    top_left_point = (1487, 620)
    bottom_left_point = (1625, 310)
    top_right_point = (783, 420)
    bottom_right_point = (1229, 270)

    # Interest points in BIM coordinates (Project coordinates)
    top_left = (96000, 1110)
    bottom_left = (84000, 1110)
    top_right = (96000, 7700)
    bottom_right = (84000, 7700)

    # Get perspective transformation matrix
    pts1 = np.float32([top_left_point, bottom_left_point, top_right_point, bottom_right_point])
    pts2 = np.float32([top_left, bottom_left, top_right, bottom_right])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    return np.array(matrix)