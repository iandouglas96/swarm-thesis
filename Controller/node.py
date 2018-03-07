import sympy
from sympy import symbols, Matrix
import numpy as np

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from constants import *
from serialinterface import SerialInterface
import struct
import pdb

#IMPORTANT: Import AFTER kivy stuff
from UKFFilter import UnscentedKalmanFilter as UKF
from filterpy.kalman import unscented_transform, MerweScaledSigmaPoints

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def move(x, u, dt, l):
    #simulate rounding error created by speed timing algorithm
    if (u[0] != 0):
        Vl = 1024//abs(int(u[0]))*np.sign(u[0])
        Vl = 1024.0/Vl
    else:
        Vl = 0
    if (u[1] != 0):    
        Vr = 1024//abs(int(u[1]))*np.sign(u[1])
        Vr = 1024.0/Vr
    else:
        Vr = 0
        
    #print str(Vl) + "  " + str(Vr)
    
    #scale appropriately to screen
    Vl = 0.2*Vl
    Vr = 0.2*Vr

    #special case for straight motion
    if (Vl == Vr):
        return np.array([x[0]+Vl*dt*np.cos(-x[2]), x[1]+Vl*dt*np.sin(-x[2]), x[2]])
    
    R = (l/4)*(Vl+Vr)/(Vl-Vr)
    omega = (Vl-Vr)/l
    
    #calculate ICC position
    ICC = np.array([x[0]-R*np.sin(-x[2]), x[1]+R*np.cos(-x[2])])

    #calculate the new transformed position
    rotation = np.array([[np.cos(omega*dt), -np.sin(omega*dt), 0],
                       [np.sin(omega*dt), np.cos(omega*dt), 0],
                       [0, 0, 1]])
    fxu = rotation.dot(np.array([x[0]-ICC[0], x[1]-ICC[1], x[2]]))
    return fxu + np.array([ICC[0], ICC[1], omega*dt])
        
def fx(x, dt, u):
    return move(x, u, dt, 55.)

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
        dist = np.sqrt((px - x[0])**2 + (py - x[1])**2)
        angle = np.arctan2(x[1] - py, px - x[0])
        hx.extend([dist, normalize_angle(angle - x[2])])
    return np.array(hx)
    
def state_mean(sigmas, Wm):
    x = np.zeros(3)

    sum_sin = np.sum(np.dot(np.sin(sigmas[:, 2]), Wm))
    sum_cos = np.sum(np.dot(np.cos(sigmas[:, 2]), Wm))
    x[0] = np.sum(np.dot(sigmas[:, 0], Wm))
    x[1] = np.sum(np.dot(sigmas[:, 1], Wm))
    x[2] = np.arctan2(sum_sin, sum_cos)
    return x

def z_mean(sigmas, Wm):
    z_count = sigmas.shape[1]
    x = np.zeros(z_count)

    for z in range(0, z_count, 2):
        sum_sin = np.sum(np.dot(np.sin(sigmas[:, z+1]), Wm))
        sum_cos = np.sum(np.dot(np.cos(sigmas[:, z+1]), Wm))

        x[z] = np.sum(np.dot(sigmas[:,z], Wm))
        x[z+1] = np.arctan2(sum_sin, sum_cos)
    return x

#A Class for keeping track of robot data
class Node(Widget):
    
    #link node_id to the .kv file by making it a kivy property
    node_id = NumericProperty(0)

    def __init__(self, data, ser, **kwargs):
        super(Node, self).__init__(**kwargs)
        #parse data
        self.set_data(data)
        self.current_id = self.node_id
        self.comm = ser
        self.manual = True
        #u, r, d, l
        self.key_matrix = [False, False, False, False]
        self.old_matrix = [False, False, False, False]
        self.target_list = []
        self.control = np.array([0., 0.])

    #Parse data struct
    def set_data(self, data):
        self.node_id = data[DUMP_DATA_NODE_ID]
        self.verbose_flag = data[DUMP_DATA_VERBOSE]
        self.target_separation = data[DUMP_DATA_TARGET_SEPARATION]
        self.attraction_const = data[DUMP_DATA_ATTRACTION_CONST]
        self.repulsion_const = data[DUMP_DATA_REPULSION_CONST]
        self.sensor_calib_1 = data[DUMP_DATA_SENSOR_CALIB_1_CONST]
        self.sensor_calib_2 = data[DUMP_DATA_SENSOR_CALIB_2_CONST]
        self.angular_v_const = data[DUMP_DATA_ANGULAR_VELOCITY_CONST]
        self.linear_v_const = data[DUMP_DATA_LINEAR_VELOCITY_CONST]
        self.freq = data[DUMP_DATA_FREQ]
        self.color = FREQUENCY_BIN_COLORS[FREQUENCIES[self.freq]]

    #Update prefs over communication link
    def send_data(self):
        #pack all the data we want to send
        args = struct.pack(FORMATS[DUMP_COMMAND], self.node_id, self.verbose_flag,
                           self.target_separation, self.attraction_const,
                           self.repulsion_const, self.sensor_calib_1, self.sensor_calib_2,
                           self.angular_v_const, self.linear_v_const, self.freq)

        #send the command
        self.comm.send_command(self.current_id, SET_CONSTS_COMMAND, args)

        #Now the ID has actually changed
        self.current_id = self.node_id

    #turn off or on manual mode
    def set_manual(self, manual):
        self.manual = manual
        if (manual):
            #take over the keyboard
            Window.bind(on_key_down=self.key_down)
            Window.bind(on_key_up=self.key_up)

            #enter manual control mode (and stop)
            args = struct.pack(FORMATS[DRIVE_COMMAND], 0, 0)
            self.comm.send_command(self.current_id, DRIVE_COMMAND, args)
            self.control[0] = 0
            self.control[1] = 0
        else:
            #relinquish the keyboard
            Window.unbind(on_key_down=self.key_down)
            Window.unbind(on_key_up=self.key_up)
            self.key_matrix = [False, False, False, False]

            #return to auto control
            self.comm.send_command(self.current_id, AUTO_COMMAND)

    #called when user changes focus to or away
    def set_active(self, active):
        if (active and self.manual):
            #take over the keyboard
            Window.bind(on_key_down=self.key_down)
            Window.bind(on_key_up=self.key_up)
        elif (not active and self.manual):
            #relinquish the keyboard
            Window.unbind(on_key_down=self.key_down)
            Window.unbind(on_key_up=self.key_up)

    def key_down(self, window, key, *args):
        if (key == 273):
            #up
            self.key_matrix[UP] = True
        elif (key == 275):
            #right
            self.key_matrix[RIGHT] = True
        elif (key == 274):
            #down
            self.key_matrix[DOWN] = True
        elif (key == 276):
            #left
            self.key_matrix[LEFT] = True

        self.command_motion()

    def key_up(self, window, key, *args):
        if (key == 273):
            #up
            self.key_matrix[UP] = False
        elif (key == 275):
            #right
            self.key_matrix[RIGHT] = False
        elif (key == 274):
            #down
            self.key_matrix[DOWN] = False
        elif (key == 276):
            #left
            self.key_matrix[LEFT] = False

        self.command_motion()

    #If motion controls changed, send the appropriate command to the robot
    def command_motion(self):
        #only send command if something changed, so we don't spam the comm system
        if (self.old_matrix != self.key_matrix):
            r_speed = 100*(self.key_matrix[UP]-self.key_matrix[DOWN])+50*(self.key_matrix[LEFT]-self.key_matrix[RIGHT])
            l_speed = 100*(self.key_matrix[UP]-self.key_matrix[DOWN])+50*(self.key_matrix[RIGHT]-self.key_matrix[LEFT])
            
            self.control[0] = r_speed
            self.control[1] = l_speed

            #payload, assemble!
            args = struct.pack(FORMATS[DRIVE_COMMAND], r_speed, l_speed)

            #send the command
            self.comm.send_command(self.current_id, DRIVE_COMMAND, args)

            #slice so we copy values instead of ref
            self.old_matrix = self.key_matrix[:]
            
    #Functions relating to UKF filtering of robot position
    def ukf_init(self):
        print "ukf init"
        points = MerweScaledSigmaPoints(n=3, alpha=.00001, beta=2, kappa=0, 
                                    subtract=residual_x)

        self.ukf = UKF(dim_x=3, fx=fx, hx=Hx,
                  dt=1./30, points=points, x_mean_fn=state_mean, 
                  z_mean_fn=z_mean, residual_x=residual_x, 
                  residual_z=residual_h)
        
        #covariance and state matrices
        self.ukf.x = np.array([self.pos[0],self.pos[1],np.radians(self.angle)])
        self.ukf.P = np.diag([5, 5, 0.1])
        #sensor noise
        self.ukf.R = np.array([10**2, 
                         0.1**2])
        #process noise                 
        self.ukf.Q = np.diag([0.01, 0.01, 0.01])
        
        #Run predict step to initialize.  Otherwise if we got a measurement before predict, we would crash
        self.ukf_predict(0.0001)
        
    def ukf_predict(self, dt):
        #try:
        #    self.state = fx(self.state, dt, self.control)
        #except AttributeError:
        #    self.state = [self.pos[0], self.pos[1], np.radians(self.angle)]
            
        #self.pos[0] = int(self.state[0])
        #self.pos[1] = int(self.state[1])
        #self.angle = int(np.degrees(self.state[2]))
        
        self.ukf.predict(fx_args=self.control, dt=dt)
        
        self.pos[0] = int(self.ukf.x[0])
        self.pos[1] = int(self.ukf.x[1])
        self.angle = int(np.degrees(self.ukf.x[2]))
        
    def ukf_update(self, z, l_pos):
        self.ukf.update(z, hx_args=l_pos,)
        #print self.ukf.P

    def process_targets(self):
        #figure out force vector
        force_fwd = 0.0
        force_side = 0.0

        #print "proc"
        for n in self.target_list:
            dist =(n['magnitude'])
            #print dist
            if (dist < self.target_separation*1.5):
                force_mag = 0.
                if (dist > self.target_separation):
                    force_mag = (dist-self.target_separation)*self.attraction_const
                elif (dist < self.target_separation):
                    force_mag = (dist-self.target_separation)*self.repulsion_const

                force_fwd += force_mag*np.cos(np.radians(n['direction']))
                force_side += force_mag*np.sin(np.radians(n['direction']))
        
        angular_v, linear_v = self.calc_movement(force_fwd, force_side)
        self.control[0] = float(linear_v + angular_v)
        self.control[1] = float(linear_v - angular_v)

    def calc_movement(self, force_fwd, force_side):
        #convert force vector to motion settings
        if (force_fwd != 0 or force_side != 0):
            #Go back to circular coordinates
            force_angle = np.pi/2-np.arctan2(force_fwd, force_side);
            force_mag = np.sqrt(force_fwd*force_fwd + force_side*force_side);

            #put angle in the +-90 degree range
            while (force_angle > np.pi/2):
                force_angle -= np.pi;
                force_mag *= -1;
            while (force_angle < -np.pi/2):
                force_angle += np.pi;
                force_mag *= -1;

            angular_v = int(-(self.angular_v_const * force_angle));
            linear_v = int(self.linear_v_const * force_mag * np.cos(force_angle));
            
            linear_v = np.clip(linear_v, -400, 400)
            angular_v = np.clip(angular_v, -300, 300)
            return angular_v, linear_v
        else:
            return 0, 0
    
    #generate landmark information     
    def proc_sen_data(self, node_list):
        measurements = []
        landmark_pos = np.empty((0,2), float)
        for target in self.target_list:
            dist = 5.*target['magnitude']
            relevant_node = filter(lambda node: FREQUENCIES[node['data'].freq] == target['bin'], node_list)
            if (len(relevant_node) > 0):
                measurements.extend([dist, -np.radians(target['direction'])])
                landmark_pos = np.vstack([landmark_pos, relevant_node[0]['data'].ukf.x[0:2]])
         
        if (len(measurements) > 0):     
            self.ukf_update(measurements, landmark_pos)

    def update(self, update_type, data, node_list):
        if (update_type == TARGET_LIST_UPDATE):
            #clear out list before we load in new values
            self.target_list = []
            for b in range(0, TARGET_LIST_NUM_TARGETS):
                #verify that the magnitude is nonzero to see if it is a target
                if (data[b*3+TARGET_LIST_UPDATE_MAGNITUDE] != 0):
                    target = {'magnitude':data[b*3+TARGET_LIST_UPDATE_MAGNITUDE],
                              'direction':data[b*3+TARGET_LIST_UPDATE_DIRECTION],
                              'bin':data[b*3+TARGET_LIST_UPDATE_BIN]}
                    self.target_list.append(target)
            print self.target_list
            
            #If we are off of manual, motion is determined by neighbors
            if (not self.manual):
                self.process_targets()
              
            #if the ukf is initialized, go for it
            if (hasattr(self, 'ukf')):
                self.proc_sen_data(node_list)
