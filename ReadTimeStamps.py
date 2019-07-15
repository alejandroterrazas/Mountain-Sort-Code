"""
TimeStamp : UInt64
ChannelNumber: UInt32
SampleFreq: UInt32
NumValidSample: UInt32
Samples: Int16[]
"""
from __future__ import division


import struct
import numpy as np
import sys
from mlpy import writemda16i, writemda32
#from matplotlib import pyplot as plt

#print(sys.argv[1])   
#filename = sys.argv[1]
filename = "./RawData/Sc11_5.t"
with open(filename, 'rb') as f:  
    #hdr = f.read()[:16384]
    #print(hdr)
    tsdata  = f.read()
    recsize = 8
    nevents = int(len(tsdata)/recsize)
    print("nevents: {}".format(nevents))

    ts = np.zeros(nevents)
 
    for i in range(nevents):
     recoffset=recsize*i
     dnParams = np.zeros(8)
     #print recoffset
     ts[i] = struct.unpack('d', tsdata[recoffset:recoffset+8])[0]
     print(ts[i])
