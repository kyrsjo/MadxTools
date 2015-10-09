import numpy as np

def stripQuotes(inStr):
    outStr = inStr
    if inStr[0]=='"' and inStr[-1]=='"':
        outStr = inStr[1:-1]
    return outStr


class TwissTable:
    tfsName = None
    metadata = None
    variableNames = None
    variableTypes  = None
    data = None

    N = None

    def __init__(self,tfsName):
        self.tfsName = tfsName
        tfsFile = open(tfsName,'r')

        self.metadata = {}
        self.variableNames = []
        self.variableTypes  = []
        self.data = {}
        
        self.N = 0

        for line in tfsFile.xreadlines():
            #print line
            if line[0]=="@":
                #Metadata
                ls = line.split()[1:]
                ls[2]=stripQuotes(ls[2])
                self.metadata[ls[0]] = (ls[1],ls[2])
            elif line[0]=="*":
                #Header/variable names
                ls = line.split()[1:]
                for l in ls:
                    self.variableNames.append(l)
                    self.data[l]=[]
            elif line[0]=="$":
                #Header/variable types
                ls = line.split()[1:]
                for l in ls:
                    self.variableTypes.append(l)
            else:
                #Data
                ls = line.split()
                assert len(ls) == len(self.variableNames)
                for (l,vn) in zip(ls,self.variableNames):
                    self.data[vn].append(l)
                self.N += 1
                #break
        tfsFile.close()

        #print self.metadata
        #print self.variableNames
        #print self.variableTypes
        #print
        #print self.data
                
                


TT = TwissTable("twiss_ip1_b1.tfs")

import matplotlib
import matplotlib.pyplot as plt
plt.plot(TT.data['S'],TT.data['BETX'],label=r"$\beta_x$")
plt.plot(TT.data['S'],TT.data['BETY'],label=r"$\beta_y$")

Smin = 26370

plt.xlim(Smin,float(TT.metadata["LENGTH"][1]))

#Rebuilt sliced elements
currElementName  = None
currElementStart = None
currElementEnd   = None
elements = {}
maxSearch = 500#None
for i in xrange(TT.N):
    #look for sliced element
    name1 = stripQuotes(TT.data["NAME"][i])
    ns1 = name1.split("..")
    if len(ns1) == 2:
        if not ns1[0] in elements:
            #print "Searching for", ns1[0],i
            
            idx = int(ns1[1])
            assert idx == 1
            
            sMin = float(TT.data["S"][i])
            sMax = float(TT.data["S"][i])
            maxj = TT.N
            if maxSearch != None:
                maxj = min(TT.N,i+1+maxSearch)
            for j in xrange(i+1, maxj):
                name2 = stripQuotes(TT.data["NAME"][j])
                ns2 = name2.split("..")
                if len(ns2)==2:
                    if ns2[0] == ns1[0]:
                        #print "\t sub", ns2[0],j
                        idx += 1
                        assert idx == int(ns2[1])
                        sMax = float(TT.data["S"][j])
            elements[ns1[0]] = (sMin,sMax)

#print elements

def getColor(elemName):
    if elemName.startswith("MB"):
        return "blue"
    elif elemName.startswith("MQ"):
        return "red"
    elif elemName.startswith("T"):
        return "darkgreen" 
    elif elemName.startswith("A"):
        return "magenta"
    return "k"
yPOS=max(map(float,TT.data['BETX']))


#Draw sliced elements
ax = plt.gca()
for el in elements:
    if el[1] < Smin:
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
    
#Draw markers
prevS = -1.0
for (i,s,name) in zip(xrange(TT.N),map(float,TT.data["S"]),map(stripQuotes,TT.data["NAME"])):
    if s < Smin:
        continue
        
    if float(TT.data["L"][i]) > 0.0:
        #Thin elements; skip DRIFT
        #print name, TT.data["L"][i]
        continue
    if ".." in name:
        #Sliced elements, skip
        continue

    if name.startswith("V") or name.startswith("ATLAS") or name.startswith("BPM") or name.startswith("BPTX") or name.startswith("MC"):
        #Declutter
        continue
    
    if name in elements:
        continue

    if prevS == s:
        print "Double?", i,s,name
        continue
    prevS=s
    #print s,name
    
    textcolor=getColor(name)
    
    plt.axvline(s,ls="--",color=textcolor)
    plt.text(s,yPOS,name,rotation="vertical",color=textcolor,va="center",ha="right")
    
    #Print a few selected elements:
    if name.startswith("TCT") or name.startswith("TAS") or name.startswith("TAN"):
        print name, TT.data["S"][i], TT.data["BETX"][i], TT.data["BETY"][i]

plt.legend(loc=6)

plt.show()
