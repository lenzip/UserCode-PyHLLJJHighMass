#!/usr/bin/env python

import copy

from CMGTools.RootTools.RootTools import *
from ROOT import gSystem
gSystem.Load("libCondFormatsJetMETObjects")
from ROOT import JetCorrectorParameters, JetCorrectionUncertainty

from math import *




class JES:

  def __init__(self, filename):
    self.jcp = JetCorrectorParameters(filename, "")
    self.jcu = JetCorrectionUncertainty(self.jcp)

  def uncertainty(self, pt, eta):
    self.jcu.setJetPt(pt)
    self.jcu.setJetEta(eta)
    return self.jcu.getUncertainty(True);
  
class MyEvent:
  def __init__(self):
    return;

class SystematicVariation:
  def __init__(self, isData):
    filejes = "txt/Fall12_V7_MC_Uncertainty_AK5PFchs.txt" 
    if isData:
      filejes = "txt/Fall12_V7_DATA_Uncertainty_AK5PFchs.txt"
    self.jes = JES(filejes)

  def cloneEvent(self, event):
    cloneevent = MyEvent();
    cloneevent.J2Eta = event.J2Eta
    cloneevent.HEEJJcosthetastar = event.HEEJJcosthetastar
    cloneevent.HEEJJDeltaPhiZJ1 = event.HEEJJDeltaPhiZJ1
    cloneevent.ZJJEnergy = event.ZJJEnergy
    cloneevent.E1Mass = event.E1Mass
    cloneevent.VBFJ2Pt = event.VBFJ2Pt
    cloneevent.ZMMMass = event.ZMMMass
    cloneevent.VBFJ2NHFraction = event.VBFJ2NHFraction
    cloneevent.J1ChFraction = event.J1ChFraction
    cloneevent.HEEJJPhi = event.HEEJJPhi
    cloneevent.J2NHFraction = event.J2NHFraction
    cloneevent.E1Charge = event.E1Charge
    cloneevent.HEEJJDeltaPtZ = event.HEEJJDeltaPtZ
    cloneevent.HMMJJPt = event.HMMJJPt
    cloneevent.M1Mass = event.M1Mass
    cloneevent.HEEJJdetaVBF = event.HEEJJdetaVBF
    cloneevent.ZEEPhi = event.ZEEPhi
    cloneevent.VBFJ1NHFraction = event.VBFJ1NHFraction
    cloneevent.M2Phi = event.M2Phi
    cloneevent.M1Eta = event.M1Eta
    cloneevent.M2Charge = event.M2Charge
    cloneevent.E1Pt = event.E1Pt
    cloneevent.VBFJ2btag = event.VBFJ2btag
    cloneevent.VBFJ1EFraction = event.VBFJ1EFraction
    cloneevent.HEEJJdphiVBF = event.HEEJJdphiVBF
    cloneevent.J1Eta = event.J1Eta
    cloneevent.M2Energy = event.M2Energy
    cloneevent.J1Ntrk = event.J1Ntrk
    cloneevent.ZEEMass = event.ZEEMass
    cloneevent.E2Mass = event.E2Mass
    cloneevent.M2Mass = event.M2Mass
    cloneevent.J2btag = event.J2btag
    cloneevent.J1EFraction = event.J1EFraction
    cloneevent.ZMMCharge = event.ZMMCharge
    cloneevent.weight = event.weight
    cloneevent.njets = event.njets
    cloneevent.J2Ntrk = event.J2Ntrk
    cloneevent.J2Phi = event.J2Phi
    cloneevent.isVBFMatched = event.isVBFMatched
    cloneevent.VBFJ1Eta = event.VBFJ1Eta
    cloneevent.J2PFraction = event.J2PFraction
    cloneevent.ZMMPt = event.ZMMPt
    cloneevent.HMMJJDeltaPtZ = event.HMMJJDeltaPtZ
    cloneevent.ZMMEta = event.ZMMEta
    cloneevent.isDecayMatched = event.isDecayMatched
    cloneevent.ZJJEta = event.ZJJEta
    cloneevent.HMMJJClassifier = event.HMMJJClassifier
    cloneevent.ZJJPt = event.ZJJPt
    cloneevent.truezlepmass = event.truezlepmass
    cloneevent.VBFJ2Eta = event.VBFJ2Eta
    cloneevent.VBFJ2Ntrk = event.VBFJ2Ntrk
    cloneevent.HMMJJhelphi = event.HMMJJhelphi
    cloneevent.HEEJJhelcosthetaZl2 = event.HEEJJhelcosthetaZl2
    cloneevent.HEEJJhelcosthetaZl1 = event.HEEJJhelcosthetaZl1
    cloneevent.HMMJJdetaVBF = event.HMMJJdetaVBF
    cloneevent.VBFJ2Phi = event.VBFJ2Phi
    cloneevent.M1Charge = event.M1Charge
    cloneevent.HMMJJcosthetastar = event.HMMJJcosthetastar
    cloneevent.HMMJJMass = event.HMMJJMass
    cloneevent.iszee = event.iszee
    cloneevent.step = event.step
    cloneevent.E1Phi = event.E1Phi
    cloneevent.iszmumu = event.iszmumu
    cloneevent.VBFJ1Pt = event.VBFJ1Pt
    cloneevent.ZEEPt = event.ZEEPt
    cloneevent.VBFJ2ChFraction = event.VBFJ2ChFraction
    cloneevent.HEEJJEnergy = event.HEEJJEnergy
    cloneevent.J1Phi = event.J1Phi
    cloneevent.E2Charge = event.E2Charge
    cloneevent.HEEJJClassifier = event.HEEJJClassifier
    cloneevent.VBFJ2Energy = event.VBFJ2Energy
    cloneevent.J2Mass = event.J2Mass
    cloneevent.VBFJ1Energy = event.VBFJ1Energy
    cloneevent.J1Pt = event.J1Pt
    cloneevent.VBFJ2PFraction = event.VBFJ2PFraction
    cloneevent.HEEJJEta = event.HEEJJEta
    cloneevent.E2Energy = event.E2Energy
    cloneevent.E2Phi = event.E2Phi
    cloneevent.HEEJJphistarZl1 = event.HEEJJphistarZl1
    cloneevent.HEEJJphistarZl2 = event.HEEJJphistarZl2
    cloneevent.E2Pt = event.E2Pt
    cloneevent.HEEJJMass = event.HEEJJMass
    cloneevent.HEEJJmassVBF = event.HEEJJmassVBF
    cloneevent.VBFJ1Ntrk = event.VBFJ1Ntrk
    cloneevent.J2Pt = event.J2Pt
    cloneevent.HMMJJEta = event.HMMJJEta
    cloneevent.J2EFraction = event.J2EFraction
    cloneevent.ZMMPhi = event.ZMMPhi
    cloneevent.ZJJMass = event.ZJJMass
    cloneevent.VBFJ1PFraction = event.VBFJ1PFraction
    cloneevent.HMMJJmassVBF = event.HMMJJmassVBF
    cloneevent.ZMMEnergy = event.ZMMEnergy
    cloneevent.M2Eta = event.M2Eta
    cloneevent.VBFJ2EFraction = event.VBFJ2EFraction
    cloneevent.ZJJCharge = event.ZJJCharge
    cloneevent.HEEJJDeltaPhiZ = event.HEEJJDeltaPhiZ
    cloneevent.HEEJJDeltaPhiZJ2 = event.HEEJJDeltaPhiZJ2
    cloneevent.M1Phi = event.M1Phi
    cloneevent.J2ChFraction = event.J2ChFraction
    cloneevent.VBFJ2Mass = event.VBFJ2Mass
    cloneevent.VBFJ1btag = event.VBFJ1btag
    cloneevent.HMMJJdphiVBF = event.HMMJJdphiVBF
    cloneevent.J1Mass = event.J1Mass
    cloneevent.VBFJ1ChFraction = event.VBFJ1ChFraction
    cloneevent.ZEEEta = event.ZEEEta
    cloneevent.HEEJJPt = event.HEEJJPt
    cloneevent.HMMJJSumAbsEtaJ1J2 = event.HMMJJSumAbsEtaJ1J2
    cloneevent.HMMJJPhi = event.HMMJJPhi
    cloneevent.HEEJJSumAbsEtaJ1J2 = event.HEEJJSumAbsEtaJ1J2
    cloneevent.M1Energy = event.M1Energy
    cloneevent.J2Energy = event.J2Energy
    cloneevent.J1NHFraction = event.J1NHFraction
    cloneevent.J1Energy = event.J1Energy
    cloneevent.HMMJJEnergy = event.HMMJJEnergy
    cloneevent.nvertices = event.nvertices
    cloneevent.HMMJJDeltaPhiZ = event.HMMJJDeltaPhiZ
    cloneevent.M2Pt = event.M2Pt
    cloneevent.J1btag = event.J1btag
    cloneevent.HEEJJhelphiZl2 = event.HEEJJhelphiZl2
    cloneevent.E2Eta = event.E2Eta
    cloneevent.HEEJJhelphiZl1 = event.HEEJJhelphiZl1
    cloneevent.M1Pt = event.M1Pt
    cloneevent.ZEEEnergy = event.ZEEEnergy
    cloneevent.E1Energy = event.E1Energy
    cloneevent.J1PFraction = event.J1PFraction
    cloneevent.HMMJJDeltaPhiZJ2 = event.HMMJJDeltaPhiZJ2
    cloneevent.HMMJJDeltaPhiZJ1 = event.HMMJJDeltaPhiZJ1
    cloneevent.HMMJJphistarZl1 = event.HMMJJphistarZl1
    cloneevent.HMMJJphistarZl2 = event.HMMJJphistarZl2
    cloneevent.HMMJJhelphiZl2 = event.HMMJJhelphiZl2
    cloneevent.ZEECharge = event.ZEECharge
    cloneevent.HMMJJhelphiZl1 = event.HMMJJhelphiZl1
    cloneevent.VBFJ1Mass = event.VBFJ1Mass
    cloneevent.ZJJPhi = event.ZJJPhi
    cloneevent.VBFJ1Phi = event.VBFJ1Phi
    cloneevent.HEEJJhelphi = event.HEEJJhelphi
    cloneevent.HMMJJhelcosthetaZl2 = event.HMMJJhelcosthetaZl2
    cloneevent.HMMJJhelcosthetaZl1 = event.HMMJJhelcosthetaZl1
    #cloneevent.E1Et = event.E1Et

    return cloneevent 


  def applyJES(self, event, up):
    cloneevent = self.cloneEvent(event)
    #for branch in event.GetListOfBranches():
    #  print branch.GetName()
      #cloneevent.eval(branch.GetName()) = event.eval(branch.GetName())
    #sys.exit(1) 
    #print event.ZJJMass
    uncj1 = self.jes.uncertainty(event.J1Pt, event.J1Eta) 
    uncj2 = self.jes.uncertainty(event.J2Pt, event.J2Eta) 
    uncvbfj1 = self.jes.uncertainty(event.VBFJ1Pt, event.VBFJ1Eta) 
    uncvbfj2 = self.jes.uncertainty(event.VBFJ2Pt, event.VBFJ2Eta) 
    j1 = [event.J1Pt*cos(event.J1Phi), 
          event.J1Pt*sin(event.J1Phi), 
          event.J1Pt/tan(2*atan(exp(-1*event.J1Eta))),
          sqrt(event.J1Pt*event.J1Pt*(1+1/(tan(2*atan(exp(-1*event.J1Eta)))*tan(2*atan(exp(-1*event.J1Eta))))))]

    j2 = [event.J2Pt*cos(event.J2Phi), 
          event.J2Pt*sin(event.J2Phi),
          event.J2Pt/tan(2*atan(exp(-1*event.J2Eta))),
          sqrt(event.J2Pt*event.J2Pt*(1+1/(tan(2*atan(exp(-1*event.J2Eta)))*tan(2*atan(exp(-1*event.J2Eta))))))]

    vbfj1 = [event.VBFJ1Pt*cos(event.VBFJ1Phi),
          event.VBFJ1Pt*sin(event.VBFJ1Phi),
          event.VBFJ1Pt/tan(2*atan(exp(-1*event.VBFJ1Eta))),
          sqrt(event.VBFJ1Pt*event.VBFJ1Pt*(1+1/(tan(2*atan(exp(-1*event.VBFJ1Eta)))*tan(2*atan(exp(-1*event.VBFJ1Eta))))))]       

    vbfj2 = [event.VBFJ2Pt*cos(event.VBFJ2Phi),
          event.VBFJ2Pt*sin(event.VBFJ2Phi),
          event.VBFJ2Pt/tan(2*atan(exp(-1*event.VBFJ2Eta))),
          sqrt(event.VBFJ2Pt*event.VBFJ2Pt*(1+1/(tan(2*atan(exp(-1*event.VBFJ2Eta)))*tan(2*atan(exp(-1*event.VBFJ2Eta))))))]

    if up: 
      cloneevent.J1Pt = event.J1Pt+uncj1*event.J1Pt
      cloneevent.J2Pt = event.J2Pt+uncj2*event.J2Pt
      cloneevent.VBFJ1Pt = event.VBFJ1Pt+uncvbfj1*event.VBFJ1Pt
      cloneevent.VBFJ2Pt = event.VBFJ2Pt+uncvbfj2*event.VBFJ2Pt
    
      for i in range(4):
        j1[i] = j1[i]+uncj1*j1[i]
        j2[i] = j2[i]+uncj2*j2[i]
        vbfj1[i] = vbfj1[i]+uncvbfj1*vbfj1[i]
        vbfj2[i] = vbfj2[i]+uncvbfj2*vbfj2[i]  

    else:
      cloneevent.J1Pt = event.J1Pt-uncj1*event.J1Pt
      cloneevent.J2Pt = event.J2Pt-uncj2*event.J2Pt
      cloneevent.VBFJ1Pt = event.VBFJ1Pt-uncvbfj1*event.VBFJ1Pt
      cloneevent.VBFJ2Pt = event.VBFJ2Pt-uncvbfj2*event.VBFJ2Pt 

      for i in range(4):
        j1[i] = j1[i]-uncj1*j1[i]
        j2[i] = j2[i]-uncj2*j2[i]
        vbfj1[i] = vbfj1[i]-uncvbfj1*vbfj1[i]
        vbfj2[i] = vbfj2[i]-uncvbfj2*vbfj2[i]

    jsum = [j1[0]+j2[0], j1[1]+j2[1], j1[2]+j2[2], j1[3]+j2[3]]
    vbfjsum = [vbfj1[0]+vbfj2[0], vbfj1[1]+vbfj2[1], vbfj1[2]+vbfj2[2], vbfj1[3]+vbfj2[3]]
    modmass = sqrt(max(jsum[3]*jsum[3] - jsum[0]*jsum[0] - jsum[1]*jsum[1] - jsum[2]*jsum[2], 0.) )
    modmassvbf = sqrt(max(vbfjsum[3]*vbfjsum[3] - vbfjsum[0]*vbfjsum[0] - vbfjsum[1]*vbfjsum[1] - vbfjsum[2]*vbfjsum[2], 0.) )
    #print "orig mass", event.ZJJMass, "modmass", modmass
    cloneevent.ZJJMass = modmass
    cloneevent.VBFMass = modmassvbf

    #print event.ZMMMass

    return cloneevent


#if __name__=="__main__":
#  sv=SystematicVariation(False) 
#  print "JES test (40, 0)", sv.getJES(40., 0.)
#  print "JES test (40, 1)", sv.getJES(40., 1.)
#  print "JES test (40, 2)", sv.getJES(40., 2.)
#  print "JES test (40, 3)", sv.getJES(40., 3.)
#  print "JES test (40, 4)", sv.getJES(40., 4.)
#  print "JES test (40, 4.7)", sv.getJES(40., 4.7)
#  print "JES test (40, 5)", sv.getJES(40., 5.)
  
  
