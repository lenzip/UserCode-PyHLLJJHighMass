import CMGTools.RootTools.fwlite.Config as cfg
from HiggsAna.PyHLLJJHighMass.analhjjll_cff import *
#hjjllAna.matchgen=False

VBFH500 = cfg.MCComponent(
    name = 'VBFH500',
    files = [
#125    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_0.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_1.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_2.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_3.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_4.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_5.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_6.root',    
'root://eoscms//eos/cms/store/user/lenzip/CMG/VBF_HToZZTo2L2Q_M-500_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV7/cmgTuple_newId_vbf_7.root',    
#  'file:cmgTuple.root'
    ],
    
    xSection = 0.00114477 * 11050000, 
    nGenEvents = 6972564, # dummy 
    triggers = [],
    intLumi = 1000,
    effCorrFactor = 1 )

selectedComponents = [VBFH500]

VBFH500.splitFactor = 1
    
config = cfg.Config( components = selectedComponents,
                     sequence = sequence )
