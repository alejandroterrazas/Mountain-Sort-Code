import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

npzfile = np.load("./interneuron/Sc6_4.npz")

iwave = npzfile['arr_0']

npzfile = np.load("./05-04Cut/Sc10_7.npz")

pwave = npzfile['arr_0']


print iwave[0,0]
print pwave[0,0]

iwave += -1*iwave[0,0]
pwave += -1*pwave[0,0]
#pwave *= 2
iwave = iwave/np.amax(iwave[0,:])
pwave = pwave/np.amax(pwave[0,:])
#print np.amax(iwave[0,:])
fig = plt.figure()
red_patch = mpatches.Patch(color='red', label="Pyramidal Cell")
green_patch = mpatches.Patch(color='green', label="Inhibitory Cell")
plt.legend(handles=[red_patch,green_patch])
ax = plt.subplot(111)

ax.plot(iwave[0,:], 'g')
ax.plot(pwave[0,:], 'r')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


locs, labs = plt.xticks()

plt.xticks([0,16,32])
plt.yticks([-.75,0,1.0])

locs, labs = plt.xticks()
labs[0].set_text("0")
labs[1].set_text("50")
labs[2].set_text("100")

plt.xticks(locs,labs)

plt.ylabel("Normalized Amplitude", fontname='Verdana', fontweight='bold')
plt.xlabel("Time(ms)", fontname='Verdana', fontweight='bold')

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


#plt.tight_layout()
fig.savefig("./PLOTA.png", dpi=1200)

plt.show()

