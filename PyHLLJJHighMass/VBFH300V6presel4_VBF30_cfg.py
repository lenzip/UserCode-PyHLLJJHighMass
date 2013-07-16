import CMGTools.RootTools.fwlite.Config as cfg
from HiggsAna.PyHLLJJHighMass.analhjjll_cff import *
#hjjllAna.matchgen=False
hjjllAna.jetptmin = 30.
hjjllAna.minjets = 4.

VBFH300 = cfg.MCComponent(
    name = 'VBFH300',
    files = [
#125    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_0.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_1.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_2.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_3.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_4.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_5.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_6.root',    
#  'file:cmgTuple.root'
    ],
    
    xSection = 0.00114477 * 11050000, 
    nGenEvents = 6972564, # dummy 
    triggers = [],
    intLumi = 1000,
    effCorrFactor = 1 )

selectedComponents = [VBFH300]

VBFH300.splitFactor = 1
    
config = cfg.Config( components = selectedComponents,
                     sequence = sequence )
