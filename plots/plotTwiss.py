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

yPOS_beta=max(TT.data['BETX']) # y position on plot of labels
plt.xlim(Smin,TT.metadata["LENGTH"])

drawThickElementMarkers(TT.elements,yPOS_beta,Smin,None)
drawThinElementMarkers (TT,yPOS_beta,Smin,None,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\beta$ [m]")

#plt.show()

#Print the emittance
mp = 0.938272046e9
e_tot = 7e12
gamma_rel = e_tot/mp
beta_rel = np.sqrt(gamma_rel**2 - 1)/gamma_rel

# Get emittance from TWISS file
#EX=TT.metadata["EX"]
#EY=TT.metadata["EY"]
# Set emittance manually
EX = 3.5e-6/gamma_rel*beta_rel
EY = 3.5e-6/gamma_rel*beta_rel

EX_norm = EX*gamma_rel*beta_rel
EY_norm = EY*gamma_rel*beta_rel
print "EX =", EX, "->", EX_norm
print "EY =", EY, "->", EY_norm

#Print a few selected elements:
print "NAME S[m] BETA_X[m] SIGMA_X[m] BETA_Y[m] SIGMA_Y[m]"
TCT_PATTERN="TCT.*L1\.B1"
import re
for (i,s,name) in zip(xrange(TT.N),TT.data["S"],TT.data["NAME"]):
    #if name.startswith("TCT") or name.startswith("TAS") or name.startswith("TAN"):
    if re.match(TCT_PATTERN,name) or name.startswith("TAN"):
        print name, TT.data["S"][i], TT.data["BETX"][i], np.sqrt(TT.data["BETX"][i]*EX), TT.data["BETY"][i], np.sqrt(TT.data["BETY"][i]*EY)

plt.figure() # Plot beam sigmas
plt.plot(TT.data['S'],np.sqrt(TT.data['BETX']*EX)*1e3,label=r"$\sigma_x$")
plt.plot(TT.data['S'],np.sqrt(TT.data['BETY']*EY)*1e3,label=r"$\sigma_y$")

yPOS_sigma=np.sqrt(max(TT.data['BETX']*EX))*1e3 # y position on plot of labels
plt.xlim(Smin,TT.metadata["LENGTH"])

drawThickElementMarkers(TT.elements,yPOS_sigma,Smin,None)
drawThinElementMarkers (TT,yPOS_sigma,Smin,None,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\sigma$ [mm]")
plt.title(r"$\epsilon_N$ = %.2f [mm*mrad]" % (EX_norm*1e6,))

plt.figure() #Plot orbit
yPOS_orbit = max(max(TT.data['X']),max(TT.data['Y']))
plt.plot(TT.data['S'],TT.data['X']*1e3,label=r"$x$")
plt.plot(TT.data['S'],TT.data['Y']*1e3,label=r"$y$")

plt.xlim(Smin,TT.metadata["LENGTH"])

drawThickElementMarkers(TT.elements,yPOS_orbit*1e3,Smin,None,True)
drawThinElementMarkers (TT,yPOS_orbit*1e3,Smin,None,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"Orbit [mm]")

plt.figure() # Plot beam sigmas, centered.
#TT.shift("DRIFT_111")
TT.shift("MB.A8L1.B1..1")
TT.sliced_rebuild(500)
#print TT.elements
plt.plot(TT.data['S'],np.sqrt(TT.data['BETX']*EX)*1e3,label=r"$\sigma_x$")
plt.plot(TT.data['S'],np.sqrt(TT.data['BETY']*EY)*1e3,label=r"$\sigma_y$")
Smin = 560
drawThickElementMarkers(TT.elements,yPOS_sigma,None,Smin)
drawThinElementMarkers (TT,yPOS_sigma,None,Smin,("V", "ATLAS","BPM","BPTX","MC"))

plt.xlim(0,Smin)
plt.legend(loc=6)
plt.xlabel("s [m]")
plt.ylabel(r"$\sigma$ [mm]")



plt.show()
