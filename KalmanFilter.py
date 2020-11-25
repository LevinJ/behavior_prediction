import numpy as np

#If students already developed Kalman filter they can utilize it in this project. 
class KalmanFilter(object):
    def __init__(self):
        #TODO: Write a function that does the initialization
        # Here we have 4 system states, [x, ]
        self.STATE_SIZE = 4
        self.X = np.zeros(self.STATE_SIZE)
        self.P = np.identity(self.STATE_SIZE)
        
        return
    def F(self, dt):
        # Here we are using an constaant velocity motion model
        F = [1,0,dt,0,
             0, 1, 0, dt,
             0, 0, 1, 0,
             0, 0, 0, 1]
        return np.array(F).reshape(4, 4)

        
    def motion_model(self, cur_pos, cur_vel, pred_duration, pred_time):
        #TODO: Write a function for capturing the motion model (optional) with constant velocity
        self.X = np.array([cur_pos[0], cur_pos[1], cur_vel[0], cur_vel[1]])
        self.P = np.identity(self.STATE_SIZE)
        xys = []
        xys.append([self.X[0], self.X[1],pred_time])
        
        
        dt = 0.1
        elapsed_time = 0
        while  elapsed_time <= pred_duration:
            elapsed_time += dt
            self.predict(dt)
            pred_time += dt* 1e6
            xys.append([self.X[0], self.X[1],pred_time])
        
        return np.array(xys)
        
    def predict(self, dt):
        #TODO: Write a function for the prediction state of KF
        F = self.F(dt)
        self.X = F.dot(self.X)
        F_transpose = np.transpose(F)
        self.P = (F.dot(self.P)).dot(F_transpose)
        return
            
    def update(self, R,H,z_pred, z):
        #TODO: Write a function for the update state of KF
        y = z - z_pred
        I = np.identity(self.STATE_SIZE)
        
        pht = self.P * (H.T)
        S = H * pht + R 
        K = pht * S.I
       
        self.X = self.X + (K * y)
        
        #we can use subset K to speed up computation
        gainResidual = I
        gainResidual -= K * H;
        self.P = gainResidual * self.P * gainResidual.T;
        self.P += K * R * K.T;
        return