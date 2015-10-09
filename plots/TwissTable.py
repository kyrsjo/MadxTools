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
    
    elements = None
    def sliced_rebuild(self,maxSearch=None):
        "Rebuil sliced elements. Argue"
        currElementName  = None
        currElementStart = None
        currElementEnd   = None
        self.elements = {}
        for i in xrange(self.N):
            #look for sliced element
            name1 = stripQuotes(self.data["NAME"][i])
            ns1 = name1.split("..")
            if len(ns1) == 2:
                if not ns1[0] in self.elements:
                    #print "Searching for", ns1[0],i

                    idx = int(ns1[1])
                    assert idx == 1

                    sMin = float(self.data["S"][i])
                    sMax = float(self.data["S"][i])
                    maxj = self.N
                    if maxSearch != None:
                        maxj = min(self.N,i+1+maxSearch)
                    for j in xrange(i+1, maxj):
                        name2 = stripQuotes(self.data["NAME"][j])
                        ns2 = name2.split("..")
                        if len(ns2)==2:
                            if ns2[0] == ns1[0]:
                                #print "\t sub", ns2[0],j
                                idx += 1
                                assert idx == int(ns2[1])
                                sMax = float(self.data["S"][j])
                    self.elements[ns1[0]] = (sMin,sMax)
