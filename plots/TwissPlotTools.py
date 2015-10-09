import matplotlib
import matplotlib.pyplot as plt
from TwissTable import stripQuotes

def getColor(elemName):
    "Return standard colors for elements"
    
    if elemName.startswith("MB"):   # Bending magnet
        return "blue"
    elif elemName.startswith("MQ"): # Quadrupole magnet
        return "red"
    elif elemName.startswith("T"):  # Targed/collimator etc.
        return "darkgreen" 
    elif elemName.startswith("A"):  # RF
        return "magenta"
    return "k"

def drawThickElementMarkers(elements, yPOS, sMin=None):
    "Draw thick markers using the element types produced by TwissTable::sliced_rebuild."
    ax = plt.gca()
    for el in elements:
        if sMin != None and el[1] < sMin:
            continue
        #print el
        sPOS = elements[el]

        textcolor=getColor(el)

        #Type 1 annotation
        # plt.annotate(
        #     '', xy=(sPOS[0], yPOS*0.7), xycoords='data',
        #     xytext=(sPOS[1], yPOS*0.7), textcoords='data',
        #     #arrowprops={'arrowstyle': '<->', 'shrink':0.0},
        #     arrowprops=dict(arrowstyle='<->', shrinkA=0.0,shrinkB=0.0),
        #     color=textcolor)

        # plt.annotate(
        #     el,
        #     xy=(0.5*(sPOS[1]+sPOS[0]), yPOS*0.7), xycoords='data',
        #     xytext=(0, 5), textcoords='offset points',
        #     color=textcolor, ha="center")
        
        #Type 2 annotation
        ax.add_patch(matplotlib.patches.Rectangle(
            (sPOS[0],yPOS*0.0),sPOS[1]-sPOS[0],yPOS*1.2,
            color=textcolor,alpha=0.5,edgecolor="none"
        ))
        plt.annotate(
            el,
            xy=(0.5*(sPOS[1]+sPOS[0]), yPOS), xycoords='data',
            xytext=(0, 0), textcoords='offset points',
            rotation="vertical",color=textcolor,va="center",ha="center"
        )


def drawThinElementMarkers(TT,yPOS,sMin=None,skipList=None):
    prevS = -1.0
    for (i,s,name) in zip(xrange(TT.N),map(float,TT.data["S"]),map(stripQuotes,TT.data["NAME"])):
        if sMin!=None and s < sMin:
            continue

        if float(TT.data["L"][i]) > 0.0:
            #Thin elements only
            continue
        if ".." in name:
            #Sliced elements, skip
            continue
        
        #Declutter
        doSkip = False
        for skip in skipList:
            if name.startswith(skipList):
                doSkip=True
        if doSkip:
            continue

        if TT.elements!=None and name in TT.elements:
            continue

        if prevS == s:
            continue
        prevS=s

        textcolor=getColor(name)

        plt.axvline(s,ls="--",color=textcolor)
        plt.text(s,yPOS,name,rotation="vertical",color=textcolor,va="center",ha="right")

        #Print a few selected elements:
        # if name.startswith("TCT") or name.startswith("TAS") or name.startswith("TAN"):
        #     print name, TT.data["S"][i], TT.data["BETX"][i], TT.data["BETY"][i]
