from utility.dumpload import DumpLoad
import numpy as np
import pandas as pd
import os

class CSVDumpLoad(object):
    def __init__(self, _name,datafolder, _cols):
        
        self.name = _name
        
        self.meta_data_dict = self.gen_csv_dict(_cols)
        self.cols = _cols
        self.datafolder = datafolder
        if not os.path.exists(datafolder):
            os.makedirs(datafolder)
       
        return
    def get_data_dict(self):
        return self.meta_data_dict
    def gen_csv_dict(self, cols):
        meta_data_dict ={}
        for col in cols:
            meta_data_dict[col] = []
        return meta_data_dict
    def dump(self):
        df = pd.DataFrame(self.meta_data_dict)
        csv_file_name = "{}/{}.csv".format(self.datafolder, self.name)
        df.to_csv(csv_file_name, index=False, columns=self.cols)    
        print("saved file {}".format(csv_file_name))  
        
        dump_file_name = '{}/{}.data'.format( self.datafolder, self.name)
        DumpLoad(dump_file_name).dump(df)
        return df
    def load(self):
        dump_file_name = '{}/{}.data'.format( self.datafolder, self.name)
        df = DumpLoad(dump_file_name).load()
        return df
    def run(self):
        return
    
if __name__ == "__main__":   
    obj= CSVDumpLoad(None)
    obj.run()
        
        