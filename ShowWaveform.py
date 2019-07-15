 
from bisect import bisect_left
import numpy as np
import sys
import struct
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.lines as mlines
import TetrodeUtils as trode
from scipy.interpolate import interp1d
import matplotlib as mpl
import seaborn as sns
from matplotlib import rc
from matplotlib.pyplot import gca

sns.set(style="white")
#sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

font_paths = mpl.font_manager.findSystemFonts()
font_objects = mpl.font_manager.createFontList(font_paths)
font_names = [f.name for f in font_objects]
#print font_names
#rc('font', **{'family':'serif', 'serif':['Times']})
#rc('text', usetex=True)
rc('axes', linewidth=2)

def acf(x, length):
    return np.array([1]+[np.corrcoef(x[:-i], x[i:])[0,1] for i in range(1, length)])

def autocor(x,t):
    return np.corrcoef(x[0:len(x)-t], x[t:len(x)])[0,1]

ttfile=sys.argv[1]
print ttfile
ttfile=ttfile[:-20]
print(ttfile)

ts, waveforms = trode.readTetrode(ttfile)
totaltime = (ts[-1] - ts[0])/600000
print("totaltime: {}".format(totaltime/60.))
curatefile=ttfile
curatefile+=".firings.curated.mda"
print(curatefile)

with open(curatefile, 'rb') as f:  
	hdr = f.read()
	f.close()

print("data format {}".format(struct.unpack('i', hdr[0:4])[0]))
print("bytes per entry {}".format(struct.unpack('i', hdr[4:8])[0]))
print("n dimensions {}".format(struct.unpack('i', hdr[8:12])[0]))
print("size of dim 1 {}".format(struct.unpack('i', hdr[12:16])[0]))
nrecs = struct.unpack('i', hdr[16:20])[0]
print("number of events detected: {}".format(nrecs))
#nrecs = len(ts)

tindex = np.zeros(nrecs)
cluster = np.zeros(nrecs)
adj_index = np.zeros(nrecs)

for i in range(nrecs):
   offset = i*24
   tindex[i] = struct.unpack('d', hdr[28+offset:36+offset])[0]
   cluster[i] = struct.unpack('d', hdr[36+offset:44+offset])[0]
   adj_index[i] = (tindex[i]/128).astype(int)
   #print("tindex[] {}: cluster[] {}".format(tindex[i], cluster[i]))
   
u, indices = np.unique(cluster, return_inverse=True)

for suffix in u:
   sns.set
   fig = plt.figure(figsize=(8,10))
 
   print("Cluster number {}".format(suffix))

   indx = adj_index[np.where(cluster == suffix)].astype(int)
   print(suffix)
   filename = "{}_{}".format(ttfile[:-4], np.int(suffix))
#   idx = int(adj_index[indx]);
   print(ts[indx])
   
   print(filename)
  
#   test = adj_index[indx].astype(int)
   smallwave = np.zeros([4,32,len(indx)])
   spikes = np.zeros(len(indx))
   print("Number of spikes {}".format(len(spikes)))
   print("Firing Rate {}".format(len(spikes)/totaltime))

   for i in range(len(indx)):
       smallwave[:,:,i]=waveforms[:,:,indx[i]]
   
   plot_colors = ['b', 'g', 'r', 'c']

   #compute spike statistics
   wave_mean = np.zeros([4,32])

#   fig = plt.figure()

   for i in range(4):
      wave_mean[i,:] = np.mean(smallwave[i,:,:], axis=1)
#   sns.set(font_scale=5)
   np.savez(filename, wave_mean)
 
   #fig.savefig(filename, dpi='figure')
#   csfont = {'fontname':'Arial'}
#   hfont = {'fontname':'Helvetica'}

  # plt.ylabel("Amplitude(uV)", fontname='Verdana', fontweight='bold')
 
  # plt.xlabel("Time(ms)",fontname='Verdana', fontweight='bold')
  # fig.savefig("./PLOT.png", dpi='figure')

   plt.show()

   


