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
from matplotlib import pyplot as plt

recsize = 304   
#args = str(sys.argv)
filename = sys.argv[1]

print("************Processing {} ...".format(filename))

def read_data(fname):
  with open(fname, 'rb') as f:  
    data = f.read()[16384:]
    f.close()
    print('raw data is read')
  return data

def read_spikes(fname):
   spikedata = read_data(fname)

   nevents = int(len(spikedata)/recsize)
   print("nevents: {}".format(len(spikedata)/304))

   spiketrain = np.zeros([4,128,nevents], dtype=np.int8)
 
   for i in range(nevents):
      recoffset=recsize*i

      #print("rec offset {}".format(recoffset))

      x=np.zeros(128)
 
      for j in range(128):
         x[j] = struct.unpack('h', spikedata[recoffset+48+(j*2):recoffset+48+(j*2)+2])[0]
      #32,32,32,32
      spiketrain[:,48:80,i] = x.reshape([32,4]).transpose()
      plt.plot(spiketrain[0,:,i].flatten('F')
)
      plt.show()    
   
   return nevents, spiketrain.reshape([4,128*nevents])


print('here')

nevents,spiketrain = read_spikes(filename)

#plt.plot(spiketrain[:,0:4000]))
plt.show()
#uncomment the following line when MS allow event times
#writemda32(firings,'event_times.mda');
filename +=".raw.mda"
print(filename)
writemda16i(spiketrain.reshape([4,128*nevents]),filename);


