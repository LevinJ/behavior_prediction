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

class Evaluator():
    def __init__(self):
        #load dataset, mainly ground truth info
        self.gt_df =  DataReader().load()
        self.selected_objids = [0, 8, 5, 15, 20, 13]
        
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
            res[objectid] = objectid_df[["center_x","center_y","center_z"]]
        
        
        return res
        

    def visualizer(self):
        #TODO: Write a function that Visualizes the frames side by side the prediction results 
        img = self.get_image()
        obj_xyzs = self.get_gttrj()
        
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Image and trajectory predciton')
        ax1.imshow(img)
        for ind, (_objid, xyzs) in enumerate(obj_xyzs.items()):
#             if ind <=10:
#                 continue
            if not ind in self.selected_objids:
                continue
            ax2.plot(xyzs.center_x, xyzs.center_y, label='{}'.format(ind))
            
#             break
        plt.legend()
#         plt.xlabel('X')
#         plt.ylabel('Y')
        plt.show()
        return

    def plot_RSME(self):
        #TODO: Write a function that plots the MSE over time
        
        return
    def run(self):
        self.visualizer()
        return


if __name__ == "__main__":
    obj = Evaluator()
    obj.run()
    
    
