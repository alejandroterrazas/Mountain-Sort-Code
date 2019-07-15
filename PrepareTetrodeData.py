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

recsize = 304   
#args = str(sys.argv)
filename = sys.argv[1]

print("************Processing {} ...".format(filename))

with open(filename, 'rb') as f:  
    spikedata = f.read()[16384:]
    f.close()
    
nevents = int(len(spikedata)/recsize)
print("nevents: {}".format(len(spikedata)/304))

ts = np.zeros(nevents)
spiketrain = np.zeros([4,128,nevents], dtype=np.int16)

 
for i in range(nevents):
    recoffset=recsize*i
    #print("rec offset {}".format(recoffset))

    ts[i] = struct.unpack('Q', spikedata[recoffset:recoffset+8])[0]
    x=np.zeros(128)
 
    for j in range(128):
       x[j] = struct.unpack('h', spikedata[recoffset+48+(j*2):recoffset+48+(j*2)+2])[0]

    spiketrain[:,48:80,i] = x.reshape([32,4]).transpose()

print('here')

bigmat = np.zeros([4,128*nevents], dtype=np.int16)

print('here also')

for i in range(4):
    bigmat[i,:] = spiketrain[i,:,:].flatten('F')


print("...Done writing raw.mda for {}".format(filename))

#plt.plot(bigmat[:,0:4000].transpose())
#plt.show()
#uncomment the following line when MS allow event times
#writemda32(firings,'event_times.mda');
filename +=".raw.mda"
print(filename)
writemda16i(bigmat,filename);


