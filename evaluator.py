#This is the class that evaluates and illustrates the results. Students should have something similar to 
#evaluate their predictions and visualize their results.
import os
import tensorflow.compat.v1 as tf
import math
import numpy as np
import itertools
import matplotlib.image as mpimg
from utility.poseinfo import PoseInfo
from utility.csvdumpload import CSVDumpLoad
from Dataloader import DataReader
import matplotlib.pyplot as plt
from predictor import Predictor
import matplotlib.patches as patches

class Evaluator():
    def __init__(self):
        #load dataset, mainly ground truth info
        self.gt_df =  DataReader().load()
        self.selected_objids = [0, 8, 5, 15, 20, 13]
        self.selected_objids = [0, 20, 13]
#         self.selected_objids = [15]
        
        return
          
    def evaluate(self):
        #TODO: Write a function that compares the results of prediction with ground-truth and calculates the MSE
        
        return
    def get_image(self):
        fname = self.gt_df.img_path[0]
        img = mpimg.imread(fname)
        return img
    def get_gttrj(self):
        frame_id = self.gt_df.frame_id[0]
        frame_df = self.gt_df[self.gt_df["frame_id"] == frame_id]
        
        visible_flag = ~(frame_df.u.isnull().values)
        
        visible_objectids = frame_df[visible_flag].bd_id
        
        res = {}
        
        for objectid in visible_objectids:
            objectid_df = self.gt_df[self.gt_df["bd_id"] == objectid]
            res[objectid] = objectid_df[["center_x","center_y","center_z", "speed_x", "speed_y", "bd_type", "frame_id", "dim_x", "dim_y",'u', 'v']]
        
        filtered_res = {}
        for ind, (objid, xyzvels) in enumerate(res.items()):
            if ind in self.selected_objids:
                filtered_res[objid] = xyzvels
                continue
        return filtered_res
#     def annotate_img(self, img, dim_x, dim_y,u,v ):
#         mpimg.
#         return img
        

    def visualizer(self):
        #TODO: Write a function that Visualizes the frames side by side the prediction results 
        img = self.get_image()
        obj_xyzs = self.obj_xyzs
        obj_xys_pred = self.obj_xys_pred
        
        
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Image and trajectory predciton')
        ax1.imshow(img)  
        for ind, (objid, xyzvels) in enumerate(obj_xyzs.items()):

            dim_x, dim_y,u,v = xyzvels.iloc[-1][['dim_x', 'dim_y', 'u', 'v']]
            rect = patches.Rectangle((u-dim_x/2.0,v-dim_y/2.0),dim_x,dim_y,linewidth=1,edgecolor='r',facecolor='none')
            ax1.add_patch(rect)
            print("u={}, v= {}, dim_x={}, dim_y = {}".format(u, v, dim_x, dim_y))

#             img = self.annotate_img(img, dim_x, dim_y, u, v)
            
            c = np.random.rand(3,)
            ax2.plot(xyzvels.center_x, xyzvels.center_y, label='{}'.format(ind), color = c)
            ax2.annotate('{}'.format(ind), xy=xyzvels.iloc[-1][['center_x', 'center_y']], color = c)
            
            ax2.plot(obj_xys_pred[objid][:, 0],obj_xys_pred[objid][:, 1], label='{}_pred'.format(ind), color = c)
            ax2.annotate('{}_pred'.format(ind), xy=obj_xys_pred[objid][-1][:2], color = c)
            
          
#             break
        plt.legend()
#         plt.xlabel('X')
#         plt.ylabel('Y')
        
        return
    def calc_rmse(self, objid):
        xyzvels = self.obj_xyzs[objid]
        xys_pred = self.obj_xys_pred[objid]
        
        start_time = xyzvels.iloc[0]['frame_id']
        res = []
        for ind, row in xyzvels.iterrows():
            x, y, t = row['center_x'], row['center_y'], row['frame_id']
            matched_flag = np.abs(xys_pred[:,-1] -t ) < 1e4
            if matched_flag.sum() == 1:
                pred_x, pred_y = xys_pred[matched_flag][0][:2]
                rmse = (x - pred_x) ** 2 + (y - pred_y) ** 2
                rmse = math.sqrt(rmse)
                timestamp = (t - start_time) * 1e-6
                res.append([timestamp, rmse])
            elif matched_flag.sum() > 1:
                raise "we dont' expect to find more than one math"
            else:
                print("{} has no match at time {}".format(objid, t))
        
        return np.array(res)

    def plot_RSME(self):
        #TODO: Write a function that plots the MSE over time
        obj_xyzs = self.obj_xyzs
        obj_xys_pred = self.obj_xys_pred
        fig, axs = plt.subplots(len(self.selected_objids))
        for ind, (objid, xyzvels) in enumerate(obj_xyzs.items()):
            res = self.calc_rmse(objid)
            if len(self.selected_objids) == 1:
                ax = axs
            else:
                ax = axs[ind]
            ax.plot(res[:, 0], res[:, 1])
            ax.set_xlabel("time")
            ax.set_ylabel("rmse error")
            
        
        
        return
    def run(self):
        self.obj_xyzs = self.get_gttrj()
        pred = Predictor()
        self.obj_xys_pred = pred.predict(self.obj_xyzs)
        
        self.visualizer()
#         self.plot_RSME()
        
        plt.show()
        return


if __name__ == "__main__":
    obj = Evaluator()
    obj.run()
    
    
