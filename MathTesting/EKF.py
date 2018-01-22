import sympy
from sympy import symbols, Matrix
import numpy as np
from filterpy.stats import plot_covariance_ellipse
import matplotlib.pyplot as plt

#Calculate the system propagation matrix
def calc_system_mat(x_x, x_y, theta, l, Vl, Vr, time):
    #calculate R to ICC
    R = (l/4)*(Vl+Vr)/(Vr-Vl)
    omega = (Vr-Vl)/l
    
    #calculate ICC position
    ICC = Matrix([[x_x-R*sympy.sin(theta), x_y+R*sympy.cos(theta)]])

    #calculate the measurement matrix
    rotation = Matrix([[sympy.cos(omega*time), -sympy.sin(omega*time), 0],
                       [sympy.sin(omega*time), sympy.cos(omega*time), 0],
                       [0, 0, 1]])
    fxu = rotation * Matrix([[x_x-ICC[0]], [x_y-ICC[1]], [theta]])
    fxu = fxu + Matrix([ICC[0], ICC[1], omega*time])
    
    #The jacobian of the system propagation matrix is F
    F = fxu.jacobian(Matrix([x_x, x_y, theta]))
    #V we can use to convert our noise from control space
    V = fxu.jacobian(Matrix([Vl, Vr]))
    return fxu, F, V
    
def calc_measurement_mat(x_x, x_y, theta, px, py):
    #measurement matrix
    z = Matrix([[sympy.sqrt(((px-x_x)**2) + ((py-x_y)**2))],
                [sympy.atan2(py-x_y, px-x_x) - theta]])
                
    #find H matrix (jacobian of z wrt x,y,theta)
    H = z.jacobian(Matrix([x_x, x_y, theta]))
    #find H_p (jacobian of z wrt px, py)
    H_p = z.jacobian(Matrix([px, py])) 
    
    return z, H, H_p

class Robot():
    #define our variables
    time = symbols('t')
    Vl, Vr = symbols('V_l, V_r')
    px, py = symbols('px, py')
    x_x, x_y, l, theta = symbols('x_x, x_y, l, theta')
    
    #get the various matrices
    fxu, F, V = calc_system_mat(x_x, x_y, theta, l, Vl, Vr, time)
    z, H, H_p = calc_measurement_mat(x_x, x_y, theta, px, py)

    #lambdify our matrices for numerical evaluation
    f_n = staticmethod(sympy.lambdify((x_x, x_y, theta, l, Vl, Vr, time),
                       fxu, modules='numpy'))
    F_n = staticmethod(sympy.lambdify((x_x, x_y, theta, l, Vl, Vr, time),
                       F, modules='numpy'))
    V_n = staticmethod(sympy.lambdify((x_x, x_y, theta, l, Vl, Vr, time),
                       V, modules='numpy'))
    z_n = staticmethod(sympy.lambdify((x_x, x_y, theta, px, py),
                       z, modules='numpy'))
    H_n = staticmethod(sympy.lambdify((x_x, x_y, theta, px, py),
                       H, modules='numpy'))
    H_p_n = staticmethod(sympy.lambdify((x_x, x_y, theta, px, py),
                       H_p, modules='numpy'))
    
    def __init__(self, robot_width, dt):
        self.dt = dt
        
        self.P = np.diag([0.1, 0.1, 0])
        self.x = np.array([[0],[0],[0]])
        self.x_act = np.array([[0],[0],[0]])
        
        #covariance models
        self.std_v = 0.1
        
    def predict(self, control=0, control_ideal=0):
        #calculate V and V
        F = self.F_n(self.x[0][0], self.x[1][0], self.x[2][0], 2, control[0], control[1], self.dt)
        V = self.V_n(self.x[0][0], self.x[1][0], self.x[2][0], 2, control[0], control[1], self.dt)
        
        #use f(x,u) to compute posterior
        self.x = self.f_n(self.x[0][0], self.x[1][0], self.x[2][0], 2, control_ideal[0], control_ideal[1], self.dt)
        
        self.x_act = self.f_n(self.x_act[0][0], self.x_act[1][0], self.x_act[2][0], 2, control[0], control[1], self.dt)
        
#         print F
#         print V
#         print self.x
        
        #covariance matrix of error of control inputs
        M = np.array([[self.std_v*control[0], 0],
                      [0, self.std_v*control[1]]])
        
        #update covariance
        self.P = (F.dot(self.P)).dot(F.T) + (V.dot(M)).dot(V.T)
        
    def update(self, measurement, landmark_pos, landmark_cov):
        #calculate the predicted value
        h = self.z_n(self.x[0][0], self.x[1][0], self.x[2][0], landmark_pos[0], landmark_pos[1])
        
        #calculate the residual
        y = measurement - h
        
        y[1] = y[1] % (2 * np.pi)    # force in range [0, 2 pi)
        if y[1] > np.pi:             # move to [-pi, pi)
            y[1] -= 2 * np.pi
        
        #generate H and R matrices
        H = self.H_n(self.x[0][0], self.x[1][0], self.x[2][0], landmark_pos[0], landmark_pos[1])
        H_p = self.H_p_n(self.x[0][0], self.x[1][0], self.x[2][0], landmark_pos[0], landmark_pos[1])
        #R is sensor noise
        R = np.diag([0.1, 0.02])
        
        #calculate kalman gain
        K = (self.P.dot(H.T)).dot(np.linalg.inv((H.dot(self.P)).dot(H.T) + (H_p.dot(landmark_cov)).dot(H_p.T) + R))
        
        #calculate new prior
        self.x = self.x + K.dot(y)
        
        #new covariance matrix
        self.P = (np.eye(3)-K.dot(H)).dot(self.P)


def run(r):
    landmarks = np.array([[5,5], [5,0], [10, 5]])
    landmark_cov = np.diag([0.1, 0.1])
    control_ideal = np.array([1,1.1])
    
    #plot landmark covariances
    for l in landmarks:
        plot_covariance_ellipse(
                    (l[0], l[1]), landmark_cov, 
                     std=6, facecolor='k', alpha=0.3)
    
    track = []
    for i in range(200):
        print i
        control = control_ideal# * [np.random.normal(1, 0.1),np.random.normal(1, 0.1)]
        r.predict(control, control_ideal)
#         print "yo"
#         print track
        track.append(r.x_act[:,0])

        if (i%10 == 0):
            plot_covariance_ellipse(
                    (r.x[0,0], r.x[1,0]), r.P[0:2, 0:2], 
                     std=6, facecolor='k', alpha=0.3)
            for l in landmarks:
                dist = np.sqrt((l[0]-r.x_act[0][0])**2 + (l[1]-r.x_act[1][0])**2) + np.random.normal(0, 0.1)
                theta = np.arctan2(l[1]-r.x_act[1][0], l[0]-r.x_act[0][0])-r.x_act[2][0] + np.random.normal(0, 0.02)
                measurement = np.array([[dist], [theta]])
                r.update(measurement, l, landmark_cov)
            plot_covariance_ellipse(
                    (r.x[0][0], r.x[1][0]), r.P[0:2, 0:2], 
                     std=6, facecolor='g', alpha=0.8)
                     
            #change direction
            #control_ideal = np.array([np.random.normal(1, 0.5),np.random.normal(1, 0.5)])
                     
    #output the final covariance              
    print r.P              
    
    track = np.array(track)

    plt.scatter(landmarks[:, 0], landmarks[:, 1],
                marker='s', s=60)
    plt.plot(track[:, 0], track[:,1], color='k', lw=2)
    plt.ylim((-10,15))
    plt.show()

print "running"
r = Robot(2, 0.1)
run(r)
