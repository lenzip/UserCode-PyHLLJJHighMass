import CMGTools.RootTools.fwlite.Config as cfg
from HiggsAna.PyHLLJJHighMass.analhjjll_cff import *
hjjllAna.matchgen=False
hjjllAna.jetptmin = 30.
hjjllAna.minjets = 4.

DY50 = cfg.MCComponent(
    name = 'DY50',
    files = [
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_0.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_13.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_14.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_15.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_16.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_18.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_19.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_2.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_20.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_21.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_23.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_24.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_25.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_27.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_28.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_29.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_3.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_30.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_31.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_32.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_34.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_37.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_4.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_40.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_41.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_42.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_43.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_5.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_6.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_7.root',
'root://eoscms//eos/cms/store/user/lenzip/CMG/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/CMGV6/cmgTuple_9.root'    
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
