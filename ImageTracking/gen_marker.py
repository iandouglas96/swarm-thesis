import numpy as np
import cv2
import cv2.aruco as aruco

#grab standard dict of aruco squares (default is fine for us)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

#generate 4-aruco pattern
#board = cv2.aruco.Board_create([np.array([[0.1, 0.1 ,0.],[0.2, 0.1, 0. ],[0.2, 0., 0.],[0.1, 0., 0.]], dtype=np.float32),
#                                np.array([[0., 0.2 ,0.],[0.1, 0.2, 0. ],[0.1, 0.1, 0.],[0., 0.1, 0.]], dtype=np.float32),
#                                np.array([[0.2, 0.2 ,0.],[0.3, 0.2, 0. ],[0.3, 0.1, 0.],[0.2, 0.1, 0.]], dtype=np.float32),
#                                np.array([[0.1, 0.3 ,0.],[0.2, 0.3, 0. ],[0.2, 0.2, 0.],[0.1, 0.2, 0.]], dtype=np.float32)], 
#                                aruco_dict, np.array([0,1,2,3]))

board = cv2.aruco.Board_create([np.array([[0.025, 0.05 ,0.],[0.125, 0.05, 0. ],[0.125, -0.05, 0.],[0.025, -0.05, 0.]], dtype=np.float32),
                                np.array([[-0.125, 0.05 ,0.],[-0.025, 0.05, 0. ],[-0.025, -0.05, 0.],[-0.125, -0.05, 0.]], dtype=np.float32)], 
                                aruco_dict, np.array([0,1]))
print board.objPoints
img = cv2.aruco.drawPlanarBoard(board, (1000,1000))
cv2.imwrite("test_marker.jpg", img)

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
