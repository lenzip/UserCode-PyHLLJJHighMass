import CMGTools.RootTools.fwlite.Config as cfg
from HiggsAna.PyHLLJJHighMass.analhjjll_cff import *
hjjllAna.matchgen=False
hjjllAna.jetptmin = 30.
hjjllAna.minjets = 4.

DY50 = cfg.MCComponent(
    name = 'DY50',
    files = [
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_0.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_10.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_11.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_12.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_133.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_14.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_152.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_163.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_2.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_209.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_42.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_58.root',
'root://eoscms//eos/cms/store/user/tropiano/CMG/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_65.root'    
    ],
    
    xSection = 0.00114477 * 11050000, 
    nGenEvents = 6972564, # dummy 
    triggers = [],
    intLumi = 1000,
    effCorrFactor = 1 )

selectedComponents = [DY50]

DY50.splitFactor = 1
    
config = cfg.Config( components = selectedComponents,
                     sequence = sequence )
