import cv2
import numpy as np

def get_projection_matrix():
    """
    Return a homography matrix for camera projection.
    """
    # Interest points in camera (pixel)
    top_left_point = [1558, 907]
    bottom_left_point = [1347, 742]
    top_right_point = [367, 822]
    bottom_right_point = [731, 723]

    # Interest points in BIM coordinates (Project coordinates)
    top_left = (12118, 30325)
    bottom_left = (12118, 24325)
    top_right = (20816, 30325)
    bottom_right = (20816, 24325)

    # Get perspective transformation matrix
    pts1 = np.float32([top_left_point, bottom_left_point, top_right_point, bottom_right_point])
    pts2 = np.float32([top_left, bottom_left, top_right, bottom_right])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    return np.array(matrix)