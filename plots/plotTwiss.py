import numpy as np

from TwissTable import TwissTable, stripQuotes

TT = TwissTable("twiss_ip1_b1.tfs")
TT.sliced_rebuild(500)

#import matplotlib
import matplotlib.pyplot as plt
from TwissPlotTools import *
plt.plot(TT.data['S'],TT.data['BETX'],label=r"$\beta_x$")
plt.plot(TT.data['S'],TT.data['BETY'],label=r"$\beta_y$")

Smin = 26370
yPOS=max(map(float,TT.data['BETX'])) # y position on plot of labels
plt.xlim(Smin,float(TT.metadata["LENGTH"][1]))

drawThickElementMarkers(TT.elements,yPOS,Smin)
drawThinElementMarkers (TT,yPOS,Smin,("V", "ATLAS","BPM","BPTX","MC"))

plt.legend(loc=6)

plt.show()
