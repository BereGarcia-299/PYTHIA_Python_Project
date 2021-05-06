import ROOT
from ROOT import TFile, TTree
import numpy as np
import sys

if len(sys.argv) != 2:
    print("USAGE: %s <input  file >")%(sys.argv [0])
    sys.exit (1)
histFile = sys.argv [1]
inFile = ROOT.TFile.Open(histFile ,"READ")

h_pt = inFile.Get("h_pt")
h_phi = inFile.Get("h_phi")
h_y = inFile.Get("h_y")

h_photon_pt = inFile.Get("h_photon_pt")
h_photon_phi = inFile.Get("h_photon_phi")
h_photon_eta = inFile.Get("h_photon_eta")

h_xJg_50 = inFile.Get("h_xJg_50")

h_photonpt_highjetpt = inFile.Get("h_photonpt_highjetpt")
h_photonpt_dphi = inFile.Get("h_photonpt_dphi")
    
h_xJg_50.Scale(1.0/h_xJg_50.Integral());

h_pt.GetXaxis().SetTitle("Jet_pT");
h_pt.GetYaxis().SetTitle("# entries");
h_pt.GetXaxis().SetRange(0,100);
c1 = ROOT.TCanvas("c1")
h_pt.Draw()
c1.Print("h_pt.pdf")

h_y.GetXaxis().SetTitle("Jet_eta");
h_y.GetYaxis().SetTitle("# entries");
c2 = ROOT.TCanvas("c2")
h_y.Draw()
c2.Print("h_y.pdf")

h_phi.GetXaxis().SetTitle("Jet_phi");
h_phi.GetYaxis().SetTitle("# entries");
h_phi.SetMinimum(0);
c3 = ROOT.TCanvas("c3")
h_phi.Draw()
c3.Print("h_phi.pdf")

h_photon_pt.GetXaxis().SetTitle("Photon_pT");
h_photon_pt.GetYaxis().SetTitle("# entries");
h_photon_pt.GetXaxis().SetRange(0,50);
c4 = ROOT.TCanvas("c4")
h_photon_pt.Draw()
c4.Print("h_photon_pt.pdf")

h_photon_eta.GetXaxis().SetTitle("Photon_eta");
h_photon_eta.GetYaxis().SetTitle("# entries");
c5 = ROOT.TCanvas("c5")
h_photon_eta.Draw()
c5.Print("h_photon_eta.pdf")

h_photon_phi.GetXaxis().SetTitle("Photon_phi");
h_photon_phi.GetYaxis().SetTitle("# entries");
h_photon_phi.SetMinimum(0);
c6 = ROOT.TCanvas("c6")
h_photon_phi.Draw()
c6.Print("h_photon_phi.pdf")

h_xJg_50.GetXaxis().SetTitle("xJGamma (pT(photons) < 50 GeV)");
h_xJg_50.GetYaxis().SetTitle("# entries");
c7 = ROOT.TCanvas("c7")
h_xJg_50.Draw("COLZ")
c7.Print("h_xJg_50.pdf")

h_photonpt_highjetpt.GetXaxis().SetTitle("Photon pT");
h_photonpt_highjetpt.GetYaxis().SetTitle("Leading Jet pT");
c11 = ROOT.TCanvas("c11")
h_photonpt_highjetpt.Draw("COLZ")
c11.Print("h_photonpt_highjetpt.pdf")

h_photonpt_dphi.GetXaxis().SetTitle("Photon pT");
h_photonpt_dphi.GetYaxis().SetTitle("Delta Phi between photons and leading jet");
c12 = ROOT.TCanvas("c12")
h_photonpt_dphi.Draw("COLZ")
c12.Print("h_photonpt_dphi.pdf")



'''

    TCanvas* c1 = new TCanvas("c1","New Canvas",50,50,700,600);
    TPad* thePad = (TPad*)c1->cd();
    TH1F *h_frame = thePad->DrawFrame(0,0,4.0,0.15);
    //h_frame->GetYaxis()->SetTitle("#it{v}_{2,2}");
    //h_frame->GetYaxis()->SetTitleOffset(1.7);
    h_frame->GetXaxis()->SetTitle("xJg for Jets with R=1.0");
    h_frame->GetYaxis()->SetNdivisions(506,kTRUE);
    h_frame->GetXaxis()->SetNdivisions(509,kTRUE);
    h_frame->Draw("AXIS");

    h_xJg_R1_50_70->SetLineColor(1);
    h_xJg_R1_70_100->SetLineColor(4);
    h_xJg_R1_100_150->SetLineColor(2);
    h_xJg_R1_150->SetLineColor(6);
    
    
    h_xJg_R1_150->Draw("hist same");
    h_xJg_R1_100_150->Draw("hist same");
    h_xJg_R1_50_70->Draw("hist same");
    h_xJg_R1_70_100->Draw("hist same");
    auto legend = new TLegend(0.1,0.7,0.48,0.9);
    legend->SetBorderSize(0);
    legend->SetTextSize(0.04);
    legend->SetTextFont(42);
    legend->AddEntry("h_xJg_R1_50_70","photon pT: [50,70] GeV","l");
    legend->AddEntry("h_xJg_R1_70_100","photon pT: [70,100] GeV","l");
    legend->AddEntry("h_xJg_R1_100_150","photon pT: [100,150] GeV","l");
    legend->AddEntry("h_xJg_R1_150","photon pT > 150 GeV","l");
    legend->Draw();
    //myMarkerLineText(0.6,0.85, 1.2, 1, 21, 1, 1, "h_xJg_R1_50_70", 0.04, true);
    //myMarkerLineText(0.6,0.80, 1.2, 4, 21, 4, 1, "h_xJg_R1_70_100", 0.04, true);
    //myMarkerLineText(0.6,0.75, 1.2, 2, 21, 2, 1, "h_xJg_R1_100_150", 0.04, true);
    //myMarkerLineText(0.6,0.70, 1.2, 6, 21, 6, 1, "h_xJg_R1_150", 0.04, true);


'''
