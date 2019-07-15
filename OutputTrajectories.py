import VideoUtils as vu
import TetrodeUtils as tu
import sys
import struct
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from bisect import bisect_left

import numpy as np

def readTFile(filename):

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
  return ts

def takeClosest(myList, myNumber):
  pos = bisect_left(myList, myNumber)
  if pos == 0:
     return myList[0]
  if pos == len(myList):
     return myList[-1]

  before = myList[pos - 1]
  after = myList[pos]
  rpos = pos

  if after - myNumber < myNumber - before:
     return after
  else:
     return before


vidfile = './RawData/VT1.Nvt'
#testFile = './rec_09152017/VT1.Nvt'
with open(vidfile, 'rb') as f:
    videodata = f.read()[16384:]
 
#start_idx = 45326
#stop_idx = 180752
start_idx = int(sys.argv[1])
stop_idx = int(sys.argv[2])


x, y, ts = vu.getVideodata(videodata)
x = x[start_idx:stop_idx]
y = y[start_idx:stop_idx]
ts = ts[start_idx:stop_idx]

xfilt = vu.smooth(x, window_len=200)
yfilt = vu.smooth(y, window_len=200)

moving,notmoving,speed = vu.returnMoving(xfilt, yfilt, 30)
tstart, tstop = vu.returnTrajectoryFlags(moving, 240)

tspeed = [np.mean(np.asarray(speed[start:stop])) for start,stop in zip(tstart,tstop)]

#for dwells
moving,notmoving,speed = vu.returnMoving(xfilt, yfilt, 5)
dstart, dstop = vu.returnTrajectoryFlags(notmoving, 240)
dspeed = [np.mean(np.asarray(speed[start:stop])) for start,stop in zip(dstart,dstop)]

fig, ax = plt.subplots()

bgpoints = int(len(xfilt)/(len(xfilt)/10))
l1, = plt.plot(xfilt[1:len(xfilt):bgpoints],yfilt[1:len(yfilt):bgpoints],'.', markersize=3, color='#FFE4C4')
l2, = plt.plot(xfilt[tstart[0]], yfilt[tstart[0]], 'g.', markersize=20)
l3, = plt.plot(xfilt[tstop[0]], yfilt[tstop[0]], 'r.', markersize=20)

l4, = plt.plot(xfilt[tstart[0]:tstop[0]], yfilt[tstart[0]:tstop[0]], 'b.', markersize=5)

#plt.xlim([40000,np.amax(xfilt)+1000])
plt.xlim([np.amin(xfilt)-1000,np.amax(xfilt)+1000])
plt.ylim([np.amin(xfilt)-1000,np.amax(xfilt)+1000])


class Index(object):
    ind = 0

    def next(self, event):
        self.ind += 1
        ii=self.ind
        
        if ii < len(tstop):
			l3.set_xdata(xfilt[tstop[ii]])
			l3.set_ydata(yfilt[tstop[ii]])
			l2.set_xdata(xfilt[tstart[ii]])
			l2.set_ydata(yfilt[tstart[ii]])
			l4.set_xdata(xfilt[tstart[ii]:tstop[ii]])
			l4.set_ydata(yfilt[tstart[ii]:tstop[ii]])
			plt.draw()
		#else:
		 #   self.ind -= 1
	    
	   # plt.draw()

    def prev(self, event):
        self.ind -= 1
        ii=self.ind
        if ii > 0:
			l3.set_xdata(xfilt[tstop[ii]])
			l3.set_ydata(yfilt[tstop[ii]])
			l2.set_xdata(xfilt[tstart[ii]])
			l2.set_ydata(yfilt[tstart[ii]])
			l4.set_xdata(xfilt[tstart[ii]:tstop[ii]])
			l4.set_ydata(yfilt[tstart[ii]:tstop[ii]])
			plt.draw()
		#else:
		#    self.ind += 1
		#plt.draw()
        
  
callback = Index()      

axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()

recsize=1828

for i  in xrange(len(tstart)):
    
    recoffset=recsize*tstart[i]
    starttime = struct.unpack('q', videodata[recoffset+6:recoffset+14])[0]
     
    recoffset=recsize*tstop[i]
    stoptime = struct.unpack('q', videodata[recoffset+6:recoffset+14])[0]
    print("START: {}-----:> STOP: {}".format(starttime,stoptime))

np.savez("./RawData/POSITION", xfilt, yfilt, ts) 
np.savez("./RawData/TRAJECTORIES", tstart, tstop, tspeed)
np.savez("./RawData/NONTRAJECTORIES", dstart, dstop, dspeed)



