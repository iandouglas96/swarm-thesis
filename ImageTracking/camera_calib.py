#This code taken verbatim from https://docs.opencv.org/3.3.1/dc/dbb/tutorial_py_calibration.html
#Run with this code inside folder with calibration images (chessboard)

import numpy as np
import cv2
import glob

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
board = cv2.aruco.CharucoBoard_create(5, 7, 0.04, 0.02, aruco_dict);

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
all_corners = [] # 3d point in real world space
all_ids = [] # 2d points in image plane.
images = glob.glob('*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, (7,6), None)
    # If found, add object points, image points (after refining them)
    if len(ids) > 0:
        ret, corners, ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
        if (len(corners) > 0 and len(ids) > 0):
            all_corners.append(corners)
            all_ids.append(ids)
        # Draw and display the corners
        cv2.aruco.drawDetectedCornersCharuco(img, corners, ids)
        cv2.imshow('img', img)
        cv2.waitKey(500)

ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_corners, all_ids, board, (1080, 720), 0, 0)

print mtx
print dist
#save calibration parameters to file
np.save("camera_calib_mtx", mtx)
np.save("camera_calib_dist", dist)

cv2.destroyAllWindows()
