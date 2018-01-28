import numpy as np
import cv2
import cv2.aruco as aruco


'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size

board = cv2.aruco.CharucoBoard_create(5, 7, 0.04, 0.02, aruco_dict);
img = board.draw((1000,1400))
#img = aruco.drawMarker(aruco_dict, 2, 700)
cv2.imwrite("test_marker.jpg", img)

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
