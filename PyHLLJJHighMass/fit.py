#!/usr/bin/env python

import copy

from CMGTools.RootTools.RootTools import *
from ROOT import gSystem, RooDataSet, RooRealVar, RooCategory, RooArgSet, RooExponential, RooAddPdf, RooBifurGauss, RooArgList, RooCmdArg, RooFit, RooLinkedList
gSystem.Load("libCondFormatsJetMETObjects")
from ROOT import JetCorrectorParameters, JetCorrectionUncertainty

class MLFit :
  def __init__(self, plot_dire, condition):
    self.plot_dire = plot_dire
    self.condition = condition
    self.mjj = RooRealVar("ZJJMass", "ZJJMass", 50., 7000.)
    #self.costhetastar = RooRealVar("costhetastar", "costhetastar", -1., 1.)
    self.weight = RooRealVar("weight", "weight", -100., 100.)
    self.isSignal = RooCategory("isSignal", "isSignal")
    self.isSignal.defineType("signal", 1);
    self.isSignal.defineType("background", 0);
    self.ras = RooArgSet(self.mjj, self.weight)
    self.ds = RooDataSet("ds"+condition, "ds"+condition, self.ras, "weight")
    
    #self.mu = RooRealVar("mu", "mu", 90., 80., 100.)
    #self.widthL = RooRealVar("widthL", "widthL", 15., 2., 30.)
    #self.widthR = RooRealVar("widthR", "widthR", 4., 2., 15.)
    #self.sigmass = RooBifurGauss("bifurgauss", "bifurgauss", self.mjj, self.mu, self.widthL, self.widthR)

    self.c0 = RooRealVar("c0", "c0", -100., 100.)
    self.bkgmass = RooExponential("expo", "expo", self.mjj, self.c0)

    #self.nsig = RooRealVar("nsig", "nsig", 100, 0, 200)
    #self.nbkg = RooRealVar("nbkg", "nbkg", 100, 0, 200)
  
    #self.components = RooArgList(self.sigmass, self.bkgmass)
    #self.coefficients = RooArgList(self.nsig, self.nbkg)

    self.modelmass = self.bkgmass #RooAddPdf("massmodel", "massmodel", self.components, self.coefficients)



  
  def addToDataset(self, event, isSignal):
    if not eval(self.condition):
      return
    self.mjj = event.ZJJMass
    print self.mjj
    #self.costhetastar = event.costhetastar
    self.weight = event.weight
    #self.isSignal = isSignal
    self.ds.fill()


  def fit(self):
    print "nentries", self.ds.numEntries()
    #for i in range(self.ds.numEntries()):
    #  argset = self.ds.get(i)
    #  argset.Dump()
    
    fitresult = self.modelmass.fitTo(self.ds, RooFit.Save(True), RooFit.Extended(), RooFit.PrintLevel(3), RooFit.Strategy(2)) #, RooFit.SumW2Error(True))
    #plot = self.mjj.frame()
    #self.ds.plotOn(plot)
    #self.ds.plotOn(plot, "isSignal==isSignal::background",MarkerColor(kRed))
    #self.modelmass.plotOn(plot)
    #plot.SaveAs(self.plot_dire+"/prova.png")


#if __name__=="__main__":
#  mlfit=MLFit("ciao", "ciao") 
  
  
