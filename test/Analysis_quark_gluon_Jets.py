<<<<<<< HEAD
# main01.py is a part of the PYTHIA event generator.
# Copyright (C) 2020 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.

# Keywords: basic usage; charged multiplicity; python;

# This is a simple test program. It fits on one slide in a talk.  It
# studies the charged multiplicity distribution at the LHC. To set the
# path to the Pythia 8 Python interface do either (in a shell prompt):
#      export PYTHONPATH=$(PREFIX_LIB):$PYTHONPAT
=======
#This is where we test our Analysis code

>>>>>>> ac509c7b9c6eca54579df9a02be94556eefbd1a8

import sys

import math 

cfg = open("Makefile.inc")
lib = "../lib"
for line in cfg:
    if line.startswith("PREFIX_LIB="): lib = line[11:-1]; break
sys.path.insert(0, lib)

#following https://wiki.physik.uzh.ch/cms/root:pyroot_ttree
#IMPORT root
from ROOT import TFile, TTree
from array import array

inFile = TFile("tree.root", 'recreate')
inTree = TTree("tree_name", "tree title")

nPart= array('i',[0])
bigSize=10000000
pxVar = array('d',[0])
pyVar = array('d',[0])
pzVar = array('d',[0])
eVar = array('d',[0])
mVar = array('d',[0])
idVar = array('i',[0])

nJets = array('i',[0])
jets_phi = array('f',[0])
jets_pT =array('f',[0])
jets_m =array('f',[0])
jets_eta=array('f',[0])	
jets_px=array('f',[0])
jets_py=array('f',[0])
jets_pz=array('f',[0])
jets_e=array('f',[0])

nGamma = array('i',[0])
gamma_pT=array('d',[0])
gamma_phi=array('d',[0])
gamma_eta=array('d',[0])

nGluonJets = array('i',[0])
gluon_jets_pT = array('f',[0])
gluon_jets_phi = array('f',[0])
gluon_jets_eta = array('f',[0])

nQuarkJets = array('i',[0])
quark_jets_pT = array('f',[0])
quark_jets_phi = array('f',[0])
quark_jets_eta = array('f',[0])

keep_jet_indicies = array('i',[0])

for i in range(0,bigSize):
    pxVar.append(0)
    pyVar.append(0)
    pzVar.append(0)
    eVar.append(0)
    mVar.append(0)
    idVar.append(0)
    jets_phi.append(0)
    jets_pT.append(0)
    jets_m.append(0)
    jets_eta.append(0)
    jets_px.append(0)
    jets_py.append(0)
    jets_pz.append(0)
    jets_e.append(0)
    gamma_pT.append(0)
    gamma_phi.append(0)
    gamma_eta.append(0)	
    gluon_jets_pT.append(0)
    gluon_jets_phi.append(0)
    gluon_jets_eta.append(0)	
    quark_jets_pT.append(0)
    quark_jets_phi.append(0)
    quark_jets_eta.append(0)


for i in range(0,90):
    keep_jet_indicies.append(-1)


inTree.Branch("nPart",  nPart,  'nPart/I')
inTree.Branch("px",  pxVar,  'px[nPart]/D')
inTree.Branch("py",  pyVar,  'py[nPart]/D')
inTree.Branch("pz",  pzVar,  'pz[nPart]/D')
inTree.Branch("e",  eVar,  'e[nPart]/D')
inTree.Branch("m",  mVar,  'm[nPart]/D')
inTree.Branch("id",  idVar,  'id[nPart]/I')
inTree.Branch("nJets", nJets, 'nJets/I')
inTree.Branch("jets_phi",jets_phi,'jets_phi[nJets]/F')
inTree.Branch("jets_pT",jets_pT,'jets_pT[nJets]/F')
inTree.Branch("jets_m",jets_m,'jets_m[nJets]/F')
inTree.Branch("jets_eta",jets_eta,'jets_eta[nJets]/F')
inTree.Branch("jets_px",jets_px,'jets_px[nJets]/F')
inTree.Branch("jets_py",jets_py,'jets_py[nJets]/F')
inTree.Branch("jets_pz",jets_pz,'jets_pz[nJets]/F')
inTree.Branch("jets_e",jets_e,'jets_e[nJets]/F')

inTree.Branch("nGamma",nGamma,'nGamma/I')
inTree.Branch("gamma_pT",gamma_pT,'gamma_pT[nGamma]/F')
inTree.Branch("gamma_phi",gamma_phi,'gamma_phi[nGamma]/F')
inTree.Branch("gamma_eta",gamma_eta,'gamma_eta[nGamma]/F')

inTree.Branch("nGluonJets",nGluonJets,'nGluonJets/I')
inTree.Branch("gluon_jets_pT",gluon_jets_pT,'gluon_jets_pT[nGluonJets]/F')
inTree.Branch("gluon_jets_eta",gluon_jets_eta,'gluon_jets_eta[nGluonJets]/F')
inTree.Branch("gluon_jets_phi",gluon_jets_phi,'gluon_jets_phi[nGluonJets]/F')


inTree.Branch("nQuarkJets",nQuarkJets,'nQuarkJets/I')
inTree.Branch("quark_jets_pT",quark_jets_pT,'quark_jets_pT[nQuarkJets]/F')
inTree.Branch("quark_jets_eta",quark_jets_eta,'quark_jets_eta[nQuarkJets]/F')
inTree.Branch("quark_jets_phi",quark_jets_phi,'quark_jets_phi[nQuarkJets]/F')

# Import the Pythia module.
import pythia8
pythia = pythia8.Pythia()

#Initialize the Angantyr model to fit the total and semi-includive
#cross sections in Pythia within some tolerance.
pythia.readString("HeavyIon:SigFitErr = "
                    "0.02,0.02,0.1,0.05,0.05,0.0,0.1,0.0");
#These parameters are typicall suitable for sqrt(S_NN)=5TeV
pythia.readString("HeavyIon:SigFitDefPar = "
                    "17.24,2.15,0.33,0.0,0.0,0.0,0.0,0.0");
#A simple genetic algorithm is run for 20 generations to fit the parameters.
pythia.readString("HeavyIon:SigFitNGen = 20");


pythia.readString("HardQCD:all = off")
pythia.readString("PromptPhoton:all = on")
pythia.init()
mult = pythia8.Hist("charged multiplicity", 100, -0.5, 799.5)
# Begin event loop. Generate event. Skip if error. List first one.

for iEvent in range(0, 30):
    if not pythia.next(): continue
    # Find number of all final charged particles and fill histogram.
    nCharged = 0
    nPart[0]=0
    nJets[0]=0
    nGamma[0]=0	 
    nQuarkJets[0]=0
    nGluonJets[0] = 0	     
    nJets[0] = 0	
   
    #Setting Up The Jet Class
    jets = pythia8.SlowJet(-1, 1.0, 10., 5)
    jets.analyze(pythia.event)
    numJets = jets.sizeJet() 

    #Test:
    #Uncomment the print of lines if you wish to run tets

    #print("Event Number: ")
    #print(iEvent)    
    #print("This is the number of jets in this events: ")
    #print(numJets)

    for iJets in range(0,numJets):
    	 #Running Over Jets In Events 
	 count_gluons_inJet_5 = 0
    	 count_quarks_inJet_5 = 0
    	 count_quarks_inJet_6 = 0
    	 count_gluons_inJet_6 = 0
    	 pos = 0
    	 passed_5 = False
    	 passed_6 = False
    	 for prt in pythia.event:
    	 	#Looping Over All Particles
	 	if((prt.idAbs()==22) and (prt.pT()>3) and (prt.pT()<800)):
			#If Particle Made  It Here It Means It Is A Photon
			# With a pT > 3 GeV and < 800 GeV
			
			#print("Collected a gamma!")
			#print("pT: ")
			#print(prt.pT())
			#print("Eta value of gamma: ")
			#print(prt.y())
			#print("Phi value of gamma: ")
			#print("prt.phi()")
	
        		#Collecting Photons Kinematic Information
			gamma_pT[nGamma[0]]=prt.pT()
        		gamma_eta[nGamma[0]]=prt.y()
        		gamma_phi[nGamma[0]]=prt.phi()
        		nGamma[0]+=1    	 	
		
  		#The pTHat Value Give The pT Of The Particles In The Events 
		pTHat_val = pythia.infoPython().pTHat()

    	 	
    	 	if((pos == 1) or (pos==2)):
    	 		#Here we are checking the particke position (initial state and final state)
    	 		parton_mom = prt.idAbs()
			
    	    
		if((pos==5) and (parton_mom ==2212)):
			#We will save the final state of the parton
			#(These can potentially be quarks or gluons)
		  	part5_iD = prt.idAbs()
			part5_pT = prt.pT()
		  	part5_pz = prt.pz()
		  	part5_py = prt.py()
		  	part5_px = prt.px()
		  	part5_eta = prt.y()
		  	part5_phi = prt.phi()
		  	passed_5 = True
			
		if((pos == 6) and (parton_mom==2212)):
			#We will save the final state of the parton
			#(These can potentially be quarks or gluons)
		 	part6_iD = prt.idAbs()
			part6_pT = prt.pT()
		  	part6_pz = prt.pz()
		  	part6_py = prt.py()
		  	part6_px = prt.px()
		  	part6_eta = prt.y()
		  	part6_phi = prt.phi()
		  	passed_6 = True
		  	
		if(passed_5 and passed_6):
		  #It made sure to grab the particle information after the hard scattering
		  #Between two partons
		  sum_px = part5_px + part6_px
		  sum_py = part5_py + part6_py
		  #We summed the px and py values to check that they came from the same
	          #HardScattering. IF they did, they px's and py's will add to zero
	
		  if((sum_py == 0) and (sum_py==0)):
		  	#print("sum of pys and pxs is: ")
			#print(sum_py)
			#print(sum_px)
			if((pTHat_val == part6_pT) and (pTHat_val == part5_pT)):
				#In the line of code from above we are checking that the pTHat value matches 
				#The pT of the particle will match to the pTHat if it comes from a Hardscattering event	  		
	
				#We are now matching jets to gluons
		  		
		  		
		  		deltaEta_5J = jets.y(iJets) - part5_eta
				deltaEta_6J = jets.y(iJets) - part6_eta
				
				deltaPhi_5J = jets.phi(iJets) - part5_phi 
				deltaPhi_6J = jets.phi(iJets) - part6_phi

				deltaR_5J = (deltaEta_5J**2 + deltaPhi_5J**2)**(0.5)
				deltaR_6J = (deltaPhi_6J**2 + deltaPhi_6J**2)**(0.5)
				
				#We calculate the distance between the particle and jet (deltaR)
				#Its within our jet if deltaR < 0.3 (ofcourse this can vary but this is the cut we chose)
				if((part5_iD == 21) and (deltaR_5J<0.3) and (part5_pT > 10)):
					if(jets.pT(iJets)>20):
					#Requiring Jet to have a pT > 20 GeV
						count_gluons_inJet_5 +=1
						#Counting the number of gluons in my jet
     		                if((part6_iD == 21) and (deltaR_6J<0.3) and (part6_pT > 10)):
					if(jets.pT(iJets)>20):
						count_gluons_inJet_6 +=1

				if((part6_iD == 2) and (deltaR_6J<0.3) and (part6_pT > 10)):
					if(jets.pT(iJets)>20):
						count_quarks_inJet_6 += 1
				if((part5_iD == 2) and (deltaR_5J<0.3) and (part5_pT >10)):
					if(jets.pT(iJets)>20):
						count_quarks_inJet_5 += 1
  	
        	pos += 1			
			
	 if ((count_gluons_inJet_5 > 400) or (count_gluons_inJet_6 > 400)):
	     #print("this is how many gluons are in our jet: ")
	     #print(count_gluons_inJet_5)
	     #print(count_gluons_inJet_6)
	     #If there are more than 400 gluons in my jet record it as gluon-jet	
	     gluon_jets_pT[nGluonJets[0]] = jets.pT(iJets);
	     gluon_jets_phi[nGluonJets[0]] =jets.phi(iJets);
	     gluon_jets_eta[nGluonJets[0]] = jets.y(iJets);
	     nGluonJets[0] += 1
	   
	 if((count_quarks_inJet_5 > 300) or (count_quarks_inJet_6>300)):
	     #print("this is how many quarks are in our jet: ")
	     #print(count_quarks_inJet_5)
	     #print(count_quarks_inJet_6)
	     #If there are more than 300 quarks in my jet record it as a quark-jet
	     quark_jets_pT[nQuarkJets[0]] = jets.pT(iJets);
	     quark_jets_phi[nQuarkJets[0]] = jets.phi(iJets);
	     quark_jets_eta[nQuarkJets[0]] = jets.y(iJets);
	     nQuarkJets[0] += 1	
	
	
    #Filling my tree
    inTree.Fill()
    mult.fill(nCharged)
# End of event loop. Statistics. Histogram. Done.
pythia.stat();
print(mult)


inFile.Write("", TFile.kOverwrite)
inFile.Close()






















