import cPickle
import os
from dumpload import DumpLoad

class DumpLoadData(object):
    def __init__(self, root_file, data_seqid = 1, dumped_file = "simulated_data.data"):
        
        datafolder = os.path.abspath(os.path.join(os.path.dirname(root_file), 'temp/'))
        datafolder = '{}/{}'.format(datafolder, data_seqid)
        if not os.path.exists(datafolder):
            os.makedirs(datafolder)
        self.datafolder = datafolder
        self.dumploadtool = DumpLoad('{}/simulated.data'.format(datafolder))
        return
    def dump(self, data):     
        self.dumploadtool.dump(data)
        print("Data saved to {}".format(self.dumploadtool.filename))
        return
    def is_data_exist(self):
        file_path = self.dumploadtool.filename
        if os.path.exists(file_path):
            return True
        else:
            return False
        return
    def load(self):
        res = self.dumploadtool.load()
        print("simulated data loaded from {}".format(self.dumploadtool.filename))
        return res