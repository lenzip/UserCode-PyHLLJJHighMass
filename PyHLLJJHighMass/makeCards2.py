#! /usr/bin/env python

import os, sys, logging, re
import getopt
import string
import threading, Queue
import subprocess
import urllib2
import numpy
from optparse import OptionParser, Option
from stat import *
from ROOT import * 

#linkexpectednevents="http://lenzip.web.cern.ch/lenzip/H2l2q/20130528/sel_"
#linkexpectednevents="http://lenzip.web.cern.ch/lenzip/H2l2q/20130528/plots/"
linkexpectednevents="http://lenzip.web.cern.ch/lenzip/H2l2q/20130528/selcut_300To600"
xsecgg="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-ggH.txt?revision=1.4&view=markup"
xsecvbf="http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/xs/8TeV/8TeV-vbfH.txt?revision=1.7&view=markup"
xsecdy=[3503.71, 152, -152.] 

def getNexpected(mass, JES):

  #file=urllib2.urlopen(linkexpectednevents+"index.html")
  #file=urllib2.urlopen(linkexpectednevents+str(mass)+JES+"/index.html")
  file=urllib2.urlopen(linkexpectednevents+JES+"/index.html")
  def getN(string, position):
    split = string.split()
    res = split[position].rstrip("</CENTER>")
    ressplit = res.split("+")
    return ressplit
  
  def getlumiweight(string, position):
    split = string.split()
    return split[position].rstrip("</CENTER>")
    

  expected={}
  mcstat={}
  #errors={}

  for line in file:
    #print line.split()
    if "VBF"+str(mass) in line and "HMM" in line:
      res = getN(line,8)
      expected["VBFMM"] = res[0]
      lw = getlumiweight(line,16)
      mcstat["VBFMM"] = [str(int(float(expected["VBFMM"])/float(lw))), lw]
      #errors["VBFMM"] = res[1]
      print "VBF MM",getN(line,8)
    elif "VBF"+str(mass) in line and "HEE" in line:
      res = getN(line,8)
      expected["VBFEE"] = res[0]
      lw = getlumiweight(line,16)
      print lw
      mcstat["VBFEE"] = [str(int(float(expected["VBFEE"])/float(lw))), lw]
      #errors["VBFEE"] = res[1]
      print "VBF EE",getN(line,8)
    elif "GG"+str(mass) in line and "HMM" in line :
      res = getN(line,8)
      expected["GGMM"] = res[0]
      lw = getlumiweight(line,16)
      mcstat["GGMM"] = [str(int(float(expected["GGMM"])/float(lw))), lw]
      #errors["GGMM"] = res[1]
      print "gg MM",getN(line,8)
    elif "GG"+str(mass) in line and "HEE" in line:
      res = getN(line,8)
      expected["GGEE"] = res[0]
      lw = getlumiweight(line,16)
      mcstat["GGEE"] = [str(int(float(expected["GGEE"])/float(lw))), lw]
      #errors["GGEE"] = res[1]
      print "gg EE",getN(line,8)
    elif "DY50_1" in line and str(mass) in line and "HMM" in line :
      res = getN(line,9)
      expected["DY50MM_1"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50MM_1"] = [str(int(float(expected["DY50MM_1"])/float(lw))), lw]
      #errors["BKGMM"] = res[1]
      print "DY50_1 MM",getN(line,9)
    elif "DY50_2" in line and str(mass) in line and "HMM" in line :
      res = getN(line,9)
      expected["DY50MM_2"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50MM_2"] = [str(int(float(expected["DY50MM_2"])/float(lw))), lw]
      #errors["BKGMM"] = res[1]
      print "DY50_2 MM",getN(line,9)   
    elif "DY50_3" in line and str(mass) in line and "HMM" in line :
      res = getN(line,9)
      expected["DY50MM_3"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50MM_3"] = [str(int(float(expected["DY50MM_3"])/float(lw))), lw]
      #errors["BKGMM"] = res[1]
      print "DY50_3 MM",getN(line,9)  
    elif "DY50_4" in line and str(mass) in line and "HMM" in line :
      res = getN(line,9)
      expected["DY50MM_4"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50MM_4"] = [str(int(float(expected["DY50MM_4"])/float(lw))), lw]
      #errors["BKGMM"] = res[1]
      print "DY50_4 MM",getN(line,9)
    elif "DY50_1" in line and str(mass) in line and "HEE" in line :
      res = getN(line,9)
      expected["DY50EE_1"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50EE_1"] = [str(int(float(expected["DY50EE_1"])/float(lw))), lw]
      #errors["BKGEE"] = res[1]
      print "DY50_1 EE",getN(line,9)
    elif "DY50_2" in line and str(mass) in line and "HEE" in line :
      res = getN(line,9) 
      expected["DY50EE_2"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50EE_2"] = [str(int(float(expected["DY50EE_2"])/float(lw))), lw]
      #errors["BKGEE"] = res[1]
      print "DY50_2 EE",getN(line,9)
    elif "DY50_3" in line and str(mass) in line and "HEE" in line :
      res = getN(line,9)
      expected["DY50EE_3"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50EE_3"] = [str(int(float(expected["DY50EE_3"])/float(lw))), lw]
      #errors["BKGEE"] = res[1]
      print "DY50_3 EE",getN(line,9)
    elif "DY50_4" in line and str(mass) in line and "HEE" in line :
      res = getN(line,9) 
      expected["DY50EE_4"] = res[0]
      lw = getlumiweight(line,17)
      mcstat["DY50EE_4"] = [str(int(float(expected["DY50EE_4"])/float(lw))), lw]
      #errors["BKGEE"] = res[1]
      print "DY50_4 EE",getN(line,9)
    else:
      continue
  return expected, mcstat#,errors

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


class CardBuilder:
  def __init__(self,mass, filename):
    self._mass=mass
    self._filename = filename
  
  def build(self):
    #expected, errors = getNexpected(mass)
    expected,mcstat = getNexpected(mass, "")
    expected_JU,mcstat_JU = getNexpected(mass, "_JESUP_JESUP")
    expected_JD,mcstat_JD = getNexpected(mass, "_JESDOWN_JESDOWN")
    errjesup  = {}
    errjesdown= {}
    jesstrings={} 
    for k,v in expected.iteritems():
      upiszero=False
      downiszero=False
      if v == expected_JU[k]:
        errjesup[k] = "1"
        upiszero = True  
      if v == expected_JD[k]:
        errjesdown[k] = "1"
        downiszero=True
      if upiszero and downiszero:  
        if errjesup[k]=="1" and errjesdown[k] == "1":
          jesstrings[k] = "-"
          continue
      errjesup[k] = float(expected_JU[k])/max(1e-6,float(v))
      #dirty
      if errjesup[k] > 10.:
        errjesup[k] = 10.
      errjesdown[k] = float(expected_JD[k])/max(1e-6,float(v))
      #dirty
      if errjesdown[k] < 1e-6:
        errjesdown[k] = 1e-6
      jesstrings[k] = str(errjesdown[k])+"/"+str(errjesup[k])

        
        
        

    #get cross sections
    xvbf = getXsec(mass, "vbf")
    xgg = getXsec(mass, "gg")

    infile = ''
    infile += "# Simple counting experiment, with one signal and 1 background processes\n"
    infile += "# Test version of the 20/fb H->ZZ->2l2q VBF analysis\n"
    infile += "imax 2  number of channels\n"
    infile += "jmax *  number of backgrounds\n"
    infile += "kmax *  number of nuisance parameters (sources of systematical uncertainties)\n"
    infile += "------------\n"
    infile += "# we have just one channel, in which we observe 0 events\n"
    infile += "#bin 1 2\n"
    infile += "#observation 0 0\n"
    infile += "------------\n"
    infile += "# now we list the expected events for signal and all backgrounds in that bin\n"
    infile += "# the second 'process' line must have a positive number for backgrounds, and 0 for signal\n"
    infile += "# then we list the independent sources of uncertainties, and give their effect (syst. error)\n"
    infile += "# on each process and bin\n"
    infile += "bin             EEJJ   EEJJ    EEJJ   EEJJ   EEJJ   EEJJ   MMJJ MMJJ  MMJJ   MMJJ   MMJJ   MMJJ \n"  
    infile += "process         ggH    vbfH   DY50_1 DY50_2 DY50_3 DY50_4  ggH  vbfH DY50_1 DY50_2 DY50_3 DY50_4\n"
    infile += "process         -1       0      1      2      3      4     -1    0     1      2      3      4\n"
    infile += "rate            %s      %s     %s     %s     %s     %s     %s    %s    %s     %s     %s     %s\n" %(expected["GGEE"], expected["VBFEE"], expected["DY50EE_1"], expected["DY50EE_2"], expected["DY50EE_3"], expected["DY50EE_4"], expected["GGMM"], expected["VBFMM"], expected["DY50MM_1"], expected["DY50MM_2"], expected["DY50MM_3"], expected["DY50MM_4"])
    infile += "------------\n"
    infile += "lumi     lnN    1.044    1.044   1.044    1.044   1.044   1.044  1.044    1.044   1.044    1.044   1.044   1.044 lumi affects both signal and background (mc-driven). \n"
    infile += "xs_ggH   lnN    %s       %s      -      -      -      -     %s       %s    -        -      -      - gg->H cross section + signal efficiency + other minor ones.\n" %(1+xgg[1]/xgg[0], 1+xvbf[1]/xvbf[0], 1+xgg[1]/xgg[0], 1+xvbf[1]/xvbf[0])
    infile += "DY50_norm lnN    -       -       %s      %s    %s     %s    -      -       %s      %s     %s      %s\n" %(1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0],1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0], 1+xsecdy[1]/xsecdy[0])
    infile += "DY50_1EEstat gmN %s -    -       %s      -     -      -     -      -       -       -       -      -\n" % ((mcstat["DY50EE_1"])[0], (mcstat["DY50EE_1"])[1])
    infile += "DY50_2EEstat gmN %s -    -       -      %s     -      -     -      -       -       -       -      -\n" % ((mcstat["DY50EE_2"])[0], (mcstat["DY50EE_2"])[1])
    infile += "DY50_3EEstat gmN %s -    -       -      -     %s      -     -      -       -       -       -      -\n" % ((mcstat["DY50EE_3"])[0], (mcstat["DY50EE_3"])[1])
    infile += "DY50_4EEstat gmN %s -    -       -      -     -      %s     -      -       -       -       -      -\n" % ((mcstat["DY50EE_4"])[0], (mcstat["DY50EE_4"])[1])
    infile += "DY50_1MMstat gmN %s -    -       -      -     -      -      -      -       %s      -       -      -\n" % ((mcstat["DY50MM_1"])[0], (mcstat["DY50MM_1"])[1])
    infile += "DY50_2MMstat gmN %s -    -       -      -     -      -      -      -       -       %s      -      -\n" % ((mcstat["DY50MM_2"])[0], (mcstat["DY50MM_2"])[1])
    infile += "DY50_3MMstat gmN %s -    -       -      -     -      -      -      -       -       -      %s      -\n" % ((mcstat["DY50MM_3"])[0], (mcstat["DY50MM_3"])[1])
    infile += "DY50_4MMstat gmN %s -    -       -      -     -      -      -      -       -       -       -     %s\n" % ((mcstat["DY50MM_4"])[0], (mcstat["DY50MM_4"])[1])
    
    infile += "GGEEstat gmN %s %s   -       -      -     -      -      -      -       -       -       -      -\n" % ((mcstat["GGEE"])[0], (mcstat["GGEE"])[1])
    infile += "VBFEEstat gmN %s -    %s      -      -     -      -      -      -       -       -       -      -\n" % ((mcstat["VBFEE"])[0], (mcstat["VBFEE"])[1])
    infile += "GGMMstat gmN %s -    -       -      -     -      -      %s     -       -       -       -      -\n" % ((mcstat["GGMM"])[0], (mcstat["GGMM"])[1])
    infile += "VBFMMstat gmN %s -    -       -      -     -      -      -     %s       -       -       -      -\n" % ((mcstat["VBFMM"])[0], (mcstat["VBFMM"])[1])

    infile += "JES   lnN    %s       %s      %s      %s      %s      %s     %s       %s    %s        %s     %s     %s JESuncertainty\n" \
            %(jesstrings["GGEE"], \
              jesstrings["VBFEE"], \
              jesstrings["DY50EE_1"], \
              jesstrings["DY50EE_2"], \
              jesstrings["DY50EE_3"], \
              jesstrings["DY50EE_4"], \
              jesstrings["GGMM"], \
              jesstrings["VBFMM"], \
              jesstrings["DY50MM_1"], \
              jesstrings["DY50MM_2"], \
              jesstrings["DY50MM_3"], \
              jesstrings["DY50MM_4"])
    f = open(self._filename, "w")
    f.write(infile)
    f.close()
    

class Worker(threading.Thread):
  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue
    self.status = -1
  def run(self):
    while True:
      try:
        command = self.queue.get()
        #print command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        self.status = process.returncode
        print 'task finished with exit code '+str(self.status)
        self.queue.task_done()
      except Queue.Empty, e:
        break
      except Exception, e:
        print "Error: %s" % str(e)


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



numcores = os.sysconf('SC_NPROCESSORS_ONLN')
if numcores is None:
  numcores = 1

usage  = "usage: %prog massstart massend stepsize [options]\n"

parser = OptionParser(usage=usage,option_class=ExtendedOption)
parser.add_option('-f', "--force", action="store_true", help="overwrite old results (default=False)", default=False)
parser.add_option('-c', "--cores", action="store", help="number of cores to use (default=%s)" %numcores, default=numcores)
parser.add_option("-n", '--negate', action="store_true", help="do nothing, just prepare the jobs", default=False)
parser.add_option("-r", '--run', action="store_true", help="run profile Likelihood", default=False)
parser.add_option("-p", '--plot', action="store_true", help="make the limit plot", default=False)


(options, args) = parser.parse_args()
if len(args)<3 :
  parser.print_help()
  sys.exit(1)

queue = Queue.Queue()

#start the workers
for i in range(int(options.cores)):
  worker = Worker(queue)
  worker.setDaemon(True)
  worker.start()

#fill the queue
#parser=ConfigParser(args[0])
#requests=parser.parse() 

for mass in range(int(args[0]), int(args[1])+int(args[2]), int(args[2])):

  filename = "datacard_m"+str(mass)+".dat"
  if os.path.exists(filename) and options.force is False:
    print 'file '+filename+' exists already, doing nothing.'
    print 'You can overwrite with the --force option'
    continue
  
  print "mass is", mass
  cb = CardBuilder(mass, filename)
  cb.build()

  if (options.run and not options.negate):
    command="combine -M ProfileLikelihood %s -m %s -t 100 &> log%s.txt" % (filename, str(mass), str(mass))
    #command="combine -M HybridNew --frequentist --testStat LHC %s -m %s -t 100 -H ProfileLikelihood &> log%s.txt" % (filename, str(mass), str(mass))
    print command
    queue.put(command)  
    
  
if not options.negate:
  queue.join()

if not options.plot:
  exit(0) 


def clsgetCLsFromFile(file):
  values = [0.,0.,0.,0.,0.]
  f = open(file, 'r')
  #if not f:
  #  return values

  for line in f:
    ls = line.split()
    #print ls
    if "median expected limit" in line:
      values[0] = float(ls[5])
    if "68% expected band" in line:
      values[1] = abs(float(ls[8]) - values[0])
      values[2] = abs(float(ls[4]) - values[0])
    if "95% expected band" in line:
      values[3] = abs(float(ls[8]) - values[0])
      values[4] = abs(float(ls[4]) - values[0])

  return values

gROOT.ProcessLine(".L ~/tdrStyle.C");
setTDRStyle()

masses = []
central = []
ex = []
err1p = []
err1m = []
err2p = []
err2m = []
for mass in range(int(args[0]), int(args[1])+int(args[2]), int(args[2])):
  masses.append(float(mass))
  values = clsgetCLsFromFile("log"+str(mass)+".txt")
  print values
  central.append(values[0])
  err1p.append(values[1])
  err1m.append(values[2])
  err2p.append(values[3])
  err2m.append(values[4])
  ex.append(0.)

x = numpy.array(masses)
y = numpy.array(central)
e1p = numpy.array(err1p)
e1m = numpy.array(err1m)
e2p = numpy.array(err2p)
e2m = numpy.array(err2m)
exx = numpy.array(ex)

graph1 = TGraphAsymmErrors(len(masses), x, y, exx, exx, e1m, e1p)
graph2 = TGraphAsymmErrors(len(masses), x, y, exx, exx, e2m, e2p)
graph3 = TGraphAsymmErrors(len(masses), x, y, exx, exx, exx, exx)
#graph1.SetLineWidth(2)
#graph2.SetLineWidth(2)
graph3.SetLineWidth(2)

graph1.SetFillColor(3)
graph2.SetFillColor(5)

canvas = TCanvas()
canvas.cd()


#graph2.Draw("a4")
graph2.Draw("a3")
graph2.GetXaxis().SetTitle("Mass [GeV]")
graph2.GetYaxis().SetTitle("#sigma/#sigma_{SM}")
#graph2.Draw("a4")
graph2.Draw("a3")
#graph1.Draw("4sames")
graph1.Draw("3sames")
#graph3.Draw("Csames")
graph3.Draw("Lsames")

canvas.SaveAs('limit.png')



  
