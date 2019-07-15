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
#from mlpy import writemda16i, writemda32
from matplotlib import pyplot as plt

filename = sys.argv[1]


recsize = 304   


with open(filename, 'rb') as f:  

    spikedata = f.read()[16384:]
    f.close()
    nevents=int(len(spikedata)/recsize)
    nevents = 5000
    print("Number of events: {}".format(nevents))
    ts= np.zeros(nevents)
    dwScnumber = np.zeros(nevents)
    dwCellnumber = np.zeros(nevents)
    snData = np.zeros(32) 
    snD = []
 
    for i in range(nevents):
     recoffset=recsize*i
     dnParams = np.zeros(8)
     #print recoffset
     ts[i] = struct.unpack('Q', spikedata[recoffset:recoffset+8])[0]
     dwScnumber[i] = struct.unpack('I', spikedata[recoffset+8:recoffset+12])[0]
     dwCellnumber[i] = struct.unpack('I', spikedata[recoffset+12:recoffset+16])[0]
     dnParams = struct.unpack('8I', spikedata[recoffset+16:recoffset+48])[0]
     x=np.zeros(128)
     for j in range(128):
        x[j] = struct.unpack('h', spikedata[recoffset+48+(j*2):recoffset+48+(j*2)+2])[0]

     snD.append(x)
#waveforms = np.zeros([4,32,nevents])

waveforms = np.zeros([4,64,nevents], dtype=np.int16)

for i in range(nevents):   
   waveforms[:,16:48,i] = snD[i].reshape([32,4]).transpose()

bigmat = np.zeros([4,64*nevents],dtype=np.int16)

for i in range(4):
   bigmat[i,:] = waveforms[i,:,:].flatten('F')
   

plt.plot(bigmat[:,:].transpose())
plt.show()

   
plt.plot(waveforms[0,:,:])
plt.show()

f, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharex=True, sharey=True)
ax1.plot(np.mean(waveforms[0,:,:],axis=1), 'r')
ax2.plot(np.mean(waveforms[1,:,:],axis=1), 'r')
ax3.plot(np.mean(waveforms[2,:,:],axis=1), 'r')
ax4.plot(np.mean(waveforms[3,:,:],axis=1), 'r')

plt.show()


