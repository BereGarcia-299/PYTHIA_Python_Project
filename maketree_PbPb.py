# Copyright (C) 2020 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.

# This program, simulates Pb+Pb events and write it into a root file.

import sys
cfg = open("Makefile.inc")
lib = "../lib"
for line in cfg:
    if line.startswith("PREFIX_LIB="): lib = line[11:-1]; break
sys.path.insert(0, lib)

#following https://wiki.physik.uzh.ch/cms/root:pyroot_ttree
#IMPORT root
from ROOT import TFile, TTree
from array import array

# Creating root file to save events
inFile = TFile("tree.root", 'recreate')
inTree = TTree("tree_name", "tree title")

# Branches of the Tree
mult= array('i',[0])
nJets= array('i',[0])
nPhotons= array('i',[0])
bigSize=10000
pTVar = array('d',[0])
phiVar = array('d',[0])
yVar = array('d',[0])
mVar = array('d',[0])
pxVar = array('d',[0])
pyVar = array('d',[0])
pzVar = array('d',[0])
eVar = array('d',[0])
pTPho = array('d',[0])
etaPho = array('d',[0])
phiPho = array('d',[0])

for i in range(0,bigSize):
    pTVar.append(0)
    phiVar.append(0)
    yVar.append(0)
    mVar.append(0)
    pxVar.append(0)
    pyVar.append(0)
    pzVar.append(0)
    eVar.append(0)
    pTPho.append(0)
    etaPho.append(0)
    phiPho.append(0)

inTree.Branch("mult",  mult,  'mult/I')
inTree.Branch("nJets",  nJets,  'nJets/I')
inTree.Branch("nPhotons",  nPhotons,  'nPhotons/I')
inTree.Branch("pTJets",  pTVar,  'pTJets[nJets]/D')
inTree.Branch("phiJets",  phiVar,  'phiJets[nJets]/D')
inTree.Branch("yJets",  yVar,  'yJets[nJets]/D')
inTree.Branch("mJets",  mVar,  'mJets[nJets]/D')
inTree.Branch("pxJets",  pxVar,  'pxJets[nJets]/D')
inTree.Branch("pyJets",  pyVar,  'pyJets[nJets]/D')
inTree.Branch("pzJets",  pzVar,  'pzJets[nJets]/D')
inTree.Branch("eJets",  eVar,  'eJets[nJets]/D')
inTree.Branch("pTPhotons",  pTPho,  'pTPhotons[nPhotons]/D')
inTree.Branch("etaPhotons",  etaPho,  'etaPhotons[nPhotons]/D')
inTree.Branch("phiPhotons",  phiPho,  'phiPhotons[nPhotons]/D')

# Import the Pythia module.
import pythia8
pythia = pythia8.Pythia()

#Setup the beams.
pythia.readString("Beams:idA = 1000822080");
pythia.readString("Beams:idB = 1000822080"); #The lead ions.
pythia.readString("Beams:eCM = 2760.0"); #Collision energy at 2.76 TeV
pythia.readString("HardQCD:all = off")
pythia.readString("PromptPhoton:all  = on")
pythia.readString("Beams:frameType = 1");

#Initialize the Angantyr model to fit the total and semi-includive
#cross sections in Pythia within some tolerance.
pythia.readString("HeavyIon:SigFitErr = "
                    "0.02,0.02,0.1,0.05,0.05,0.0,0.1,0.0");
#These parameters are typicall suitable for sqrt(S_NN)=5TeV
pythia.readString("HeavyIon:SigFitDefPar = "
                    "17.24,2.15,0.33,0.0,0.0,0.0,0.0,0.0");
#A simple genetic algorithm is run for 20 generations to fit the parameters.
pythia.readString("HeavyIon:SigFitNGen = 20");
pythia.init()

# SlowJet is a class that creates Jets with (-1, R, pTmin, etaMax); R is the jet radii cone. We are looking at R=1.0 and R=0.4.
slowJet = pythia8.SlowJet(-1, 1.0, 5., 5)

# Begin event loop. Generate event. Skip if error. List first one.
# Generating 5000 events
for iEvent in range(0, 5000):
    print(iEvent)
    if not pythia.next(): continue
    mult[0] = 0
    mult_cut = 0
    for prt in pythia.event:
        if(prt.isFinal() and prt.isCharged() and abs(prt.eta()) < 2.5 and prt.pT() > 0.5):
            mult[0] += 1
            mult_cut += 1

    nJets[0] = 0
    slowJet.analyze( pythia.event );
    nSlow = slowJet.sizeJet();
    
    # Looping over Jets
    for iJet in range(nSlow):
        pTVar[nJets[0]] = slowJet.pT(iJet);
        phiVar[nJets[0]] = slowJet.phi(iJet);
        yVar[nJets[0]] = slowJet.y(iJet);
        mVar[nJets[0]] = slowJet.m(iJet);
        pxVar[nJets[0]] = slowJet.p(iJet).px();
        pyVar[nJets[0]] = slowJet.p(iJet).py();
        pzVar[nJets[0]] = slowJet.p(iJet).pz();
        eVar[nJets[0]] = slowJet.p(iJet).e();
        nJets[0] += 1
   
    #Looping over Photons
    nPhotons[0]=0
    for prt in pythia.event:
        if (prt.idAbs() == 22):
            if (prt.pT() >= 5):
                if (prt.pT() >= 50):
                    print(prt.pT())
                pTPho[nPhotons[0]] = prt.pT();
                etaPho[nPhotons[0]] = prt.eta();
                phiPho[nPhotons[0]] = prt.phi();
                nPhotons[0] +=1
    # Filling TTree
    inTree.Fill()
   
# End of event loop. Statistics. Done.
pythia.stat();
inFile.Write("", TFile.kOverwrite)
inFile.Close()
