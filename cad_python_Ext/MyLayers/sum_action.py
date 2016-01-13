import unittest
import tempfile
import os
import numpy

import caffe

class sum_action(caffe.Layer):
    """A layer that initialize messages for recurrent belief propagation"""

    def setup(self, bottom, top):
        self.nScene = 5
        self.nAction = 7
        self.nPeople = 14
        self.K_ = 0;
        self.bottom_batchsize = 0
        self.unitlen = 0
        self.output_num = 0
        self.bottom_batchsize = 0
        self.top_batchsize = 0
        self.bottom_output_num = 0
        self.top_output_num = 0
        self.top_shape = []
        self.label_stop = []
    
    def reshape(self, bottom, top):
        # have one input one output, initialize messages for each node in the graphical model 
        bottom_shape = bottom[0].data.shape 
        self.bottom_batchsize = bottom_shape[0]
        self.nPeople = bottom_shape[1]
        self.bottom_output_num = bottom_shape[2]
        self.top_batchsize = self.bottom_batchsize
        self.top_output_num = self.nAction
        top[0].reshape(self.top_batchsize,self.nPeople,self.nAction)

    def forward(self, bottom, top):
        labels = bottom[1].data
        count = 0
        label_stop = numpy.ones([bottom[1].data.shape[0]])
        for i in range(0,self.top_batchsize):
            for j in range(0,self.nPeople):
                if labels[i*self.nPeople+j] == 0:
                    label_stop[i] = j
                    break
        self.label_stop = label_stop
        #print bottom[0].data.shape
        #print self.bottom_output_num
        #print bottom[0].data.shape
        tmpdata = numpy.reshape(bottom[0].data,[self.top_batchsize,self.nPeople,self.bottom_output_num/self.nAction,self.nAction])
        for i in range(0,self.top_batchsize):
            for j in range(0, self.nPeople):
                if j >= label_stop[i]:
                    tmp = numpy.zeros([1,self.nAction])
                    continue
                tmpdata[i,j,label_stop[i]:self.nPeople] = numpy.zeros([self.nPeople-label_stop[i],self.nAction])
                #print 'data',i,j
                #print tmpdata[i,j,0]
                tmp = tmpdata[i,j].sum(axis = 0)
                top[0].data[i,j] = tmp/(self.label_stop[i]+1+2*(self.K_>0))

    def backward(self, top, propagate_down, bottom):
        label_stop = self.label_stop
        tmpdiff = top[0].diff
        tm = numpy.zeros([0,0])
        for i in range(0,self.top_batchsize):
            for j in range(0,self.nPeople):
                assert(self.label_stop[i]!=0)
                fortmp = numpy.repeat(tmpdiff[i,j],self.bottom_output_num/self.nAction,axis = 0)
                fortmp = numpy.reshape(fortmp,[1,self.bottom_output_num])
                tmp = fortmp/(self.label_stop[i]+1+2*(self.K_>0))
                bottom[0].diff[i,j] = tmp

def python_net_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write("""name: 'pythonnet' force_backward: true
        input: 'data' input_shape { dim: 10 dim: 9 dim: 8 }
        layer { type: 'Python' name: 'one' bottom: 'data' top: 'one'
          python_param { module: 'test_python_layer' layer: 'SimpleLayer' } }
        layer { type: 'Python' name: 'two' bottom: 'one' top: 'two'
          python_param { module: 'test_python_layer' layer: 'SimpleLayer' } }
        layer { type: 'Python' name: 'three' bottom: 'two' top: 'three'
          python_param { module: 'test_python_layer' layer: 'SimpleLayer' } }""")
        return f.name

class TestPythonLayer(unittest.TestCase):
    def setUp(self):
        net_file = python_net_file()
        self.net = caffe.Net(net_file, caffe.TRAIN)
        os.remove(net_file)

    def test_forward(self):
        x = 8
        self.net.blobs['data'].data[...] = x
        self.net.forward()
        for y in self.net.blobs['three'].data.flat:
            self.assertEqual(y, 10**3 * x)

    def test_backward(self):
        x = 7
        self.net.blobs['three'].diff[...] = x
        self.net.backward()
        for y in self.net.blobs['data'].diff.flat:
            self.assertEqual(y, 10**3 * x)

    def test_reshape(self):
        s = 4
        self.net.blobs['data'].reshape(s, s, s, s)
        self.net.forward()
        for blob in self.net.blobs.itervalues():
            for d in blob.data.shape:
                self.assertEqual(s, d)
