import numpy as np
import cv2
import cv2.aruco as aruco

#connect to webcam
cap = cv2.VideoCapture(0)

#load calibration constants for camera
camera_calib_mtx = np.load('camera_calib_mtx.npy')
camera_calib_dist = np.load('camera_calib_dist.npy')


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    rvecs, tvecs, pts = aruco.estimatePoseSingleMarkers(corners, 0.03, camera_calib_mtx, camera_calib_dist)

    try:
        gray = aruco.drawDetectedMarkers(gray, corners)
        gray = aruco.drawAxis(gray, camera_calib_mtx, camera_calib_dist, rvecs[0], tvecs[0], 0.03)
    except TypeError:
        print "no markers detected"

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
