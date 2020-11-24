import numpy as np
import math
from pyquaternion import Quaternion



def R2ypr(R):
    n = R[:,0]
    o = R[:,1]
    a = R[:,2]
    
    ypr = np.zeros(3)
    y = math.atan2(n[1], n[0])
    p = math.atan2(-n[2], n[0] * math.cos(y) + n[1] * math.sin(y))
    r = math.atan2(a[0] * math.sin(y) - a[1] * math.cos(y), -o[0] * math.sin(y) + o[1] * math.cos(y))
    ypr[0] = y
    ypr[1] = p
    ypr[2] = r

    return ypr

def ypr2R(ypr, use_angle = True):
    y, p, r = ypr
    from math import cos
    from math import sin
    if(use_angle):
        y = ypr[0] / 180.0 * math.pi;
        p = ypr[1] / 180.0 * math.pi;
        r = ypr[2] / 180.0 * math.pi;

    Rz = np.array([cos(y), -sin(y), 0,
        sin(y), cos(y), 0,
        0, 0, 1]).reshape(3,3)

    Ry = np.array([cos(p), 0., sin(p),
        0., 1., 0.,
        -sin(p), 0., cos(p)]).reshape(3,3)
 
    Rx = np.array([ 1., 0., 0.,
        0., cos(r), -sin(r),
        0., sin(r), cos(r)]).reshape(3,3)
 
    return (Rz.dot(Ry)).dot(Rx)

def quaternion_from_matrix(R):
    q =  Quaternion(matrix=R)
    return np.array([q.x, q.y, q.z, q.w])

def quaternion_matrix(q):
    x, y, z, w = q
    q = Quaternion(w, x, y, z)
    return q.rotation_matrix
        
class PoseInfo(object):
    def __init__(self, name="pose"):
        self.name = name
              
        return
    def construct_fromT(self,  _T):
        self.T = _T.copy()
        self.R = (self.T[:3,:3]).copy()
        self.t = self.T[:3, 3].copy()
        
        self.ypr = np.array(R2ypr(self.R))
        self.q = quaternion_from_matrix(self.R)
        return self
    def construct_fromRt(self,  R = np.identity(3), t= np.zeros(3)):
        self.R = R.copy();
        self.t = t.copy()
        
        self.T = np.identity(4)
        self.T[:3,:3]= self.R.copy();
        self.T[:3,3] = self.t.copy()
        
        self.ypr = np.array(R2ypr(self.R));
        self.q = quaternion_from_matrix(self.R)
        return self

    
    def construct_fromyprt(self,  ypr = np.zeros(3), t= np.zeros(3), use_angle = True):
        R = ypr2R(ypr, use_angle = use_angle)
        t = np.array(t)
        return self.construct_fromRt(R, t)
    @property
    def I(self):
        temppose = PoseInfo("temp")
        temppose_T = (np.matrix(self.T).I).getA()
        temppose.construct_fromT(temppose_T)
        return temppose
    def get_simple_gap(self, pose2):
        res = "t={}, ypr={}".format(pose2.t - self.t, (pose2.ypr - self.ypr)* 180/math.pi)
        return res
    def get_simple_yaw_gap(self, pose2):
        np.set_printoptions(precision=8, suppress=True)
        res = "ypr={}".format((pose2.ypr - self.ypr)* 180/math.pi)
        return res
        
    def __mul__(self, other):
        
        temppose = PoseInfo("pose")
        temppose_T = (np.matrix(self.T) * np.matrix(other.T)).getA()
        temppose.construct_fromT(temppose_T)
        return temppose
    def project_point(self, pnt):
        pnt = np.array([pnt[0], pnt[1],pnt[2],  1])
        p = self.T.dot(pnt)
        p = p/p[-1]
        return p[:3]
    def set_name(self, _name):
        self.name = _name;
        return self
       

    def __repr__(self):
        np.set_printoptions(precision=6, suppress=True)
        res = "{}: t={},ypr={}\nT={}\nR={}".format(self.name, self.t, self.ypr * 180/math.pi , self.T, self.R)
        np.set_printoptions(suppress=True)
        return res
     
   
    def run(self):   
        pose = self.construct_fromqt(331383.430427,  3470499.08365, 14.7564034945,-0.00144698227995, -0.0117098317469,    0.221215935085,    0.975153473125)
        print(pose)
        return



if __name__ == "__main__":   
    obj= PoseInfo("test")
    obj.run()