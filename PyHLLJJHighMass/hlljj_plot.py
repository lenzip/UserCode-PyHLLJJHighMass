#!/usr/bin/env python
import os,string,sys,commands,time,ConfigParser
from ROOT import *
from CMGTools.RootTools.utils.DeltaR import deltaR
from array import array
import numpy
import urllib2
# legenda:
# step 0--> all
# step 1--> after njet cut
# step 2--> after cut on energy
# step 3--> after 2 tau candidate
# step 4--> after testID
# step 5--> after findhz
xsecgg="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-ggH.txt?revision=1.4&view=markup"
xsecvbf="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-vbfH.txt?revision=1.7&view=markup"
effvbf="http://lenzip.web.cern.ch/lenzip/H2l2q/Efficiencies/effVBF.txt"
effgg="http://lenzip.web.cern.ch/lenzip/H2l2q/Efficiencies/effGG.txt"

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

def getBr(mass):
  file = open ("br.txt", "r")
  for line in file:
    if line.startswith(str(mass)):
      ls = line.split()
      return [float(ls[13]), float(ls[14])/100.*float(ls[13]), float(ls[15])/100.*float(ls[13])]

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



               

if len(sys.argv)!=8:
    print "Usage:",sys.argv[0]+" <plot directory> <step> <maxevent> <batch 1=yes> <massmin> <massmax> <step>"
    sys.exit(1)

plot_dire=sys.argv[1]+"/"
stepplot=int(sys.argv[2])
maxevent=int(sys.argv[3])
batch=int(sys.argv[4])
massmin=int(sys.argv[5])  
massmax=int(sys.argv[6])  
step=int(sys.argv[7])  
if batch==1:
    print "working in batch mode, no plot will be shown"
    gROOT.SetBatch(True)
    

print "Parameters:",plot_dire,stepplot,maxevent,batch

os.system("mkdir -p "+plot_dire)

indexcontent = ""
indexcontent += "<HTML>\n"



lumi=20000
#def_condition = " and (event.J1Pt > 20 and event.J2Pt > 20. and event.VBFJ1Pt > 65. and event.VBFJ2Pt > 35.)"
def_condition = " and (event.J1Pt > 30 and event.J2Pt > 30. and event.VBFJ1Pt > 50. and event.VBFJ2Pt > 30.)"
def_condition += " and ((event.M1Pt > 40 and event.M2Pt > 20.) or (event.E1Pt > 40 and event.E2Pt > 20.))"
def_condition += " and ((event.ZEEMass > 76. and event.ZEEMass < 106.) or (event.ZMMMass > 76. and event.ZMMMass < 106.))"
def_condition += " and (event.ZJJMass > 71. and event.ZJJMass < 111.)"
#def_condition += " and max(event.HEEJJmassVBF, event.HMMJJmassVBF)> 400"
#def_condition += " and max(event.HEEJJdetaVBF, event.HMMJJdetaVBF)> 4"
#def_condition += " and event.ZJJPt > 80."
#def_condition += " and (abs(event.HEEJJcosthetastar) < 0.8 or abs(event.HMMJJcosthetastar) < 0.8)"
indexcontent += "<CENTER>"+def_condition+"</CENTER>\n"

signals=[]

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

    signals.append(["~vagori/public/VBFH"+str(mass)+"/hjjlltreeproducerhm_hjjllanalyzerhm/hjjlltreeproducerhm_hjjllanalyzerhm_tree.root",(vbfxsec[0]*br[0]*0.14)*vbfeff,"VBFH"+str(mass),"VBFH"+str(mass), "True"+def_condition]),
    signals.append(["/afs/cern.ch/user/l/lenzip/public/FromAntonio/V6_gg/GGH"+str(mass)+"/hjjlltreeproducerhm_hjjllanalyzerhm/hjjlltreeproducerhm_hjjllanalyzerhm_tree.root",(ggxsec[0]*br[0]*0.14)*ggeff,"GGH"+str(mass),"GGH"+str(mass), "True"+def_condition]),

backgrounds=[
    #["V6/dy50_treeproducerhm.root", (3503.71)*0.0627984012868, "DY50", "DY50", "True"+def_condition], 
#    ["V6/dy1_treeproducerhm.root", (667.6)*0.083927, "DY50_1", "DY50_1", "True"+def_condition], 
#    ["V6/dy2_treeproducerhm.root", (215.4)*0.137033556, "DY50_2", "DY50_2", "True"+def_condition], 
#    ["V6/dy3_treeproducerhm.root", (60.7)*0.20019701, "DY50_3", "DY50_3", "True"+def_condition], 
#    ["V6/dy4_treeproducerhm.root", (27.4)*0.26028636, "DY50_4", "DY50_4", "True"+def_condition], 

    ]
treename="hjjlltreeproducerhm_hjjllanalyzerhm"

mclist = [];
for signal in signals:
  mclist.append(signal)
for background in backgrounds :
  mclist.append(background)
print mclist  
print signals
# luminosity to normalize (in pb-1)

# step at which the plot should be made
#stepplot=6

# define special histograms
step_h=[]
genrec_s3_t1=[]
genrec_s3_t2=[]
mzh_h2=[]
dgen1_vs_iso_h2=[]
dgen2_vs_iso_h2=[]

# Define all others
# syntax: name, variable, nibn,xmin,xmax,visualize, tag (no strange character here),title,xlabel,ylabel 

step_label=["all","njet>4","ejet>10","2 taucand","2 good taucand","jet sele","mzmh cut","btag"]

def_plot=true
h1_list=[
#    ["ZJJMass" ,"event.ZJJMass" ,100,0,200,def_plot, "", "", "Mass J1J2 [GeV]", ""],
#    ["J1Pt" ,"event.J1Pt" ,100,0,200,def_plot, "", "", "pT J1 [GeV]", ""],
#    ["J2Pt" ,"event.J2Pt" ,100,0,200,def_plot, "", "", "pT J2 [GeV]", ""],
#    ["J1Eta" ,"event.J1Eta" ,100,-5,5,def_plot, "", "", "#eta J1", ""],
#    ["J2Eta" ,"event.J2Eta" ,100,-5,5,def_plot, "", "", "#eta J2", ""],
#    ["VBFJ1Pt" ,"event.VBFJ1Pt" ,100,0,200,def_plot, "", "", "pT VBF J1 [GeV]", ""],
#    ["VBFJ2Pt" ,"event.VBFJ2Pt" ,100,0,200,def_plot, "", "", "pT VBF J2 [GeV]", ""],
#    ["VBFJ1Eta" ,"event.VBFJ1Eta" ,100,-5,5,def_plot, "", "", "#eta VBF J1", ""],
#    ["VBFJ2Eta" ,"event.VBFJ2Eta" ,100,-5,5,def_plot, "", "", "#eta VBF J2", ""],
#    ["ZEEMass" ,"event.ZEEMass" ,100,0,200,def_plot, "", "", "Mass e+e- [GeV]", ""],
#    ["ZMMMass" ,"event.ZMMMass" ,100,0,200,def_plot, "", "", "Mass #mu+#mu- [GeV]", ""],
#    ["HMMJJMass" ,"event.HMMJJMass" ,200,0,2000,def_plot, "", "", "Mass H(#mu+#mu-jj)[GeV]", ""],
#    ["HEEJJMass" ,"event.HEEJJMass" ,200,0,2000,def_plot, "", "", "Mass (e+e-ll)[GeV]", ""],
#    ["HEEJJmassVBF" ,"event.HEEJJmassVBF" ,100,0,2000,def_plot, "", "", "Mass VBF pair for H(e+e-jj) [GeV]", ""],
#    ["HMMJJmassVBF" ,"event.HMMJJmassVBF" ,100,0,2000,def_plot, "", "", "Mass VBF pair for H(#mu+#mu-jj) [GeV]", ""],
#    ["HMMJJdetaVBF" ,"event.HMMJJdetaVBF" ,40,0,10,def_plot, "", "", "#Delta#eta VBF pair for H(#mu+#mu-jj) [GeV]", ""],
#    ["HEEJJdetaVBF" ,"event.HEEJJdetaVBF" ,40,0,10,def_plot, "", "", "#Delta#eta VBF pair for H(e+e-jj) [GeV]", ""],
#    ["HMMJJDeltaPhiZ" ,"abs(event.HMMJJDeltaPhiZ)" ,40,0,4,def_plot, "", "", "#Delta#phi Z(#mu+#mu-)Z(jj)", ""],
#    ["HEEJJDeltaPhiZ" ,"abs(event.HEEJJDeltaPhiZ)" ,40,0,4,def_plot, "", "", "#Delta#phi Z(e+e-)Z(jj)", ""],
#    ["HMMJJDeltaPhiZJ1" ,"abs(event.HMMJJDeltaPhiZJ1)" ,40,0,4,def_plot, "", "", "#Delta#phiZ(#mu+#mu-)J1", ""],
#    ["HEEJJDeltaPhiZJ1" ,"abs(event.HEEJJDeltaPhiZJ1)" ,40,0,4,def_plot, "", "", "#Delta#phiZ(e+e-)J1", ""],
#    ["HMMJJhelcosthetaZl1" ,"event.HMMJJhelcosthetaZl1" ,30,-1.5,1.5,def_plot, "", "", "helcosthetaZl1 H(#mu+#mu-jj)", ""],
#    ["HMMJJhelcosthetaZl2" ,"event.HMMJJhelcosthetaZl2" ,20,-0.5,1.5, def_plot, "", "", "helcosthetaZl2 H(#mu+#mu-jj)", ""],
#    ["HEEJJhelcosthetaZl1" ,"event.HEEJJhelcosthetaZl1" ,30,-1.5,1.5,def_plot, "", "", "helcosthetaZl1 H(e+e-jj)", ""],
#    ["HEEJJhelcosthetaZl2" ,"event.HEEJJhelcosthetaZl2" ,20,-0.5,1.5, def_plot, "", "", "helcosthetaZl2 H(e+e-jj)", ""],
#    ["HEEJJcosthetastar" ,"event.HEEJJcosthetastar" ,20,-1.1,1.1, def_plot, "", "", "costhetastar H(e+e-jj)", ""],
#    ["HMMJJcosthetastar" ,"event.HMMJJcosthetastar" ,20,-1.1,1.1, def_plot, "", "", "costhetastar H(e+e-jj)", ""],
#    ["HMMJJSumAbsEtaJ1J2" ,"event.HMMJJSumAbsEtaJ1J2" ,20,0,5., def_plot, "", "|#eta(J1)|+|#eta(J2)|, H(e+e-jj)", "", ""],
#    ["HEEJJSumAbsEtaJ1J2" ,"event.HEEJJSumAbsEtaJ1J2" ,20,0,5., def_plot, "", "|#eta(J1)|+|#eta(J2)|, H(#mu+#mu-jj)", "", ""],
##    ["HEEJJClassifier" ,"event.HEEJJClassifier" ,50,-0.8, 0.2, def_plot, "", "", "BDT classifier, H(e+e-jj)", ""],
##    ["HMMJJClassifier" ,"event.HMMJJClassifier", 50,-0.8, 0.2, def_plot, "", "", "BDT classifier, H(#mu+#mu-jj)", ""],
#    ["ZJJDeltaEtaDecay" ,"abs(event.J1Eta-event.J2Eta)", 50, 0 , 5, def_plot, "", "", "ZJJdeltaEtaDecay", ""],
    ["ZJJDeltaRDecay" ,"abs(deltaR(event.J1Eta, event.J1Phi, event.J2Eta, event.J2Phi))", 50, 0 , 5, def_plot, "", "", "ZJJdeltaRDecay", ""],
#    ["HMMJJhelphi" ,"event.HMMJJhelphi", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphi", ""],
#    ["HEEJJhelphi" ,"event.HEEJJhelphi", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphi", ""],
#    ["HMMJJhelphiZl1" ,"event.HMMJJhelphiZl1", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphiZl1", ""],
#    ["HEEJJhelphiZl1" ,"event.HEEJJhelphiZl1", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphiZl1", ""],
#    ["HMMJJhelphiZl2" ,"event.HMMJJhelphiZl2", 20, 0 , 3.5, def_plot, "", "", "HMMJJhelphiZl2", ""],
#    ["HEEJJhelphiZl2" ,"event.HEEJJhelphiZl2", 20, 0 , 3.5, def_plot, "", "", "HEEJJhelphiZl2", ""],
#    ["HMMJJphistarZl1" ,"event.HMMJJphistarZl1", 20, 0 , 3.5, def_plot, "", "", "HMMJJphistarZl1", ""],
#    ["HEEJJphistarZl1" ,"event.HEEJJphistarZl1", 20, 0 , 3.5, def_plot, "", "", "HEEJJphistarZl1", ""],
#    ["HMMJJphistarZl2" ,"event.HMMJJphistarZl2", 20, 0 , 3.5, def_plot, "", "", "HMMJJphistarZl2", ""],
#    ["HEEJJphistarZl2" ,"event.HEEJJphistarZl2", 20, 0 , 3.5, def_plot, "", "", "HEEJJphistarZl2", ""],
#    #["J1btag" ,"event.J1btag", 20, -1.1, 1.1, def_plot, "", "", "J1btag", ""],
#    #["J2btag" ,"event.J2btag", 20, -1.1 , 1.1, def_plot, "", "", "J2btag", ""],
#    ["VBFJ1btag" ,"event.VBFJ1btag", 20, -1.1 , 1.1, def_plot, "", "", "VBFJ1btag", ""],
#    ["VBFJ2btag" ,"event.VBFJ2btag", 20, -1.1 , 1.1, def_plot, "", "", "VBFJ2btag", ""],
#    ["ZEEPt" ,"event.ZEEPt", 100, 0. , 600, def_plot, "", "", "ZEEPt", ""],
#    ["ZMMPt" ,"event.ZMMPt", 100, 0. , 600, def_plot, "", "", "ZMMPt", ""],
#    ["ZJJPt" ,"event.ZJJPt", 100, 0. , 600, def_plot, "", "", "ZJJPt", ""],
#    ["HEEJJPt" ,"event.HEEJJPt", 100, 0. , 600, def_plot, "", "", "HEEJJPt", ""],
#    ["HMMJJPt" ,"event.HMMJJPt", 100, 0. , 600, def_plot, "", "", "HMMJJPt", ""],
#    ["ZLLJJPtSum" ,"max(event.ZEEPt, event.ZMMPt)+event.ZJJPt" , 200, 0. , 2000, def_plot, "", "", "ZLLPt+ZJJPt", ""],
#    ["HEEJJEta" ,"event.HEEJJEta", 50, -5. , 5, def_plot, "", "", "HEEJJEta", ""],
#    ["HMMJJEta" ,"event.HMMJJEta", 50, -5. , 5, def_plot, "", "", "HMMJJEta", ""],
]
    
linecolors=[]
linestyle=[]
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
  if i%2 == 0:
    linestyle.append(1)
  else:
    linestyle.append(2)
  smooth.append(False)
  lastcolor=color
  
for i in range(len(backgrounds)): 
  linecolors.append(lastcolor+i)
  fillcolors.append(4)
  fillstyles.append(3013)
  smooth.append(False)
  linestyle.append(1)

h1glob=[]
for index in range(0,len(mclist)):
    mc=mclist[index]
    tag=mc[2]

    step_h.append(TH1F("step_"+tag,"step_"+tag,10,0,10))
    step_h[index].SetLineColor(linecolors[index])
    step_h[index].SetLineWidth(2)
    step_h[index].SetMarkerColor(linecolors[index])
    step_h[index].SetFillColor(fillcolors[index])
    step_h[index].SetFillStyle(fillstyles[index])
    step_h[index].SetLineStyle(linestyle[index])
    for bin in range(1,len(step_label)+1):
        step_h[index].GetXaxis().SetBinLabel(bin,step_label[bin-1])    
#        step_h[index].LabelsOption("v","X")
    h1loc = []    
    for h1 in range(0,len(h1_list)):
        param=h1_list[h1]
        h1loc.append(TH1F(param[0]+tag,param[0]+tag,param[2],param[3],param[4]))  
        h1loc[len(h1loc)-1].SetLineColor(linecolors[index])
        h1loc[len(h1loc)-1].SetLineWidth(2)
        h1loc[len(h1loc)-1].SetMarkerColor(linecolors[index])
        h1loc[len(h1loc)-1].SetLineStyle(linestyle[index])
        #if index != 0:
        h1loc[len(h1loc)-1].SetFillStyle(fillstyles[index]);
        h1loc[len(h1loc)-1].SetFillColor(fillcolors[index])
        h1loc[len(h1loc)-1].Sumw2()
        #indexcontent+="<IMG SRC=\""+param[0]+".png\">\n" 
    h1glob.append(h1loc)            

for h1 in range(0,len(h1_list)):
  param=h1_list[h1]
  indexcontent+="<IMG SRC=\""+param[0]+".png\">\n"

#maxevent=100000000
# now loop on tree and project
nhtt=0
nhtt_sel=0
nhbbtt=0
nhbbtt_sel=0
gROOT.ProcessLine(".L ~/tdrStyle.C");
setTDRStyle()
#gROOT.ProcessLine(".L ~/tdrStyle.C");
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
    for event  in tree:
        if read>=nevents:
            break
        read+=1
        if read % 10000 ==1:
            print "Reading event:",read,'/',nevents
        #if (event.eventNumber != lastevent):
        #lastevent = event.eventNumber
        neventsprocessed += 1
        if passpresel:
          npass+=1
        passpresel = False

        addcut = eval(mc[4]) 
            
        #addcut = ( addcut and event.mu1recPt>5. ) or ( addcut and event.e1recPt>5. ) and addcut
        #addcut = ( event.dimuonTrigger or event.dielectronTrigger ) and addcut


        #for bin in range(0,int(event.step)+1):
        #    step_h[index].Fill(bin)
                
        #if event.step>=stepplot and addcut:
        if addcut:
            passpresel = True
            # here we can put all plots after selection
            for i,h1 in enumerate(h1loc):
                param=h1_list[i]
        #        print param[1]
                #h1.Fill(eval(param[1]),weight)
                h1.Fill(eval(param[1]))
    weight = xsec/neventsprocessed * lumi
    print xsec, weight, neventsprocessed, npass
    for i,h1 in enumerate(h1loc):
      h1.Scale(weight)
    treefile.Close()
    # renormalize step_h histo for efficiencies
    norm=step_h[index].GetBinContent(1)
    print norm
    if norm==0: norm=-1
    for bin in range(0,step_h[index].GetNbinsX()):
        step_h[index].SetBinContent(bin,step_h[index].GetBinContent(bin)/norm)

# first prepare legenda
#yheaderstart=.95-.023*len(mclist)
leg_hist = TLegend(0.30,0.85,0.98,0.98);
leg_hist.SetFillColor(0)# Have a white background
leg_hist.SetTextSize(0.03)
leg_hist.SetNColumns(2)

leg_hist2 = TLegend(0.30,0.85,0.98,0.98);
leg_hist2.SetFillColor(0)# Have a white background
leg_hist2.SetTextSize(0.03)
leg_hist2.SetNColumns(2)
#text_lumi = TText(60,320,"L = 500 fb-1");

c1=TCanvas("step","step")
#c1.SetFillColor(kWhite)
#c1.SetFillStyle(1001)
#gStyle.SetOptStat(0)
 
first=True
# legenda

#c1.Divide(1,2)
for index in range(0,len(mclist)):
    opt="same"
    mc=mclist[index]
    if (first):
        first=False
        opt=""
#    print index,opt
#    step_h[index].Draw(opt)
    if index<len(signals):
      leg_hist2.AddEntry(step_h[index],mc[3],"l")
    if index == len(signals):
      leg_hist.AddEntry( step_h[index], "All backgrounds", "lf");
      leg_hist2.AddEntry( step_h[index], "All backgrounds", "lf");
    leg_hist.AddEntry(step_h[index],mc[3],"l")

scalesig=1.
canv=[]
#gStyle.SetOptStat(11111111)
for i,h1 in enumerate(h1_list):
    plot=h1[5]
    if not plot:
        continue
    tag=h1[0]
    canv.append(TCanvas("c_"+tag,"c_"+tag, 1000, 500))
    canv[len(canv)-1].Divide(2)
    #canv[len(canv)-1].SetLogy()
    #canv[len(canv)-1].
    canv[len(canv)-1].cd(1)  
    stackbyhand = TH1F(tag,tag,h1[2],h1[3],h1[4])
    stackbyhand.Sumw2()
    if h1[6] != "":
      stackh_h = THStack(h1[6], h1[7])
    else:  
      stackh_h = THStack(tag, tag)
    for index in range(len(signals),len(signals)+len(backgrounds)) : 
    #for index in range(len(mclist)-1,-1,-1):
    #for index in range(len(mclist)-1,0,-1):
        h1loc=h1glob[index]
        print index
        if smooth[index]:
          h1loc[i].Smooth(1, "R")
        stackbyhand.Add(h1loc[i])  
        stackh_h.Add(h1loc[i])
    themax = max(stackbyhand.GetMaximum(), (h1glob[0])[i].GetMaximum()) 
    #stackbyhand.GetYaxis().SetRangeUser(0.02, 1.3*themax)
    if len(backgrounds):
      stackh_h.Draw("HIST")
      if h1[8] != "":
        stackh_h.GetXaxis().SetTitle(h1[8])
      if h1[9] != "":
        stackh_h.GetYaxis().SetTitle(h1[9])
      (h1glob[0])[i].Scale(scalesig)
      #(h1glob[0])[i].GetYaxis().SetRangeUser(0.02, 1.3*themax)
      stackh_h.SetMaximum(20*themax)
      stackh_h.SetMinimum(0.1)
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
    #text_lumi.Draw()
    canv[len(canv)-1].cd(2)
    #if h1[6] != "":
    #  normstackh_h = THStack(h1[6]+"norm", h1[7]+"norm")
    #else:
    #  normstackh_h = THStack(tag+"norm", tag+"norm")
    #for index1 in range(len(mclist)-1,-1,-1):
    #for index in range(len(mclist)-1,0,-1):
    #    h1loc=h1glob[index1]
    #    print index1
    #    if smooth[index1]:
    #      h1loc[i].Smooth(1, "R")
    #    h1loc2 = h1loc[i].Clone()
    #    h1loc2.SetName=str(h1loc[i].GetName())+"norm"
    #    h1loc2.SetTitle=str(h1loc[i].GetTitle())+"norm"
    #    normstackh_h.Add(h1loc2.Scale(1/stackbyhand.Integral()))
    if len(backgrounds):
      stackbyhand.GetXaxis().SetTitle(h1[8])
      stackbyhand.GetYaxis().SetTitle(h1[9])
      stackbyhand.SetLineColor(fillcolors[len(fillcolors)-1])
      stackbyhand.SetFillColor(fillcolors[len(fillcolors)-1])
      stackbyhand.SetFillStyle(fillstyles[len(fillstyles)-1])
      stackbyhand.SetLineWidth(2)
      #stackbyhand.DrawNormalized()
      stackbyhandclone = stackbyhand.Clone()
      stackbyhandclone.Scale(1/stackbyhandclone.Integral())
    clonemax=0
    h1clones=[]
    for isig in range(len(signals)):   
      h1clone = (h1glob[isig])[i].Clone()
      h1clone.Scale(1/h1clone.Integral())
      h1clones.append(h1clone)
      if h1clone.GetMaximum() > clonemax:
        clonemax = h1clone.GetMaximum()
    themax = clonemax    
    if (len(backgrounds)):
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
    #(h1glob[0])[i].Clone().DrawNormalized("sames")
    leg_hist2.Draw("sames")
    #if h1[8] != "":
    #  normstackh_h.GetXaxis().SetTitle(h1[8])
    #if h1[9] != "":
    #  normstackh_h.GetYaxis().SetTitle(h1[9])
    #leg_hist.Draw("sames")
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
        print statssig[0],statssig[1]
        type = "VBF"
        if index%2 != 0:
          type = "GG"
        print type 
        type=type+str(mass)  
        indexcontent+="<CENTER>#events in signal "+type+" in ("+str(minmass)+","+str(maxmass)+") for "+h1[0]+": "+str((h1glob[index])[i].Integral()/scalesig)+ \
                    "+/-" + str(sqrt(statssig[1])/scalesig)+'</CENTER>\n'
        indexcontent+="<CENTER>#events in background "+str(mass)+" in ("+str(minmass)+","+str(maxmass)+") for "+h1[0]+": "+str(stackbyhand.Integral()) + \
                  "+/-" + str(sqrt(statsback[1]))+'</CENTER>\n' 
        indexcontent+="<CENTER>-----------------------------------</CENTER>\n"          
      #print "#events in signal in 100,150 for "+h1[0], (h1glob[0])[i].Integral()/scalesig
      #print "#events in background in 100,150 for "+h1[0], stackbyhand.Integral()





#stackmzh_h2 = THStack("mzmh", "mzmh")
#for index in range(0,len(mclist)):
#    stackmzh_h2.Add(mzh_h2[index])
#stackmzh_h2.Draw("box")

indexcontent+="<HR WIDTH=\"100%\">\n"
indexcontent+="</HTML>\n"
out_file = open(plot_dire+"/index.html","w")
out_file.write(indexcontent)
out_file.close()

a=raw_input("hit a key to exit...")
