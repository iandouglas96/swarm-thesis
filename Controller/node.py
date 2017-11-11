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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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

#A Class for keeping track of robot data
class Node(Widget):
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
        self.angular_v_const = data[DUMP_DATA_ANGULAR_VELOCITY_CONST]
        self.linear_v_const = data[DUMP_DATA_LINEAR_VELOCITY_CONST]
        self.freq = data[DUMP_DATA_FREQ]
        self.color = FREQUENCY_BIN_COLORS[FREQUENCIES[self.freq]]

    #Update prefs over communication link
    def send_data(self):
        #pack all the data we want to send
        args = struct.pack(FORMATS[DUMP_COMMAND], self.node_id, self.verbose_flag,
                            self.target_separation, self.attraction_const,
                            self.repulsion_const, self.angular_v_const, self.linear_v_const,
                            self.freq)

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
            r_speed = 100*(self.key_matrix[UP]-self.key_matrix[DOWN])-50*(self.key_matrix[LEFT]-self.key_matrix[RIGHT])
            l_speed = 100*(self.key_matrix[UP]-self.key_matrix[DOWN])-50*(self.key_matrix[RIGHT]-self.key_matrix[LEFT])
            
            self.control[0] = r_speed
            self.control[1] = l_speed

            #payload, assemble!
            args = struct.pack(FORMATS[DRIVE_COMMAND], r_speed, l_speed)

            #send the command
            self.comm.send_command(self.current_id, DRIVE_COMMAND, args)

            #slice so we copy values instead of ref
            self.old_matrix = self.key_matrix[:]
            
    #Functions relating to EKF filtering of robot position
    def ekf_init(self):
        print "ekf init"
        #covariance and state matrices
        self.cov = np.diag([10, 10, 0.2])
        self.state = np.array([[self.pos[0]],[self.pos[1]],[np.radians(self.angle)]])
        
        #covariance models
        self.std_v = 5
    
    def ekf_predict(self, dt=1):
        #control[0]-control[1] is in the denom of matrices.  If equal, get undefined behavior
        if (np.abs(self.control[0] - self.control[1]) < 0.001):
            self.control[0] += 0.001
        
        #calculate V and V
        F = self.F_n(self.state[0][0], self.state[1][0], self.state[2][0], 50, self.control[0], self.control[1], dt)
        V = self.V_n(self.state[0][0], self.state[1][0], self.state[2][0], 50, self.control[0], self.control[1], dt)
        
        #use f(x,u) to compute posterior
        self.state = self.f_n(self.state[0][0], self.state[1][0], self.state[2][0], 50, self.control[0], self.control[1], dt)
        
#         print F
#         print V
#         print self.state
        
        #covariance matrix of error of control inputs
        M = np.array([[self.std_v*self.control[0], 0],
                      [0, self.std_v*self.control[1]]])
        
        #update covariance
        self.cov = (F.dot(self.cov)).dot(F.T) + (V.dot(M)).dot(V.T)
        
        #update graphical location
        self.pos[0] = int(self.state[0][0])
        self.pos[1] = int(self.state[1][0])
        self.angle = int(np.degrees(self.state[2][0]))
        
    def ekf_update(self, measurement, landmark_pos, landmark_cov):
        #IEKF iteration
        state_int = np.copy(self.state)
        print "update"
        for i in range(0,1):
            #calculate the predicted value
            h = self.z_n(state_int[0][0], state_int[1][0], state_int[2][0], landmark_pos[0], landmark_pos[1])
            
            #calculate the residual
            y = measurement - h
            
            y[1] = y[1] % (2 * np.pi)    # force in range [0, 2 pi)
            if y[1] > np.pi:             # move to [-pi, pi)
                y[1] -= 2 * np.pi
                
            print y
            
            #generate H and R matrices
            H = self.H_n(state_int[0][0], state_int[1][0], state_int[2][0], landmark_pos[0], landmark_pos[1])
            H_p = self.H_p_n(state_int[0][0], state_int[1][0], state_int[2][0], landmark_pos[0], landmark_pos[1])
            #R is sensor noise
            R = np.diag([5, 5])

            #calculate kalman gain
            K = (self.cov.dot(H.T)).dot(np.linalg.inv((H.dot(self.cov)).dot(H.T) + (H_p.dot(landmark_cov)).dot(H_p.T) + R))
            
            #calculate new prior
            last_state = np.copy(state_int)
            state_int = self.state + K.dot(y-H.dot(self.state-state_int))
        
        #new covariance matrix
        last_state = np.copy(self.state)
        self.state = np.copy(state_int)
        print self.state-last_state
        self.cov = (np.eye(3)-K.dot(H)).dot(self.cov)
        print self.cov

    def process_targets(self):
        #figure out force vector
        force_fwd = 0
        force_side = 0

        print "proc"
        for n in self.target_list:
            dist = ((n['magnitude']/5428.)**-(1/2.191))
            print dist
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

            angular_v = (self.angular_v_const * force_angle);
            linear_v = (self.linear_v_const * force_mag * np.cos(force_angle));
            return angular_v, linear_v
        else:
            return 0, 0
    
    #generate landmark information     
    def proc_sen_data(self, node_list):
        for target in self.target_list:
            dist = 5.*((target['magnitude']/5428.)**-(1/2.191))
            measurement = np.array([[dist], [-np.radians(target['direction'])]])
            relevant_node = filter(lambda node: FREQUENCIES[node['data'].freq] == target['bin'], node_list)
            if (len(relevant_node) > 0):
                landmark_pos = relevant_node[0]['data'].state[0:2, 0]
                landmark_cov = relevant_node[0]['data'].cov[0:2, 0:2]
            
                self.ekf_update(measurement, landmark_pos, landmark_cov)

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
            #print self.target_list
            
            #If we are off of manual, motion is determined by neighbors
            if (not self.manual):
                self.process_targets()
              
            #if the ekf is initialized, go for it
            if (hasattr(self, 'cov')):
                self.proc_sen_data(node_list)
