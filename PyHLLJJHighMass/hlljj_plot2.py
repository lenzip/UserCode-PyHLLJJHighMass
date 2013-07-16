#!/usr/bin/env python
import os,string,sys,commands,time,ConfigParser
from ROOT import *
from CMGTools.RootTools.utils.DeltaR import deltaR
from array import array
import numpy
import urllib2
import getopt
from optparse import OptionParser, Option
from systematics import *
from fit import *
import math

#sources of xsection info
xsecgg="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-ggH.txt?revision=1.4&view=markup"
xsecvbf="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-vbfH.txt?revision=1.7&view=markup"
effvbf="http://lenzip.web.cern.ch/lenzip/H2l2q/Efficiencies/effVBF.txt"
effgg="http://lenzip.web.cern.ch/lenzip/H2l2q/Efficiencies/effGG.txt"
mvatraining="/afs/cern.ch/work/v/vagori/public/MVA_weights/"

#default selection
def_condition = " and (event.J1Pt > 30 and event.J2Pt > 30. and event.VBFJ1Pt > 50. and event.VBFJ2Pt > 30.)"
def_condition += " and ((event.M1Pt > 40 and event.M2Pt > 20.) or (event.E1Pt > 40 and event.E2Pt > 20.))"
def_condition += " and ((event.ZEEMass > 76. and event.ZEEMass < 106.) or (event.ZMMMass > 76. and event.ZMMMass < 106.))"
#def_condition += " and ((event.ZEEMass > 50.) or (event.ZMMMass > 50.))"
def_condition += " and (event.ZJJMass > 71. and event.ZJJMass < 111.)"
#def_condition += " and (event.ZJJMass > 50. )"
def_condition += " and max(event.HEEJJmassVBF, event.HMMJJmassVBF)> 400"
def_condition += " and max(event.HEEJJdetaVBF, event.HMMJJdetaVBF)> 4"
def_condition += " and event.ZJJPt > 80."
def_condition += " and (abs(event.HEEJJcosthetastar) < 0.8 or abs(event.HMMJJcosthetastar) < 0.8)"
#def_condition += " and max(event.HEEJJMass, event.HMMJJMass)>564 and max(event.HEEJJMass, event.HMMJJMass) < 660"

#default list of plots
def_plot=True
h1_list=[
    ["ZJJMass" ,"event.ZJJMass" ,100,0,200,def_plot, "", "", "Mass J1J2 [GeV]", ""],
    ["J1Pt" ,"event.J1Pt" ,100,0,200,def_plot, "", "", "pT J1 [GeV]", ""],
    ["J2Pt" ,"event.J2Pt" ,100,0,200,def_plot, "", "", "pT J2 [GeV]", ""],
    ["J1Eta" ,"event.J1Eta" ,100,-5,5,def_plot, "", "", "#eta J1", ""],
    ["J2Eta" ,"event.J2Eta" ,100,-5,5,def_plot, "", "", "#eta J2", ""],
    ["VBFJ1Pt" ,"event.VBFJ1Pt" ,100,0,200,def_plot, "", "", "pT VBF J1 [GeV]", ""],
    ["VBFJ2Pt" ,"event.VBFJ2Pt" ,100,0,200,def_plot, "", "", "pT VBF J2 [GeV]", ""],
    ["VBFJ1Eta" ,"event.VBFJ1Eta" ,100,-5,5,def_plot, "", "", "#eta VBF J1", ""],
    ["VBFJ2Eta" ,"event.VBFJ2Eta" ,100,-5,5,def_plot, "", "", "#eta VBF J2", ""],
    ["ZEEMass" ,"event.ZEEMass" ,100,0,200,def_plot, "", "", "Mass e+e- [GeV]", ""],
    ["ZMMMass" ,"event.ZMMMass" ,100,0,200,def_plot, "", "", "Mass #mu+#mu- [GeV]", ""],
    ["HMMJJMass" ,"event.HMMJJMass" ,200,0,2000,def_plot, "", "", "Mass H(#mu+#mu-jj)[GeV]", ""],
    ["HEEJJMass" ,"event.HEEJJMass" ,200,0,2000,def_plot, "", "", "Mass (e+e-ll)[GeV]", ""],
    ["HEEJJmassVBF" ,"event.HEEJJmassVBF" ,100,0,2000,def_plot, "", "", "Mass VBF pair for H(e+e-jj) [GeV]", ""],
    ["HMMJJmassVBF" ,"event.HMMJJmassVBF" ,100,0,2000,def_plot, "", "", "Mass VBF pair for H(#mu+#mu-jj) [GeV]", ""],
    ["HMMJJdetaVBF" ,"event.HMMJJdetaVBF" ,40,0,10,def_plot, "", "", "#Delta#eta VBF pair for H(#mu+#mu-jj) [GeV]", ""],
    ["HEEJJdetaVBF" ,"event.HEEJJdetaVBF" ,40,0,10,def_plot, "", "", "#Delta#eta VBF pair for H(e+e-jj) [GeV]", ""],
    ["HMMJJDeltaPhiZ" ,"abs(event.HMMJJDeltaPhiZ)" ,40,0,4,def_plot, "", "", "#Delta#phi Z(#mu+#mu-)Z(jj)", ""],
    ["HEEJJDeltaPhiZ" ,"abs(event.HEEJJDeltaPhiZ)" ,40,0,4,def_plot, "", "", "#Delta#phi Z(e+e-)Z(jj)", ""],
    ["HMMJJDeltaPhiZJ1" ,"abs(event.HMMJJDeltaPhiZJ1)" ,40,0,4,def_plot, "", "", "#Delta#phiZ(#mu+#mu-)J1", ""],
    ["HEEJJDeltaPhiZJ1" ,"abs(event.HEEJJDeltaPhiZJ1)" ,40,0,4,def_plot, "", "", "#Delta#phiZ(e+e-)J1", ""],
    ["HMMJJhelcosthetaZl1" ,"event.HMMJJhelcosthetaZl1" ,30,-1.5,1.5,def_plot, "", "", "helcosthetaZl1 H(#mu+#mu-jj)", ""],
    ["HMMJJhelcosthetaZl2" ,"event.HMMJJhelcosthetaZl2" ,20,-0.5,1.5, def_plot, "", "", "helcosthetaZl2 H(#mu+#mu-jj)", ""],
    ["HEEJJhelcosthetaZl1" ,"event.HEEJJhelcosthetaZl1" ,30,-1.5,1.5,def_plot, "", "", "helcosthetaZl1 H(e+e-jj)", ""],
    ["HEEJJhelcosthetaZl2" ,"event.HEEJJhelcosthetaZl2" ,20,-0.5,1.5, def_plot, "", "", "helcosthetaZl2 H(e+e-jj)", ""],
    ["HEEJJcosthetastar" ,"event.HEEJJcosthetastar" ,20,-1.1,1.1, def_plot, "", "", "costhetastar H(e+e-jj)", ""],
    ["HMMJJcosthetastar" ,"event.HMMJJcosthetastar" ,20,-1.1,1.1, def_plot, "", "", "costhetastar H(e+e-jj)", ""],
    ["HMMJJSumAbsEtaJ1J2" ,"event.HMMJJSumAbsEtaJ1J2" ,20,0,5., def_plot, "", "|#eta(J1)|+|#eta(J2)|, H(e+e-jj)", "", ""],
    ["HEEJJSumAbsEtaJ1J2" ,"event.HEEJJSumAbsEtaJ1J2" ,20,0,5., def_plot, "", "|#eta(J1)|+|#eta(J2)|, H(#mu+#mu-jj)", "", ""],
#    ["HEEJJClassifier" ,"event.HEEJJClassifier" ,50,-0.8, 0.2, def_plot, "", "", "BDT classifier, H(e+e-jj)", ""],
#    ["HMMJJClassifier" ,"event.HMMJJClassifier", 50,-0.8, 0.2, def_plot, "", "", "BDT classifier, H(#mu+#mu-jj)", ""],
#    ["ZJJDeltaEtaDecay" ,"abs(event.J1Eta-event.J2Eta)", 50, 0 , 5, def_plot, "", "", "ZJJdeltaEtaDecay", ""],
    ["ZJJDeltaRDecay" ,"abs(deltaR(event.J1Eta, event.J1Phi, event.J2Eta, event.J2Phi))", 50, 0 , 5, def_plot, "", "", "ZJJdeltaRDecay", ""],
    ["HMMJJhelphi" ,"event.HMMJJhelphi", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphi", ""],
    ["HEEJJhelphi" ,"event.HEEJJhelphi", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphi", ""],
    ["HMMJJhelphiZl1" ,"event.HMMJJhelphiZl1", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphiZl1", ""],
    ["HEEJJhelphiZl1" ,"event.HEEJJhelphiZl1", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphiZl1", ""],
    ["HMMJJhelphiZl2" ,"event.HMMJJhelphiZl2", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphiZl2", ""],
    ["HEEJJhelphiZl2" ,"event.HEEJJhelphiZl2", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphiZl2", ""],
    ["HMMJJphistarZl1" ,"event.HMMJJphistarZl1", 20, 0 , 3.5, def_plot, "", "", "HMMJJphistarZl1", ""],
    ["HEEJJphistarZl1" ,"event.HEEJJphistarZl1", 20, 0 , 3.5, def_plot, "", "", "HEEJJphistarZl1", ""],
    ["HMMJJphistarZl2" ,"event.HMMJJphistarZl2", 20, 0 , 3.5, def_plot, "", "", "HMMJJphistarZl2", ""],
    ["HEEJJphistarZl2" ,"event.HEEJJphistarZl2", 20, 0 , 3.5, def_plot, "", "", "HEEJJphistarZl2", ""],
    #["J1btag" ,"event.J1btag", 20, -1.1, 1.1, def_plot, "", "", "J1btag", ""],
    #["J2btag" ,"event.J2btag", 20, -1.1 , 1.1, def_plot, "", "", "J2btag", ""],
    ["VBFJ1btag" ,"event.VBFJ1btag", 20, -1.1 , 1.1, def_plot, "", "", "VBFJ1btag", ""],
    ["VBFJ2btag" ,"event.VBFJ2btag", 20, -1.1 , 1.1, def_plot, "", "", "VBFJ2btag", ""],
    ["ZEEPt" ,"event.ZEEPt", 100, 0. , 600, def_plot, "", "", "ZEEPt", ""],
    ["ZMMPt" ,"event.ZMMPt", 100, 0. , 600, def_plot, "", "", "ZMMPt", ""],
    ["ZJJPt" ,"event.ZJJPt", 100, 0. , 600, def_plot, "", "", "ZJJPt", ""],
    ["HEEJJPt" ,"event.HEEJJPt", 100, 0. , 600, def_plot, "", "", "HEEJJPt", ""],
    ["HMMJJPt" ,"event.HMMJJPt", 100, 0. , 600, def_plot, "", "", "HMMJJPt", ""],
    ["ZLLJJPtSum" ,"max(event.ZEEPt, event.ZMMPt)+event.ZJJPt" , 200, 0. , 2000, def_plot, "", "", "ZLLPt+ZJJPt", ""],
    ["HEEJJEta" ,"event.HEEJJEta", 50, -5. , 5, def_plot, "", "", "HEEJJEta", ""],
    ["HMMJJEta" ,"event.HMMJJEta", 50, -5. , 5, def_plot, "", "", "HMMJJEta", ""],
    ["HMMclassifier_value", "HMMclassifier_value", 100, -0.8, 0.8, def_plot, "", "", "bdt", ""],
    ["HEEclassifier_value", "HEEclassifier_value", 100, -0.8, 0.8, def_plot, "", "", "bdt", ""],
    ["HEEJJLD", "event.HEEJJLD", 50, 0, 1, def_plot, "", "", "LD HEEJJ", ""],
    ["HMMJJLD", "event.HMMJJLD", 50, 0, 1, def_plot, "", "", "LD HMMJJ", ""],
]
#name of the tree you want to look for in the files
treename="hjjlltreeproducerhm_hjjllanalyzerhm"

#get the list of signals and backgrounds
def defineSamples(massmin, massmax, step, sigonly, bkgonly):
  signals=[]
  backgrounds=[]
  for mass in range(massmin, massmax+step, step):
    ggxsec=getXsec(mass, "gg")
    print "ggxsec", ggxsec
    ggeff=getEff(mass, "gg")
    print "ggeff", ggeff

    vbfxsec=getXsec(mass, "vbf")
    print "vbfxsec",vbfxsec
    vbfeff=getEff(mass, "vbf")
    print "vbfeff",vbfeff

    br = getBr(mass)
    print "br", br

    signals.append(["V7/VBFH"+str(mass)+"/hjjlltreeproducerhm_hjjllanalyzerhm/hjjlltreeproducerhm_hjjllanalyzerhm_tree.root",(vbfxsec[0]*br[0]*0.14)*0.376148809643,"VBFH"+str(mass),"VBFH"+str(mass), "True"+def_condition, mass])
    #signals.append(["~vagori/public/VBFH"+str(mass)+"/hjjlltreeproducerhm_hjjllanalyzerhm/hjjlltreeproducerhm_hjjllanalyzerhm_tree.root",(vbfxsec[0]*br[0]*0.14)*vbfeff,"VBFH"+str(mass),"VBFH"+str(mass), "True"+def_condition, mass]),
    #signals.append(["~vagori/public/VBFH"+str(mass)+"/hjjlltreeproducerhm_hjjllanalyzerhm/hjjlltreeproducerhm_hjjllanalyzerhm_tree.root",(vbfxsec[0]*br[0]*0.14)*vbfeff,"VBFH"+str(mass),"VBFH"+str(mass), "True"+def_condition, mass]),

  backgrounds=[
    ["V7/DY2Jet_treeproducerhm.root", (666.30)*0.029571432944, "DY50J2", "DY50J2", "True"+def_condition], 
    ["V7/DY3Jet_treeproducerhm.root", (214.97)*0.0610400939618, "DY50J3", "DY50J3", "True"+def_condition], 
    ["V7/DY4Jet_treeproducerhm.root", (60.69)*0.08356401767, "DY50J4", "DY50J4", "True"+def_condition], 
    ["V7/DY200To400_treeproducerhm.root", (23.43)*0.147013266797, "DY50HT200To400", "DY50HT200To400", "True"+def_condition], 
    ["V7/DY400ToInf_treeproducerhm.root", (3.365)*0.211445990669, "DY50HT400ToInf", "DY50HT400ToInf", "True"+def_condition], 
    #["V6/dy50_treeproducerhm.root", (3503.71)*0.0627984012868, "DY50", "DY50", "True"+def_condition], 
    #["V6/dy1_treeproducerhm.root", (667.6)*0.083927, "DY50_1", "DY50_1", "True"+def_condition],
    #["V6/dy2_treeproducerhm.root", (215.4)*0.137033556, "DY50_2", "DY50_2", "True"+def_condition],
    #["V6/dy3_treeproducerhm.root", (60.7)*0.20019701, "DY50_3", "DY50_3", "True"+def_condition],
    #["V6/dy4_treeproducerhm.root", (27.4)*0.26028636, "DY50_4", "DY50_4", "True"+def_condition],

  ]
    
  mclist = [];
  if not bkgonly:
    for signal in signals:
      mclist.append(signal)
  if not sigonly:
    for background in backgrounds :
      mclist.append(background)
  
  return signals, backgrounds, mclist

#auxiliary function to parse xsection output
def group_by_heading( some_source , match):
    buffer= []
    for line in some_source:
        if line.startswith( match ):
            if buffer: yield buffer
            buffer= [ line ]
        else:
            buffer.append( line )
    yield buffer

def getXsec(mass, vbforgg):
  if vbforgg == "vbf":
    link = xsecvbf
  else:
    link = xsecgg

  file=urllib2.urlopen(link)

  for line in file:
    match=str(mass)+'.0'
    if line.startswith(match):
      xsecline = line.rstrip('\n').split()
      return [float(xsecline[1]), float(xsecline[2])/100.*float(xsecline[1]), float(xsecline[3])/100.*float(xsecline[1])]

#auxiliary function to read BR
def getBr(mass):
  file = open ("br.txt", "r")
  for line in file:
    if line.startswith(str(mass)):
      ls = line.split()
      return [float(ls[13]), float(ls[14])/100.*float(ls[13]), float(ls[15])/100.*float(ls[13])]

#auxiliary function to get the preselection eff
def getEff(mass, sample):
  if sample == "vbf":
    match="VBF_HToZZTo2L2Q_M-"+str(mass)+"_8TeV-powheg-pythia6"
    start = "VBF_HToZZTo2L2Q_M"
    link=effvbf 
  elif sample == "gg":
    match="GluGluToHToZZTo2L2Q_M-"+str(mass)+"_8TeV-powheg-pythia6" 
    start="GluGluToHToZZTo2L2Q_M"
    link=effgg
  file=urllib2.urlopen(link)
  
  groups = group_by_heading(file, start)
  for group in groups:
    if group[0].startswith(match):
      #print group[1:]
      return (float)((group[5].rstrip('\n').split())[1])   

#book histograms
def bookHistograms(signals, backgrounds, mclist, indexcontent):
  linecolors=[]
  linestyle=[]
  linewidth=[]
  fillcolors=[]
  fillstyles=[]
  smooth=[]
  lastcolor=0
  for i in range(len(signals)):
    color = 2+i/2;
    #blue is for backgrounds
    if color == 4:
      color+=1
    linecolors.append(color)
    fillcolors.append(0)
    fillstyles.append(0)
    linewidth.append(2)
    if i%2 == 0:
      linestyle.append(1)
    else:
      linestyle.append(2)
    smooth.append(False)
    lastcolor=color
 
  for i in range(len(backgrounds)):
    #linecolors.append(lastcolor+i)
    linecolors.append(4)
    fillcolors.append(4)
    fillstyles.append(3013)
    smooth.append(False)
    if i < len(backgrounds)-1:
      linewidth.append(-1)
    else:
      linewidth.append(2)
    linestyle.append(1)

  h1glob=[]
  for index in range(0,len(mclist)):
    mc=mclist[index]
    tag=mc[2]

    h1loc = []
    for h1 in range(0,len(h1_list)):
        param=h1_list[h1]
        h1loc.append(TH1F(param[0]+tag,param[0]+tag,param[2],param[3],param[4]))
        h1loc[len(h1loc)-1].SetLineColor(linecolors[index])
        #h1loc[len(h1loc)-1].SetLineWidth(2)
        h1loc[len(h1loc)-1].SetMarkerColor(linecolors[index])
        h1loc[len(h1loc)-1].SetLineStyle(linestyle[index])
        #if index != 0:
        h1loc[len(h1loc)-1].SetFillStyle(fillstyles[index]);
        h1loc[len(h1loc)-1].SetFillColor(fillcolors[index])
        h1loc[len(h1loc)-1].SetLineWidth(linewidth[index])
        h1loc[len(h1loc)-1].Sumw2()
        #indexcontent+="<IMG SRC=\""+param[0]+".png\">\n"
    if (len(h1loc)):
      h1glob.append(h1loc)
  for h1 in range(0,len(h1_list)):
    param=h1_list[h1]
    indexcontent+="<IMG SRC=\""+param[0]+".png\">\n"

  gROOT.ProcessLine(".L ~/tdrStyle.C");
  setTDRStyle()
  return h1glob, indexcontent

def draw(h1glob, plot_dire, indexcontent, v_neventsprocessed, v_neventspassed, v_lumiweight):
  # first prepare legenda
  #yheaderstart=.95-.023*len(mclist)
  leg_hist = TLegend(0.30,0.85,0.98,0.98);
  leg_hist.SetFillColor(0)# Have a white background
  leg_hist.SetTextSize(0.03)
  leg_hist.SetNColumns(2)
  leg_hist.SetHeader( "L = %s/fb" %str(float(lumi/1000.)))

  leg_hist2 = TLegend(0.30,0.85,0.98,0.98);
  leg_hist2.SetFillColor(0)# Have a white background
  leg_hist2.SetTextSize(0.03)
  leg_hist2.SetNColumns(2)
  leg_hist2.SetHeader("Normalized to 1")

  backgroundcolor = (h1glob[len(mclist)-1])[0].GetLineColor()
  backgroundfill = (h1glob[len(mclist)-1])[0].GetFillColor()
  backgroundfillstyle = (h1glob[len(mclist)-1])[0].GetFillStyle()
  print "backgroundfillstyle", backgroundfillstyle


  first=True
  for index in range(0,len(mclist)):
    opt="same"
    mc=mclist[index]
    if (first):
        first=False
        opt=""
    if index<len(signals):
      leg_hist2.AddEntry((h1glob[index])[0],mc[3],"l")
      leg_hist.AddEntry((h1glob[index])[0],mc[3],"l")
    if index == len(h1glob)-1:
      leg_hist.AddEntry( (h1glob[index])[0], "All backgrounds", "lf");
      leg_hist2.AddEntry( (h1glob[index])[0], "All backgrounds", "lf");
    #leg_hist.AddEntry((h1glob[index])[0],mc[3],"l")

  canv=[]
  #gStyle.SetOptStat(11111111)
  #for i,h1 in enumerate(h1_list):
  for i,h1 in enumerate(h1_list):
    plot=h1[5]
    if not plot:
        continue
    tag=h1[0]
    canv.append(TCanvas("c_"+tag,"c_"+tag, 1000, 500))
    canv[len(canv)-1].Divide(2)
    canv[len(canv)-1].cd(1)
    stackbyhand = TH1F(tag,tag,h1[2],h1[3],h1[4])
    stackbyhand.Sumw2()
    if h1[6] != "":
      stackh_h = THStack(h1[6], h1[7])
    else:
      stackh_h = THStack(tag, tag)
    if not options.sigonly:  
      for index in range(len(signals),len(signals)+len(backgrounds)) :
        h1loc=h1glob[index]
        print index
        #if smooth[index]:
        #  h1loc[i].Smooth(1, "R")
        stackbyhand.Add(h1loc[i])
        stackh_h.Add(h1loc[i])
    themax = max(stackbyhand.GetMaximum(), (h1glob[0])[i].GetMaximum())
    if not options.sigonly:
      #stackh_h.Draw("HIST")
      stackbyhand.Draw("HIST")
      if h1[8] != "":
        #stackh_h.GetXaxis().SetTitle(h1[8])
        stackbyhand.GetXaxis().SetTitle(h1[8])
      if h1[9] != "":
        #stackh_h.GetYaxis().SetTitle(h1[9])
        stackbyhand.GetYaxis().SetTitle(h1[9])
      (h1glob[0])[i].Scale(scalesig)
      #stackh_h.SetMaximum(20*themax)
      stackbyhand.SetMaximum(20*themax)
      #stackh_h.SetMinimum(0.1)
      stackbyhand.SetMinimum(0.1)
      for isig in range(len(signals)):
        (h1glob[isig])[i].Draw("HISTsames")
    else:
      for isig in range(len(signals)):
        if h1[8] != "":
          (h1glob[isig])[i].GetXaxis().SetTitle(h1[8])
        if h1[9] != "":
          (h1glob[isig])[i].GetXaxis().SetTitle(h1[9])
        (h1glob[isig])[i].GetYaxis().SetRangeUser(0.02, 20*themax)
        if (isig==0):
          (h1glob[isig])[i].Draw("HIST")
        else:
          (h1glob[isig])[i].Draw("HISTsames")
    
    leg_hist.Draw("sames")
    gPad.SetLogy()
    gPad.Update()
    canv[len(canv)-1].cd(2)
    if not options.sigonly:
      stackbyhand.GetXaxis().SetTitle(h1[8])
      stackbyhand.GetYaxis().SetTitle(h1[9])
      stackbyhand.SetLineColor(backgroundcolor) #len(fillcolors)-1])
      stackbyhand.SetFillColor(backgroundfill)
      stackbyhand.SetFillStyle(backgroundfillstyle)
      stackbyhand.SetLineWidth(2)
      #stackbyhand.DrawNormalized()
      stackbyhandclone = stackbyhand.Clone()
      integral = stackbyhandclone.Integral()
      if integral == 0.:
        integral = 1.
      stackbyhandclone.Scale(1/integral)
    clonemax=0
    h1clones=[]
    for isig in range(len(signals)):
      h1clone = (h1glob[isig])[i].Clone()
      #integral = max(1., h1clone.Integral())
      integral = h1clone.Integral()
      if integral == 0.:
        integral = 1.
      h1clone.Scale(1/integral)
      h1clones.append(h1clone)
      if h1clone.GetMaximum() > clonemax:
        clonemax = h1clone.GetMaximum()
    themax = clonemax
    if not options.sigonly:
      themax = max(stackbyhandclone.GetMaximum(), clonemax)
      stackbyhandclone.GetYaxis().SetRangeUser(0, 1.3*themax)
      stackbyhandclone.Draw("HIST")
      for clone in h1clones:
        clone.Draw("HISTsames")
    else:
      for icl in range(len(h1clones)):
        h1clones[icl].GetXaxis().SetTitle(h1[8])
        h1clones[icl].GetYaxis().SetTitle(h1[9])
        h1clones[icl].GetYaxis().SetRangeUser(0, 1.3*themax)
        if icl==0:
          h1clones[icl].Draw("HIST")
        else:
          h1clones[icl].Draw("HISTsames")
    leg_hist2.Draw("sames")
    canv[len(canv)-1].Print(plot_dire+"/"+tag+".png")
    canv[len(canv)-1].Print(plot_dire+"/"+tag+".C")
    canv[len(canv)-1].Print(plot_dire+"/"+tag+".eps")
    if "HMMJJMass" in h1[0] or "HEEJJMass" in h1[0]:
      for index in range(len(signals)):
        mass = float(massmin+(index/2)*step)
        minmass = mass-0.06*mass
        maxmass = mass+0.1*mass
        statssig=numpy.array([0.,0.,0.,0.])
        statsback=numpy.array([0.,0.,0.,0.])
        (h1glob[index])[i].GetXaxis().SetRangeUser(minmass, maxmass)
        (h1glob[index])[i].GetStats(statssig)
        stackbyhand.GetXaxis().SetRangeUser(minmass, maxmass)
        stackbyhand.GetStats(statsback)
        nsel = v_neventspassed[index] #(h1glob[index])[i].GetEntries()
        print statssig[0],statssig[1]
        type = "VBF"
        if index%2 != 0:
          type = "GG"
        print type
        type=type+str(mass)
        area = (h1glob[index])[i].Integral()/scalesig
        eff_plus = ((nsel/v_neventsprocessed[index]+0.5/v_neventsprocessed[index])+\
                     math.sqrt(math.pow((nsel/v_neventsprocessed[index]+0.5/v_neventsprocessed[index]),2)-math.pow(nsel,2)/math.pow(v_neventsprocessed[index],2)*(1.+1./v_neventsprocessed[index]) ))/(1.+1./v_neventsprocessed[index])
        eff_minus = ((nsel/v_neventsprocessed[index]+0.5/v_neventsprocessed[index])-\
                     math.sqrt(math.pow((nsel/v_neventsprocessed[index]+0.5/v_neventsprocessed[index]),2)-math.pow(nsel,2)/math.pow(v_neventsprocessed[index],2)*(1.+1./v_neventsprocessed[index]) ))/(1.+1./v_neventsprocessed[index])
        print "effplus, effminus, eff ", eff_plus, eff_minus, float(nsel/v_neventsprocessed[index])            
        error_plus = (v_neventsprocessed[index]*eff_plus - nsel)*v_lumiweight[index]
        error_minus = (nsel - v_neventsprocessed[index]*eff_minus)*v_lumiweight[index]
        #protection for numeric accuracy
        if nsel==0:
          error_minus = 0.
        #TODO CAREFUL! I'm assuming, for the rerrors that half is electrons half is muons  
        indexcontent+="<CENTER>#events in signal "+type+" in ("+str(minmass)+","+str(maxmass)+") for "+h1[0]+": "+str((h1glob[index])[i].Integral()/scalesig)+ \
                    "+" + str(error_plus)+"-"+str(error_minus)+' estimated from '+str(float(nsel)/2.)+" events with lumi weight "+str(v_lumiweight[index])+'</CENTER>\n'
        if not options.sigonly:            
          for index2 in range(len(backgrounds)):
            imc = len(signals)+index2
            nsel = v_neventspassed[imc] #(h1glob[index])[i].GetEntries()
            (h1glob[imc])[i].GetXaxis().SetRangeUser(minmass, maxmass)
            area = (h1glob[imc])[i].Integral()
            eff_plus = ((nsel/v_neventsprocessed[imc]+0.5/v_neventsprocessed[imc])+\
                       math.sqrt(math.pow((nsel/v_neventsprocessed[imc]+0.5/v_neventsprocessed[imc]),2)-math.pow(nsel,2)/math.pow(v_neventsprocessed[imc],2)*(1.+1./v_neventsprocessed[imc]) ))/(1.+1./v_neventsprocessed[imc])
            eff_minus = ((nsel/v_neventsprocessed[imc]+0.5/v_neventsprocessed[imc])-\
                       math.sqrt(math.pow((nsel/v_neventsprocessed[imc]+0.5/v_neventsprocessed[imc]),2)-math.pow(nsel,2)/math.pow(v_neventsprocessed[imc],2)*(1.+1./v_neventsprocessed[imc]) ))/(1.+1./v_neventsprocessed[imc])
            print "nsel, eff_plus, eff_minus", nsel, eff_plus, eff_minus           
            error_plus = (v_neventsprocessed[imc]*eff_plus - float(nsel))*v_lumiweight[imc]
            error_minus = (-v_neventsprocessed[imc]*eff_minus + float(nsel))*v_lumiweight[imc]
            #protection for numeric accuracy
            if nsel==0:
              error_minus = 0.
            #TODO CAREFUL! I'm assuming, for the rerrors that half is electrons half is muons  
            indexcontent+="<CENTER>#events in background "+(backgrounds[index2])[2]+" "+str(mass)+" in ("+str(minmass)+","+str(maxmass)+") for "+h1[0]+": "+str(h1glob[imc][i].Integral()) + \
                        "+" + str(error_plus)+"-"+str(error_minus)+" estimated from "+str(float(nsel)/2.)+" events with lumi weight "+str(v_lumiweight[imc])+'</CENTER>\n'
                      
        #toterrp = 0.
        #toterrn = 0.
        #for i in range(len(errpos)):
        #  toterrp += math.pow(errpos[i], 2)
        #  toterrn += math.pow(errneg[i], 2)
        #toterrp = math.sqrt(toterrp)
        #toterrm = math.sqrt(toterrn)
        indexcontent+="<CENTER>-----------------------------------</CENTER>\n"
          
 
  indexcontent+="<HR WIDTH=\"100%\">\n"
  indexcontent+="</HTML>\n"
  out_file = open(plot_dire+"/index.html","w")
  out_file.write(indexcontent)
  out_file.close()
  


class ExtendedOption (Option):
  ACTIONS = Option.ACTIONS + ("extend",)
  STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
  TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
  ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

  def take_action(self, action, dest, opt, value, values, parser):
    if action == "extend":
      lvalue = value.split(",")
      values.ensure_value(dest, []).extend(lvalue)
    else:
      Option.take_action(self, action, dest, opt, value, values, parser)


if __name__=="__main__":
  usage  = "usage: %prog massstart massend stepsize [options]\n"

  parser = OptionParser(usage=usage,option_class=ExtendedOption)
  parser.add_option('-f', "--force", action="store_true", help="overwrite old results (default=False)", default=False)
  parser.add_option('-o', "--output", action="store", help="output directory (default=plots)", default='plots')
  parser.add_option('-s', "--step", action="store", help="at which step make plots (default=0)", default=0)
  parser.add_option('-n', "--nevents", action="store", help="number of events to process (default=10000000)", default=10000000)
  parser.add_option('-l', "--lumi", action="store", help="luminosity to normalize the MC in /pb, default=20000", default=20000)
  parser.add_option('--sigonly',  action="store_true", help="process signals only (default=False)", default=False)
  parser.add_option('--bkgonly',  action="store_true", help="process backgrounds only (default=False)", default=False)
  parser.add_option('--scalesignals',  action="store", help="multiply all signals by a factor (default=1.)", default=1.)
  parser.add_option('--mva',  action="store_true", help="for the moment only one mass point st a tme can be done when evaluating mva", default=False)
  parser.add_option('--mvacut', action='store', help="cut to apply on mva (default=no cut)", default=-9999999999.)
  parser.add_option('--syst', action="store", help = "perform syst evaluation (default=None), available: JESUP, JESDOWN  ", default=None)

  (options, args) = parser.parse_args()
  if len(args)<3 :
    parser.print_help()
    sys.exit(1)               

  gROOT.SetBatch(True)

  plot_dire=options.output
  if (options.syst != None):
    plot_dire += "_"+options.syst
  stepplot=int(options.step)
  maxevent=int(options.nevents)
  lumi=options.lumi
  scalesig=float(options.scalesignals)
  massmin=int(args[0])  
  massmax=int(args[1])  
  step=int(args[2])  

  if os.path.exists(plot_dire) and options.force is False:
    print 'directory '+plot_dire+' exists already, doing nothing.'
    print 'You can overwrite with the --force option'
    sys.exit(1)
  
  if options.mva and massmin != massmax:
    print "You can only do 1 mass point at a time when doing mva evaluation"
    sys.exit(1)

  os.system("mkdir -p "+plot_dire)

  indexcontent = ""
  indexcontent += "<HTML>\n"
  indexcontent += "<CENTER>"+def_condition+"</CENTER>\n"

  #define samples
  signals, backgrounds, mclist = defineSamples(massmin, massmax, step, options.sigonly, options.bkgonly) 
  if options.mva:
    gSystem.CompileMacro(mvatraining+str(massmin)+"GeV_fullDY/TMVAClassification_BDT.class.C")
    from ROOT import ReadBDT
    varnames = vector("string") ()
    varnames.push_back("J1Pt")
    varnames.push_back("J2Pt")
    varnames.push_back("VBFJ1Pt")
    varnames.push_back("VBFJ1Eta")
    varnames.push_back("max(HEEJJdetaVBF,HMMJJdetaVBF)")
    varnames.push_back("min(fabs(HEEJJDeltaPhiZ),fabs(HMMJJDeltaPhiZ))")
    varnames.push_back("max(HEEJJhelcosthetaZl2,HMMJJhelcosthetaZl2)")
    varnames.push_back("max(HMMJJcosthetastar,HEEJJcosthetastar)")
    varnames.push_back("ZJJMass")
    varnames.push_back("max(ZEEPt,ZMMPt)+ZJJPt")
    classifier = ReadBDT(varnames)

  #book all histograms
  h1glob, indexcontent = bookHistograms(signals, backgrounds, mclist, indexcontent)

  # do sample loop
  #fitmu = MLFit(plot_dire, "event.ZMMMass>0")
  v_neventsprocessed = []
  v_neventspassed = []
  v_lumiweight = []
  for index,mc in enumerate(mclist):
    rootfile=mc[0]
    xsec=mc[1]
    print xsec
    tag=mc[2]

    neventsprocessed = 0
    lastevent=-1
    treefile=TFile.Open(rootfile)
    print "opening ",rootfile
    tree=treefile.Get(treename)
    nevents=tree.GetEntries()
    nevents=min(nevents,maxevent)
    # loop on tree entries
    #weight=mc[1] #xsec*lumi/nevents
    
    h1loc=h1glob[index]
    read=0
    #nevents passing default selection
    npass = 0
    passpresel = False
    #do event loop
    sv=SystematicVariation(False)
    lumiweight = xsec/nevents * lumi
    for event  in tree:
        if (options.syst) != None:
          if options.syst == "JESUP":
            event = sv.applyJES(event, True)
          elif options.syst == "JESDOWN":   
            event = sv.applyJES(event, False)
          else:
            print "SYSTEMATIC unavailable", options.syst
            break;
        if read>=nevents:
            break
        read+=1
        if read % 10000 ==1:
            print "Reading event:",read,'/',nevents
        neventsprocessed += 1
        passpresel = False

        addcut = eval(mc[4])
        #theweight = event.weight*lumiweight
        theweight = lumiweight
        #for binomial error calculation
        #sumofinitialweights+=theweight
        HEEclassifier_value = -99.
        HMMclassifier_value = -99.
        if options.mva and addcut:
          vars = vector("double") ()
          vars.push_back(event.J1Pt)
          vars.push_back(event.J2Pt)
          vars.push_back(event.VBFJ1Pt)
          vars.push_back(event.VBFJ1Eta)
          vars.push_back(max(event.HEEJJdetaVBF, event.HMMJJdetaVBF))
          vars.push_back(min(abs(event.HEEJJDeltaPhiZ), abs(event.HMMJJDeltaPhiZ)))
          vars.push_back(max(event.HEEJJhelcosthetaZl2, event.HMMJJhelcosthetaZl2))
          vars.push_back(max(event.HMMJJcosthetastar, event.HEEJJcosthetastar))
          vars.push_back(event.ZJJMass)
          vars.push_back(max(event.ZEEPt,event.ZMMPt)+event.ZJJPt)
          classifier_value = classifier.GetMvaValue(vars)
          #print classifier_value;
          addcut = addcut and (classifier_value>float(options.mvacut))
          if event.HMMJJMass > event.HEEJJMass:
            HMMclassifier_value = classifier_value
          else:  
            HEEclassifier_value = classifier_value
          
                
        if addcut:
            passpresel = True
            npass+=event.weight
            #fitmu.addToDataset(event, index<len(signals))
            # here we can put all plots after selection
            for i,h1 in enumerate(h1loc):
                param=h1_list[i]
                h1.Fill(eval(param[1]), theweight)
    print xsec, lumiweight, neventsprocessed, npass
    v_neventsprocessed.append(neventsprocessed)
    v_neventspassed.append(npass)
    v_lumiweight.append(lumiweight)
    #for i,h1 in enumerate(h1loc):
    #  h1.Scale(weight)
    treefile.Close()


  #finally draw histograms
  draw(h1glob, plot_dire, indexcontent, v_neventsprocessed, v_neventspassed, v_lumiweight)
  #fitmu.fit()
  
