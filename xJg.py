#Analysis code
#Takes events from input file, constructs desirable quantities, saves it to output root file
#To be run as python xJg.py root_files/tree_pp_R1.root plots/hist_pp_R1.root #for pp with R=1.0 jets
#To be run as python xJg.py root_files/ttree_pp_R4.root plots/hist_pp_R4.root #for pp with R=0.4 jets
#To be run as python xJg.py root_files/ttree_PbPb_R1.root plots/hist_PbPb_R1.root #for PbPb with R=1.0 jets
#To be run as python xJg.py root_files/ttree_PbPb_R4.root plots/hist_PbPb_R4.root #for PbPb with R=0.4 jets

import ROOT
from ROOT import TFile, TTree
import numpy as np
import  sys
if len(sys.argv) != 3:
    print("USAGE: %s <input  file > <output  file >")%(sys.argv [0])
    sys.exit (1)

inFileName = sys.argv [1]
outFileName = sys.argv [2]
print("Reading  from", inFileName , "and  writing  to", outFileName)

inFile = ROOT.TFile.Open(inFileName ,"READ")
tree = inFile.Get("tree_name")

#canvas = ROOT.TCanvas("canvas")
#canvas.cd()

#Construct 1D histogram for eta, pT and phi distributions for jets.
h_pt = ROOT.TH1D("h_pt","pT", 500, 0, 800);
h_phi = ROOT.TH1D("h_phi","#phi", 500, -1*np.pi, np.pi);
h_y = ROOT.TH1D("h_y","#y", 500, -5.6, 5.6);

#Construct 1D histogram for eta, pT and phi distributions for photons.
h_photon_pt = ROOT.TH1D("h_photon_pt","pT", 100, 0, 500);
h_photon_phi = ROOT.TH1D("h_photon_phi","#phi", 64, -1*np.pi, np.pi);
h_photon_eta = ROOT.TH1D("h_photon_eta","#eta", 100, -5.6, 5.6);

#Construct 1D histogram for xJg distributions for jets with photons of different pT ranges.
h_xJg_50_70 = ROOT.TH1D("h_xJg_50_70","", 500, 0, 5);
h_xJg_70_100 = ROOT.TH1D("h_xJg_70_100","", 500, 0, 5);
h_xJg_100_150 = ROOT.TH1D("h_xJg_100_150","", 500, 0, 5);
h_xJg_150 = ROOT.TH1D("h_xJg_150","", 500, 0, 5);
h_xJg_50 = ROOT.TH1D("h_xJg_50","", 500, 0, 5);

#Construct 2D histogram for photon pT vs leading Jet pT for jets
h_photonpt_highjetpt = ROOT.TH2D("h_photonpt_highjetpt","", 500, 0, 200, 500, 0, 200);
h_photonpt_dphi = ROOT.TH2D("h_photonpt_dphi","", 500, 0, 200, 500, -1*np.pi, np.pi);

N = tree.GetEntries()

for iEntry in range(0,N):
    tree.GetEntry(iEntry)

    #Jets Kinematics
    nJets = getattr(tree,"nJets")
    pTJets = getattr(tree,"pTJets")
    phiJets = getattr(tree,"phiJets")
    yJets = getattr(tree,"yJets")
    mJets = getattr(tree,"mJets")
    pxJets = getattr(tree,"pxJets")
    pyJets = getattr(tree,"pyJets")
    pzJets = getattr(tree,"pzJets")

    for iJet in range(0,nJets):
        h_pt.Fill(pTJets[iJet])
        h_phi.Fill(phiJets[iJet])
        h_y.Fill(yJets[iJet])

    #Photons Kinematics
    nPhotons = getattr(tree,"nPhotons")
    pTPhotons = getattr(tree,"pTPhotons")
    etaPhotons = getattr(tree,"etaPhotons")
    phiPhotons = getattr(tree,"phiPhotons")

    for iPhoton in range(0,nPhotons):
        h_photon_pt.Fill(pTPhotons[iPhoton])
        h_photon_phi.Fill(phiPhotons[iPhoton])
        h_photon_eta.Fill(etaPhotons[iPhoton])

        highjet = 0;
        highjetphi = 0;
        highjetdphi = 0;
        for jJet in range(0,nJets):
            if (pTJets[jJet] > highjet): 
                highjet = pTJets[jJet]
                highjetphi = phiJets[jJet]
                highjetdphi = phiPhotons[iPhoton] - phiJets[jJet]
                while (highjetdphi > np.pi): 
                    highjetdphi -= 2*np.pi
                while (highjetdphi < -1*np.pi): 
                    highjetdphi += 2*np.pi
        

        if np.abs(highjetdphi) <= np.pi/2.: continue
        if (highjet == 0 or highjetphi == 0 or highjetdphi == 0): continue
        print(highjet," ",highjetphi," ",highjetdphi)
        xJg = highjet/pTPhotons[iPhoton]
        h_photonpt_highjetpt.Fill(pTPhotons[iPhoton], highjet)
        h_photonpt_dphi.Fill(pTPhotons[iPhoton], highjetdphi)
        if (pTPhotons[iPhoton] > 50 and pTPhotons[iPhoton] < 70):
            h_xJg_50_70.Fill(xJg)
        if (pTPhotons[iPhoton] > 70 and pTPhotons[iPhoton] < 100):
            h_xJg_70_100.Fill(xJg)
        if (pTPhotons[iPhoton] > 100 and pTPhotons[iPhoton] < 150):
            h_xJg_100_150.Fill(xJg)
        if (pTPhotons[iPhoton] > 150):
            h_xJg_150.Fill(xJg)
        if (pTPhotons[iPhoton] < 50):
            h_xJg_50.Fill(xJg)


h_pt.SetDirectory(0)
h_phi.SetDirectory(0)
h_y.SetDirectory(0)

h_photon_pt.SetDirectory(0)
h_photon_phi.SetDirectory(0)
h_photon_eta.SetDirectory(0)

h_xJg_50_70.SetDirectory(0)
h_xJg_70_100.SetDirectory(0)
h_xJg_100_150.SetDirectory(0)
h_xJg_150.SetDirectory(0)
h_xJg_50.SetDirectory(0)
h_photonpt_highjetpt.SetDirectory(0)
h_photonpt_dphi.SetDirectory(0)


inFile.Close()

outHistFile = ROOT.TFile.Open(outFileName ,"RECREATE")
outHistFile.cd() 

h_pt.Write()
h_phi.Write()
h_y.Write()
h_photon_pt.Write()
h_photon_phi.Write()
h_photon_eta.Write()
h_xJg_50_70.Write()
h_xJg_70_100.Write()
h_xJg_100_150.Write()
h_xJg_150.Write()
h_xJg_50.Write()
h_photonpt_highjetpt.Write()
h_photonpt_dphi.Write()


outHistFile.Close()


