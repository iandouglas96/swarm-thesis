import sympy
from sympy import symbols, Matrix
import numpy as np
from filterpy.stats import plot_covariance_ellipse
import matplotlib.pyplot as plt

class Robot():
    def __init__(self, robot_width, dt):
        #define our variables
        self.dt = dt
        self.time = symbols('t')
        self.Vl, self.Vr = symbols('V_l, V_r')
        self.px, self.py = symbols('px, py')
        self.x_x, self.x_y, self.l, self.theta = symbols('x_x, x_y, l, theta')
        
        #get the various matrices
        self.fxu, self.F, self.V = self.calc_system_mat()
        self.z, self.H, self.H_p = self.calc_measurement_mat()

        #lambdify our matrices for numerical evaluation
        self.f_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.l, self.Vl, self.Vr, self.time),
                           self.fxu, modules='numpy')
        self.F_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.l, self.Vl, self.Vr, self.time),
                           self.F, modules='numpy')
        self.V_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.l, self.Vl, self.Vr, self.time),
                           self.V, modules='numpy')
        self.z_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.px, self.py),
                           self.z, modules='numpy')
        self.H_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.px, self.py),
                           self.H, modules='numpy')
        self.H_p_n = sympy.lambdify((self.x_x, self.x_y, self.theta, self.px, self.py),
                           self.H_p, modules='numpy')
        
        self.P = np.diag([0.02, 0.02, 0.02])
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
        
    def update(self, measurement, landmark_pos):
        #calculate the predicted value
        h = self.z_n(self.x[0][0], self.x[1][0], self.x[2][0], landmark_pos[0], landmark_pos[1])
        
        dist = np.sqrt((landmark_pos[0]-self.x[0][0])**2 + (landmark_pos[1]-self.x[1][0])**2)
        theta = np.arctan2(landmark_pos[1]-self.x[1][0], landmark_pos[0]-self.x[0][0])-self.x[2][0]
        
        #calculate the residual
        y = measurement - h
        
        y[1] = y[1] % (2 * np.pi)    # force in range [0, 2 pi)
        if y[1] > np.pi:             # move to [-pi, pi)
            y[1] -= 2 * np.pi
        
        #generate H and R matrices
        H = self.H_n(self.x[0][0], self.x[1][0], self.x[2][0], landmark_pos[0], landmark_pos[1])
        #R is sensor noise
        R = np.diag([0.1, 0.02])
        
        #calculate kalman gain
        K = (self.P.dot(H.T)).dot(np.linalg.inv((H.dot(self.P)).dot(H.T) + R))
        
        #calculate new prior
        self.x = self.x + K.dot(y)
        
        #new covariance matrix
        self.P = (np.eye(3)-K.dot(H)).dot(self.P)
    
    #Calculate the system propagation matrix
    def calc_system_mat(self):
        #calculate R to ICC
        R = (self.l/4)*(self.Vl+self.Vr)/(self.Vr-self.Vl)
        omega = (self.Vr-self.Vl)/self.l
        
        #calculate ICC position
        ICC = Matrix([[self.x_x-R*sympy.sin(self.theta), self.x_y+R*sympy.cos(self.theta)]])

        #calculate the measurement matrix
        rotation = Matrix([[sympy.cos(omega*self.time), -sympy.sin(omega*self.time), 0],
                           [sympy.sin(omega*self.time), sympy.cos(omega*self.time), 0],
                           [0, 0, 1]])
        fxu = rotation * Matrix([[self.x_x-ICC[0]], [self.x_y-ICC[1]], [self.theta]])
        fxu = fxu + Matrix([ICC[0], ICC[1], omega*self.time])
        
        #The jacobian of the system propagation matrix is F
        F = fxu.jacobian(Matrix([self.x_x, self.x_y, self.theta]))
        #V we can use to convert our noise from control space
        V = fxu.jacobian(Matrix([self.Vl, self.Vr]))
        return fxu, F, V
        
    def calc_measurement_mat(self):
        #measurement matrix
        z = Matrix([[sympy.sqrt(((self.px-self.x_x)**2) + ((self.py-self.x_y)**2))],
                    [sympy.atan2(self.py-self.x_y, self.px-self.x_x) - self.theta]])
                    
        #find H matrix (jacobian of z wrt x,y,theta)
        H = z.jacobian(Matrix([self.x_x, self.x_y, self.theta]))
        #find H_p (jacobian of z wrt px, py)
        H_p = z.jacobian(Matrix([self.px, self.py])) 
        
        return z, H, H_p


def run(r):
    landmarks = np.array([[5,5], [5,0], [10, 5]])
    control_ideal = np.array([1,1.1])
    
    track = []
    for i in range(200):
        print i
        control = control_ideal * [np.random.normal(1, 0.1),np.random.normal(1, 0.1)]
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
                r.update(measurement, l)
            plot_covariance_ellipse(
                    (r.x[0][0], r.x[1][0]), r.P[0:2, 0:2], 
                     std=6, facecolor='g', alpha=0.8)
                     
            #change direction
            control_ideal = np.array([np.random.normal(1, 0.5),np.random.normal(1, 0.5)])
                     
    track = np.array(track)

    plt.scatter(landmarks[:, 0], landmarks[:, 1],
                marker='s', s=60)
    plt.plot(track[:, 0], track[:,1], color='k', lw=2)
    plt.ylim((-10,15))
    plt.show()

print "running"
r = Robot(2, 0.1)
run(r)
