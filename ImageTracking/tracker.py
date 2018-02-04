import numpy as np
import cv2
import cv2.aruco as aruco

#connect to webcam
cap = cv2.VideoCapture(0)

#load calibration constants for camera
camera_calib_mtx = np.load('camera_calib_mtx.npy')
camera_calib_dist = np.load('camera_calib_dist.npy')

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()

#generate 2-aruco pattern
board = cv2.aruco.Board_create([np.array([[0.025, 0.05 ,0.],[0.125, 0.05, 0. ],[0.125, -0.05, 0.],[0.025, -0.05, 0.]], dtype=np.float32),
                                np.array([[-0.125, 0.05 ,0.],[-0.025, 0.05, 0. ],[-0.025, -0.05, 0.],[-0.125, -0.05, 0.]], dtype=np.float32)], 
                                aruco_dict, np.array([0,1]))

#constant keeping track of screenshots taken
screenshot_n=0
    
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #detect the corners and ids of all the aruco markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    
    #if we detected some stuff
    success = False
    if (ids is not None):
        success, rvec, tvec = cv2.aruco.estimatePoseBoard(corners, ids, board, camera_calib_mtx, camera_calib_dist)

    try:
        if (success):
            #current rotation returned in axis-angle representation.  See Wikipedia for helpful treatment
            #we want to convert to euler angles, and are only interested in rotation about z
            angle = np.linalg.norm(rvec)
            axis = rvec/angle
            s = np.sin(angle)
            c = np.cos(angle)
            t = 1-c
            z_angle = np.arctan2(axis[2]*s - axis[1]*axis[0]*t, 1-(axis[2]**2 + axis[0]**2)*t)
            print tvec
            #draw axes
            frame = aruco.drawAxis(frame, camera_calib_mtx, camera_calib_dist, np.array([0,0,z_angle], np.float32), tvec, 0.1)
    except TypeError:
        print "no markers detected"
    

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    
    #wait for an ms and get key press.  Must pass at least (1) to provide processing time
    key_pressed = cv2.waitKey(1)
    if  key_pressed & 0xFF == ord('q'):
        break
    elif key_pressed & 0xFF == ord('s'):
        print "taking picture..."
        #write the current screen to file
        cv2.imwrite("img"+str(screenshot_n)+".jpg", frame)
        screenshot_n += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
