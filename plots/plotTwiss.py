import numpy as np

from TwissTable import TwissTable, stripQuotes

TT = TwissTable("twiss_ip1_b1.tfs")
TT.convertToNumpy()
TT.sliced_rebuild(500)

Smin = 26370

#import matplotlib
import matplotlib.pyplot as plt
from TwissPlotTools import *

plt.figure() # Plot beta functions
plt.plot(TT.data['S'],TT.data['BETX'],label=r"$\beta_x$")
plt.plot(TT.data['S'],TT.data['BETY'],label=r"$\beta_y$")

yPOS=max(TT.data['BETX']) # y position on plot of labels
plt.xlim(Smin,TT.metadata["LENGTH"])

drawThickElementMarkers(TT.elements,yPOS,Smin,None)
drawThinElementMarkers (TT,yPOS,Smin,None,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\beta$ [m]")

#plt.show()

plt.figure() # Plot beam sigmas
EX = TT.metadata["EX"]
EY = TT.metadata["EY"]
plt.plot(TT.data['S'],np.sqrt(TT.data['BETX']*EX)*1e3,label=r"$\sigma_x$")
plt.plot(TT.data['S'],np.sqrt(TT.data['BETY']*EY)*1e3,label=r"$\sigma_y$")

yPOS=np.sqrt(max(TT.data['BETX']*EX))*1e3 # y position on plot of labels
plt.xlim(Smin,TT.metadata["LENGTH"])

drawThickElementMarkers(TT.elements,yPOS,Smin,None)
drawThinElementMarkers (TT,yPOS,Smin,None,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\sigma$ [m]")

plt.figure() # Plot beam sigmas, centered.
#TT.shift("DRIFT_111")
TT.shift("MB.A8L1.B1..1")
TT.sliced_rebuild(500)
#print TT.elements
EX = TT.metadata["EX"]
EY = TT.metadata["EY"]
plt.plot(TT.data['S'],np.sqrt(TT.data['BETX']*EX)*1e3,label=r"$\sigma_x$")
plt.plot(TT.data['S'],np.sqrt(TT.data['BETY']*EY)*1e3,label=r"$\sigma_y$")
Smin = 560
drawThickElementMarkers(TT.elements,yPOS,None,Smin)
drawThinElementMarkers (TT,yPOS,None,Smin,("V", "ATLAS","BPM","BPTX","MC"))

plt.xlim(0,Smin)
plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\sigma$ [m]")


plt.show()
