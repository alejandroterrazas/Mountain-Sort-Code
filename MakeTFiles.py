 
from bisect import bisect_left
import numpy as np
import sys
import struct
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.lines as mlines
import TetrodeUtils as trode

def acf(x, length):
    return np.array([1]+[np.corrcoef(x[:-i], x[i:])[0,1] for i in range(1, length)])

def autocor(x,t):
    return np.corrcoef(x[0:len(x)-t], x[t:len(x)])[0,1]
    #for l in range(len(x)):
    #   print(x[l])



ttfile=sys.argv[1]
ttfile=ttfile[:-12]

print(ttfile)

ts, waveforms = trode.readTetrode(ttfile)

#for timest in ts:
#    print(timest)

totaltime = (ts[-1] - ts[0])/600000
print("totaltime: {}".format(totaltime/60.))
curatefile=ttfile
curatefile+=".firings.mda"
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
   fig = plt.figure(figsize=(8,10))
   gs1 = GridSpec(3,4)
   gs1.update(hspace=0.4, wspace=0.1,left=0.10, right=0.48, top = 0.95, bottom = 0.3)
   
   gs2 = GridSpec(3,3)
   gs2.update(left=0.58, right=.98, top = 0.95, bottom = 0.3, wspace=0.05)

   gs3 = GridSpec(1,1)
   gs3.update(left=0.10, right=.98, top=.2, bottom = 0.05, wspace=0.05)

   print("Cluster number {}".format(suffix))

   indx = adj_index[np.where(cluster == suffix)].astype(int)
   print(suffix)
   filename = "{}_{}.t".format(ttfile[:-4], np.int(suffix))
#   idx = int(adj_index[indx]);
   print(ts[indx])
   
   print(filename)

   with open(filename, 'wb') as f:
      f.write(ts[indx])
      f.close()
   
#   test = adj_index[indx].astype(int)
   smallwave = np.zeros([4,32,len(indx)])
   spikes = np.zeros(len(indx))
   peaks = np.zeros([4,len(indx)])
   troughs = np.zeros([4,len(indx)])
   print("Number of spikes {}".format(len(spikes)))
   print("Firing Rate {}".format(len(spikes)/totaltime))

   for i in range(len(indx)):
       smallwave[:,:,i]=waveforms[:,:,indx[i]]
       spikes[i] = ts[indx[i]]
       for j in range(4):
          peaks[j,i] = np.max(waveforms[j,:,indx[i]])
          troughs[j,i] = np.min(waveforms[j,:,indx[i]])
    
   isi = np.where(np.diff(spikes)>0, np.log10(np.diff(spikes/1000.)), 0)
   binvals = [5*i/500. for i in range(500)]

   n_noise = len(np.where(np.diff(spikes/1000.) <= 2))
   print("# spikes less than 2 ms {}".format(n_noise))
   hisi, bin_edges = np.histogram(isi, bins = binvals)
    
   ax1 = plt.subplot(gs1[:-1, :])
   #ax1.set_autoscaley_on(False)
   #ax1.set_xlim([2,10])
   ax1 = plt.plot(bin_edges[:-1], hisi, '-')
   plt.ylabel('# of spikes')
   plt.xlabel('Log10 interspike interval')
   locs, labs = plt.xticks()

   for lab,loc in zip(labs,locs):
     lab.set_text("$10^{0}$".format(loc.astype(int)))
       
   plt.xticks(locs[1:-1], labs[1:-1])
   
   #compute spike statistics
   wave_std = np.zeros([4,32])
   wave_mean = np.zeros([4,32])

   for i in range(4):
      wave_mean[i,:] = np.mean(smallwave[i,:,:], axis=1)
      for j in range(32):
         wave_std[i,:] = np.std(smallwave[i,j,:])

   amplimax = np.zeros(4)
   amplimin = np.zeros(4)

   for i in range(4):
      amplimax[i] = np.mean(peaks[i,:])
      amplimin[i] = np.mean(troughs[i,:])

   amax = np.max(amplimax)
   amin = np.min(amplimin)
   plot_colors = ['b', 'g', 'r', 'c']
   for i in range(4):
     amplimax[i] = np.mean(peaks[i,:])
     amplimin[i] = np.mean(troughs[i,:])

     ax = plt.subplot(gs1[-1,i])
     ax.set_autoscaley_on(False)
     ax.set_ylim([amin-100,amax+100])
   
     ax.text(32,amplimax[i],"{}".format(amplimax[i].astype(int)),ha='right', va='top') 
     plt.plot(wave_mean[i,:], plot_colors[i])
     plt.plot([0,32],[amplimax[i],amplimax[i]],'k')
     for j in range(32):
        plt.plot([j,j], [wave_mean[i,j]-wave_std[i,j], wave_mean[i,j]+wave_std[i,j]],plot_colors[i])
     ax.set_axis_off()

   #done with spike plots

   filename = "{}_{}.t".format(ttfile[:-4], np.int(suffix))

   ax6 = plt.subplot(gs2[0, :])
  
   max_index=np.where(wave_mean[0,:]==np.max(wave_mean[0,:]))[0]
   max_index = max_index[0] 
   print("WTF {}".format(max_index))
   half_max = wave_mean[0,max_index]/2.
   pre_peak = wave_mean[0,:max_index]
   post_peak = wave_mean[0,max_index:]
   
   fwhm_pre, pre_index  = trode.find_nearest(pre_peak,half_max)
   fwhm_post, post_index  = trode.find_nearest(post_peak,half_max)
 
   print(np.where(wave_mean[0,:]==fwhm_post)[0]-np.where(wave_mean[0,:]==fwhm_pre)[0])
   print("fwhm_pre {}".format(fwhm_pre))
   print("fwhm_post {}".format(fwhm_post))

   #find nearest left and right


   ax6.text(0,1.0,"Cluster number {}".format(filename), ha='left', va='center',fontsize=14) 
   ax6.text(0,.9,"Number of spikes: {}".format(len(spikes)), ha='left', va='center', fontsize=12)
   ax6.text(0,.8,"Firing Rate: %3.2f Hz" % (len(spikes)/totaltime), ha='left', va='center',fontsize=12)
   ax6.text(0,.7,"Total Time: %3.2f minutes" % (totaltime/60.), ha='left', va='center', fontsize=12)
  # ax6.text(0,.6,"Width at half max: (1,2,3,4): %3.2f, %3.2" %totaltime/60., %totaltime/60., ha='left', va='center', fontsize=12)
  # ax6.text(0,.7,"Total Time: %3.2f minutes" % (totaltime/60.), ha='left', va='center', fontsize=12)


   ax6.set_axis_off()
   
   ax7 = plt.subplot(gs2[-1, :])
   spikes_ms = spikes/24000
   spikes_ms = spikes_ms - spikes_ms[0]

   spike_bins = np.zeros(spikes_ms[-1].astype(int)+1)
   spike_bins[spikes_ms.astype(int)] = 1
   auto_correlogram=np.zeros(250)
   for k in range(250):
       auto_correlogram[k] = autocor(spike_bins,k)
     
   plt.plot(auto_correlogram[1:], 'k-')
   ax8 = plt.subplot(gs3[0,:])
   spikes_m = (spikes-ts[0])/36000000
   plot_dotcolors = ['b.','g.','r.', 'c.']

   for i in range(4):
      plt.plot(spikes_m, peaks[i,:], plot_dotcolors[i], markersize=1)
      plt.plot([0, spikes_m[-1]],[amplimax[i],amplimax[i]],plot_colors[i], linewidth=2)


   locs, labs = plt.xticks()
  
   for lab,loc in zip(labs,locs):
     lab.set_text("{}".format(loc))

   plt.xticks(locs[1:-1], labs[1:-1])
   mng = plt.get_current_fig_manager()
   mng.full_screen_toggle()
   filename +=".png"      
   fig.savefig(filename, dpi='figure')
   #plt.show()

