#TODO: Import libraries and packages
# from evaluator import Evaluator
from KalmanFilter import KalmanFilter
# from utility.csvdumpload import CSVDumpLoad
import os
import numpy as np

class Predictor():
    def __init__(self):
        #TODO: Write a function that does initialization
#         self.tf_record_file = "./test/data/training_segment-10226164909075980558_180_000_200_000_with_camera_labels.tfrecord"
#         
#         
#         datafolder = os.path.abspath(os.path.join(os.path.dirname(__file__), './data/temp/{}'.format(os.path.basename(self.tf_record_file).split(".")[0])))
#         cols = ["frame_id","bd_id", "bd_type","center_x","center_y"]
#         CSVDumpLoad.__init__(self, "trj_prediction", datafolder, cols)
#         np.set_printoptions(suppress=True)
        return
        
    def predict(self, obj_xyzvels):
        #TODO: Write a function that given the data, predits the position of an object at given time period. 
        res = {}
        for bd_id, xyzvel in obj_xyzvels.items():
            cur_pos = xyzvel[['center_x', 'center_y']].iloc[0].values
            cur_vel = xyzvel[['speed_x', 'speed_y']].iloc[0].values
            cur_time = xyzvel[['frame_id']].iloc[0].values[0]
            pred_duration = 5
            kf = KalmanFilter()
            pred_xys = kf.motion_model(cur_pos, cur_vel, pred_duration, cur_time)
            res[bd_id] = pred_xys
        return res
    
#     def get_obj_list(self):
#         evl = Evaluator()
#         obj_xyzvels = evl.get_gttrj()
#         return obj_xyzvels
    
    def run(self):
        obj_xyzvels = self.get_obj_list()
        for bd_id, xyzvel in obj_xyzvels.items():
            cur_pos = xyzvel[['center_x', 'center_y']].iloc[0].values
            cur_vel = xyzvel[['speed_x', 'speed_y']].iloc[0].values
            pred_duration = 5
            kf = KalmanFilter()
            kf.motion_model(cur_pos, cur_vel, pred_duration)
        return
    

if __name__ == "__main__":
    obj = Predictor()
    obj.run()
        

