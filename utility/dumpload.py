import pickle as cPickle

class DumpLoad(object):
    def __init__(self, _filename):
        self.filename = _filename
        return
    def dump(self, data):
        with open(self.filename, "wb") as output_file:
            cPickle.dump(data, output_file)
        return
    def load(self):
        with open(self.filename, "rb") as input_file:
            e = cPickle.load(input_file)
        return e