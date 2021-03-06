#This class is designed to read the output of tracking data 
import os
import tensorflow.compat.v1 as tf
import math
import numpy as np
import itertools
import matplotlib.image as mpimg

tf.enable_eager_execution()

from waymo_open_dataset.utils import range_image_utils
from waymo_open_dataset.utils import transform_utils
from waymo_open_dataset.utils import  frame_utils
from waymo_open_dataset import dataset_pb2 as open_dataset
from utility.poseinfo import PoseInfo
from utility.csvdumpload import CSVDumpLoad

class DataReader(CSVDumpLoad):
    def __init__(self):
        #TODO: Write a function that initializes the class
        self.tf_record_file = "./test/data/training_segment-10226164909075980558_180_000_200_000_with_camera_labels.tfrecord"
        
        
        datafolder = os.path.abspath(os.path.join(os.path.dirname(__file__), './data/temp/{}'.format(os.path.basename(self.tf_record_file).split(".")[0])))
        cols = ["frame_id","bd_id", "bd_type","center_x","center_y","center_z","heading",
                "rel_center_x","rel_center_y","rel_center_z","rel_heading","speed_x","speed_y","u","v", "dim_x", "dim_y","img_path"]
        CSVDumpLoad.__init__(self, "trj_ground_truth", datafolder, cols)
        np.set_printoptions(suppress=True)
        
        return
    def get_corresponding_camera_box(self, laser_bd_id, frame):
        for bd in frame.projected_lidar_labels:
            if bd.name != 1:
                break
            u,v = None, None
            dim_x, dim_y = None, None
            for label in bd.labels:
                if laser_bd_id in label.id:
                    u,v = label.box.center_x, label.box.center_y 
                    dim_x, dim_y = label.box.length, label.box.width
                    break 
        img = None
        fname = "{}/{}_front.jpg".format(self.datafolder, frame.timestamp_micros)
        if os.path.exists(fname):
            return u,v, fname, dim_x, dim_y
        for image in frame.images:
            if image.name == 1:
                img = tf.image.decode_jpeg(image.image)
                img = np.array(img)
                mpimg.imsave(fname, img)
                print("saved file {}".format(fname))
                break           
                
        return u,v, fname, dim_x, dim_y
    def parse_frame(self, frame):
#         print(frame)
        frame_id = frame.timestamp_micros
        if frame_id < 1546479695312889:
            #extract about 5 seconds appropriatge segment only
            return
        TWV = np.array(frame.pose.transform).reshape(4,4)
        TWV = PoseInfo().construct_fromT(TWV)
        
        for bd in frame.laser_labels:
            center_x = bd.box.center_x
            center_y = bd.box.center_y
            center_z = bd.box.center_z
            heading = bd.box.heading
            
            rel_center_x = center_x
            rel_center_y = center_y
            rel_center_z = center_z
            rel_heading = heading
            
            speed_x = bd.metadata.speed_x
            speed_y = bd.metadata.speed_y
            bd_id = bd.id
            bd_type = bd.type
            u,v,img_path, dim_x, dim_y = self.get_corresponding_camera_box(bd_id, frame)
            #object pose in vehicle frame
            TVO = PoseInfo().construct_fromyprt(ypr = [heading, 0, 0], t= [center_x, center_y, center_z], use_angle = False)
            #get object pose in world frame
            TWO = TWV * TVO
            #save all the data to temp ditc
            center_x, center_y,center_z = TWO.t
            heading = TWO.ypr[0]
            
            for k in self.meta_data_dict.keys():
                self.meta_data_dict[k].append(eval(k))
        
            
            
            
        
        return
    def parse(self):
        #TODO: Write function that parses the tracking data and saves the results in a new file.
        dataset = tf.data.TFRecordDataset(self.tf_record_file, compression_type='')
        for data in dataset:
            frame = open_dataset.Frame()
            frame.ParseFromString(bytearray(data.numpy()))
            self.parse_frame(frame)
        
        self.dump()
        return
    def run(self):
        self.parse()
        print("done with dataset setup")
        return
    
if __name__ == "__main__":
    obj = DataReader()
    obj.run()
