#!/usr/bin/env python
import os
import gzip

sel_ele = 0
sel_mu  = 0
sel_tot = 0
total = 0
error   = 0
for root, dirs, files in os.walk('../PyHLLJJ/VBF_HToZZTo2L2Q_M-300_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM_1364480195'):
#for root, dirs, files in os.walk('DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM_1363714531'):
#for root, dirs, files in os.walk('DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM_1363713334'):
#for root, dirs, files in os.walk('VBF_HToZZTo2L2Q_M-125_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM_1363692951'):
    for name in files:
        filename = os.path.join(root, name)
        
 #       print filename
        if filename.endswith("STDOUT.gz"):
            f = gzip.open(filename, 'r')
            goodlines_ele = []
            goodlines_mu = []
            goodlines_weights = []
                        
            for line in f:
                if 'weights' in line and 'TrigReport' in line:
                    goodlines_weights.append(line)
                if "preselEle" in line and 'TrigReport' in line:
                    goodlines_ele.append(line) 
                    #words = goodlines[0].split()
                    #for word in words:
                elif "preselMu" in line and 'TrigReport' in line:
                    goodlines_mu.append(line)
                elif "FatalSystemSignal" in line:
                    error += 1
                    print "error in file: ", filename
                                                            
            if len(goodlines_ele) and len(goodlines_mu) and len(goodlines_weights):        
                words_ele = goodlines_ele[0].split()
                words_mu  = goodlines_mu[0].split()
                words_total = goodlines_weights[0].split()
                         
#            print words[4]
            sel_ele = sel_ele + int(words_ele[4])
            sel_mu  = sel_mu  + int(words_mu[4])
            total = total + int(words_total[4])
                        
#    print "sel_ele", sel_ele

print "sel_ele ", sel_ele    
print "sel_mu  ", sel_mu
print "sel_tot ", sel_ele + sel_mu
print "total_run ", total
print "eff",float(sel_ele + sel_mu)/float(total)
