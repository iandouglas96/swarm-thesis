#This code modified from R. Labbe, "Kalman Filters in Python"

from math import tan, sin, cos, sqrt, atan2
from numpy.random import randn, randint
from filterpy.stats import plot_covariance_ellipse
from UKFFilter import UnscentedKalmanFilter as UKF
from filterpy.kalman import unscented_transform, MerweScaledSigmaPoints
import matplotlib.pyplot as plt
import numpy as np

def move(x, u, dt, l):
    #calculate R to ICC
    Vl = u[0];
    Vr = u[1];
    
    R = (l/4)*(Vl+Vr)/(Vr-Vl)
    omega = (Vr-Vl)/l
    
    #calculate ICC position
    ICC = np.array([x[0]-R*np.sin(x[2]), x[1]+R*np.cos(x[2])])

    #calculate the measurement matrix
    rotation = np.array([[np.cos(omega*dt), -np.sin(omega*dt), 0],
                       [np.sin(omega*dt), np.cos(omega*dt), 0],
                       [0, 0, 1]])
    fxu = rotation.dot(np.array([x[0]-ICC[0], x[1]-ICC[1], x[2]]))
    return fxu + np.array([ICC[0], ICC[1], omega*dt])
        
def fx(x, dt, u):
    return move(x, u, dt, wheelbase)

def normalize_angle(x):
    x = x % (2 * np.pi)    # force in range [0, 2 pi)
    if x > np.pi:          # move to [-pi, pi)
        x -= 2 * np.pi
    return x
    
def residual_h(a, b):
    y = a - b
    for i in range(0, len(b), 2):
        if (a[i] == 0 and a[i+1] == 0):
            y[i] = 0
            y[i+1] = 0
    # data in format [dist_1, bearing_1, dist_2, bearing_2,...]
    for i in range(0, len(y), 2):
        y[i + 1] = normalize_angle(y[i + 1])
    return y

def residual_x(a, b):
    y = a - b
    y[2] = normalize_angle(y[2])
    return y
    
def Hx(x, landmarks):
    """ takes a state variable and returns the measurement
    that would correspond to that state. """
    hx = []
    for lmark in landmarks:
        px, py = lmark
        dist = sqrt((px - x[0])**2 + (py - x[1])**2)
        angle = atan2(py - x[1], px - x[0])
        hx.extend([dist, normalize_angle(angle - x[2])])
    return np.array(hx)
    
def state_mean(sigmas, Wm):
    x = np.zeros(3)

    sum_sin = np.sum(np.dot(np.sin(sigmas[:, 2]), Wm))
    sum_cos = np.sum(np.dot(np.cos(sigmas[:, 2]), Wm))
    x[0] = np.sum(np.dot(sigmas[:, 0], Wm))
    x[1] = np.sum(np.dot(sigmas[:, 1], Wm))
    x[2] = atan2(sum_sin, sum_cos)
    return x

def z_mean(sigmas, Wm):
    z_count = sigmas.shape[1]
    x = np.zeros(z_count)

    for z in range(0, z_count, 2):
        sum_sin = np.sum(np.dot(np.sin(sigmas[:, z+1]), Wm))
        sum_cos = np.sum(np.dot(np.cos(sigmas[:, z+1]), Wm))

        x[z] = np.sum(np.dot(sigmas[:,z], Wm))
        x[z+1] = atan2(sum_sin, sum_cos)
    return x

def run_localization(
    cmds, landmarks, sigma_vel, sigma_steer, sigma_range, 
    sigma_bearing, ellipse_step=1, step=10):

    plt.figure()
    points = MerweScaledSigmaPoints(n=3, alpha=.00001, beta=2, kappa=0, 
                                    subtract=residual_x)
    ukf = UKF(dim_x=3, fx=fx, hx=Hx,
              dt=dt, points=points, x_mean_fn=state_mean, 
              z_mean_fn=z_mean, residual_x=residual_x, 
              residual_z=residual_h)

    ukf.x = np.array([0, 0, 0])
    ukf.P = np.diag([.1, .1, .05])
    ukf.R = np.array([sigma_range**2, 
                     sigma_bearing**2])
    ukf.Q = np.eye(3)*0.0001
    
    sim_pos = np.array([0, 0, 0.5])
    
    # plot landmarks
    if len(landmarks) > 0:
        plt.scatter(landmarks[:, 0], landmarks[:, 1], 
                    marker='s', s=60)
    
    track = []
    for i, u in enumerate(cmds):     
        sim_pos = move(sim_pos, u, dt/step, wheelbase) 
        track.append(sim_pos)

        if i % step == 0:
            ukf.predict(fx_args=u)

            if i % ellipse_step == 0:
                plot_covariance_ellipse(
                    (ukf.x[0], ukf.x[1]), ukf.P[0:2, 0:2], std=6,
                     facecolor='k', alpha=0.3)

            x, y = sim_pos[0], sim_pos[1]
            z = []
            n = randint(4)
            for lmark in landmarks[0:n+1]:
                dx, dy = lmark[0] - x, lmark[1] - y
                d = sqrt(dx**2 + dy**2) + randn()*sigma_range
                bearing = atan2(lmark[1] - y, lmark[0] - x)
                a = (normalize_angle(bearing - sim_pos[2] + 
                     randn()*sigma_bearing))
                z.extend([d, a])
            
            print z
            ukf.update(z, hx_args=landmarks[0:n+1],)

            if i % ellipse_step == 0:
                plot_covariance_ellipse(
                    (ukf.x[0], ukf.x[1]), ukf.P[0:2, 0:2], std=6,
                     facecolor='g', alpha=0.8)
    track = np.array(track)
    plt.plot(track[:, 0], track[:,1], color='k', lw=2)
    plt.axis('equal')
    plt.title("UKF Robot localization")
    plt.show()
    return ukf

dt = 1.0
wheelbase = 0.5    
landmarks = np.array([[5,5], [5,0], [10, 5]])
cmds = [np.array([-1, -0.7])] * 200
ukf = run_localization(
    cmds, landmarks, sigma_vel=0.1, sigma_steer=np.radians(1),
    sigma_range=1, sigma_bearing=0.1)
print('Final P:', ukf.P.diagonal())
