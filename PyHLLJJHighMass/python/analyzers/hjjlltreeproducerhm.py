from CMGTools.RootTools.analyzers.TreeAnalyzer import TreeAnalyzer
import math
from CMGTools.RootTools.utils.DeltaR import deltaR, deltaPhi

class hjjlltreeproducerhm( TreeAnalyzer ):
    '''Tree producer for the HZ, H->tt  analysis.'''

    def declareVariables(self):

        def var( varName ):
            self.tree.addVar('float', varName)

        def genparticleVars( pName ):
            var('g_{pName}Mass'.format(pName=pName))
            var('g_{pName}Pt'.format(pName=pName))
            var('g_{pName}Energy'.format(pName=pName))
            var('g_{pName}Eta'.format(pName=pName))
            var('g_{pName}Phi'.format(pName=pName))

        def jetVars( pName ):
            var('{pName}Mass'.format(pName=pName))
            var('{pName}Pt'.format(pName=pName))
            var('{pName}Energy'.format(pName=pName))
            var('{pName}Eta'.format(pName=pName))
            var('{pName}Phi'.format(pName=pName))
            var('{pName}Ntrk'.format(pName=pName))
            var('{pName}ChFraction'.format(pName=pName))
            var('{pName}PFraction'.format(pName=pName))
            var('{pName}EFraction'.format(pName=pName))
            var('{pName}NHFraction'.format(pName=pName))
            var('{pName}btag'.format(pName=pName))
        
        def particleVars( pName ):
            var('{pName}Mass'.format(pName=pName))
            var('{pName}Pt'.format(pName=pName))
            var('{pName}Energy'.format(pName=pName))
            var('{pName}Eta'.format(pName=pName))
            var('{pName}Phi'.format(pName=pName))
            var('{pName}Charge'.format(pName=pName))

        def higgsVars( pName ):
            var('{pName}Mass'.format(pName=pName))
            var('{pName}Pt'.format(pName=pName))
            var('{pName}Energy'.format(pName=pName))
            var('{pName}Eta'.format(pName=pName))
            var('{pName}Phi'.format(pName=pName))
            var('{pName}costhetastar'.format(pName=pName))
            var('{pName}DeltaPtZ'.format(pName=pName))
            var('{pName}DeltaPhiZ'.format(pName=pName))
            var('{pName}DeltaPhiZJ1'.format(pName=pName))
            var('{pName}DeltaPhiZJ2'.format(pName=pName))
            var('{pName}SumAbsEtaJ1J2'.format(pName=pName))
            var('{pName}helphi'.format(pName=pName))
            var('{pName}helphiZl1'.format(pName=pName))
            var('{pName}helphiZl2'.format(pName=pName))
            var('{pName}helcosthetaZl1'.format(pName=pName))
            var('{pName}helcosthetaZl2'.format(pName=pName))
            var('{pName}phistarZl1'.format(pName=pName))
            var('{pName}phistarZl2'.format(pName=pName))
            var('{pName}detaVBF'.format(pName=pName))
            var('{pName}dphiVBF'.format(pName=pName))
            var('{pName}massVBF'.format(pName=pName))     
            var('{pName}Classifier'.format(pName=pName))
            var('{pName}LD'.format(pName=pName))
                        
            
        #jetVars('j1rec')
        #jetVars('j2rec')
        #jetVars('j3rec')
        #jetVars('j4rec')
        jetVars('J1')
        jetVars('J2')
        jetVars('VBFJ1')
        jetVars('VBFJ2')
        
        particleVars('M1')
        particleVars('M2')
        
        particleVars('ZEE')
        particleVars('ZMM')
        particleVars('ZJJ')


        particleVars('E1')
        particleVars('E2')

        higgsVars('HEEJJ')
        higgsVars('HMMJJ')


        #particleVars('mu1rec')
        #particleVars('mu2rec')
        #particleVars('e1rec')
        #particleVars('e2rec')

        #particleVars('hmumujj')
        #particleVars('hmumu')
        #particleVars('hjj')

        #particleVars('heejj')
        #particleVars('hee')
        #particleVars('mumu')
        #particleVars('ee')
        #particleVars('jj')

        #particleVars('trueZhad')

        #particleVars('hmumujjrefit')

        var('step')
        var('njets')
        var('iszee')
        var('iszmumu')
        var('truezlepmass')
        var('isDecayMatched')
        var('isVBFMatched')
        
        var('weight')

        #var('deltaeta')
        #var('cosdeltaphi')
        #var('cosdeltaphigen')
        #var('mjj')
        #var('dimuonmass')
        #var('dielectronmass')
        #var('dimuonTrigger')
        #var('dielectronTrigger')
        #var('minDeltaPhiLJ')
        var('nvertices')
        
        self.tree.book()


    def process(self, iEvent, event):

        def fill( varName, value ):
            setattr( self.tree.s, varName, value )

        def fJetVars( pName, particle ):
            fill('{pName}Mass'.format(pName=pName), particle.mass() )
            fill('{pName}Pt'.format(pName=pName), particle.pt() )
            fill('{pName}Energy'.format(pName=pName), particle.energy() )
            fill('{pName}Ntrk'.format(pName=pName), particle.component(1).number() + particle.component(2).number() + particle.component(3).number())
            fill('{pName}ChFraction'.format(pName=pName), particle.component(1).fraction() + particle.component(2).fraction() + particle.component(3).fraction())
            fill('{pName}EFraction'.format(pName=pName), particle.component(2).fraction() )
            fill('{pName}PFraction'.format(pName=pName), particle.component(4).fraction() )
            fill('{pName}NHFraction'.format(pName=pName), particle.component(5).fraction() )
            fill('{pName}Eta'.format(pName=pName), particle.eta() )
            fill('{pName}btag'.format(pName=pName), particle.btag(7))
#
        def fParticleVars( pName, particle ):
            fill('{pName}Mass'.format(pName=pName), particle.mass() )
            fill('{pName}Pt'.format(pName=pName), particle.pt() )
            fill('{pName}Energy'.format(pName=pName), particle.energy() )
            fill('{pName}Eta'.format(pName=pName), particle.eta() )
            fill('{pName}Phi'.format(pName=pName), particle.phi() )
            #fill('{pName}Charge'.format(pName=pName), particle.charge() )

        def fgenParticleVars( pName, particle ):
            fill('g_{pName}Mass'.format(pName=pName), particle.mass() )
            fill('g_{pName}Pt'.format(pName=pName), particle.pt() )
            fill('g_{pName}Energy'.format(pName=pName), particle.energy() )
            fill('g_{pName}Eta'.format(pName=pName), particle.eta() )

        def fHiggsVars( pName, particle, classifierValue ):
            fill('{pName}Mass'.format(pName=pName),particle.mass())
            fill('{pName}Pt'.format(pName=pName),particle.pt())
            fill('{pName}Energy'.format(pName=pName),particle.energy())
            fill('{pName}Eta'.format(pName=pName),particle.eta())
            fill('{pName}Phi'.format(pName=pName),particle.phi())
            fill('{pName}DeltaPtZ'.format(pName=pName),abs(particle.leg1().pt() - particle.leg2().pt()))
            fill('{pName}DeltaPhiZ'.format(pName=pName),deltaPhi(particle.leg1().phi(), particle.leg2().phi()))
            fill('{pName}DeltaPhiZJ1'.format(pName=pName),deltaPhi(particle.leg1().phi(), particle.leg2().leg1().phi()))
            fill('{pName}DeltaPhiZJ2'.format(pName=pName),deltaPhi(particle.leg1().phi(), particle.leg2().leg2().phi()))
            fill('{pName}SumAbsEtaJ1J2'.format(pName=pName),abs(particle.leg2().leg1().eta())+abs(particle.leg2().leg2().eta()))
            fill('{pName}costhetastar'.format(pName=pName),particle.costhetastar())
            fill('{pName}helphi'.format(pName=pName),particle.helphi())
            fill('{pName}helphiZl1'.format(pName=pName), particle.helphiZl1())
            fill('{pName}helphiZl2'.format(pName=pName), particle.helphiZl2())
            fill('{pName}helcosthetaZl1'.format(pName=pName), particle.helcosthetaZl1())
            fill('{pName}helcosthetaZl2'.format(pName=pName), particle.helcosthetaZl2())
            fill('{pName}phistarZl1'.format(pName=pName), particle.phistarZl1())
            fill('{pName}phistarZl2'.format(pName=pName), particle.phistarZl2())
            if particle.vbfptr().isNonnull():
              fill('{pName}detaVBF'.format(pName=pName), abs(particle.vbfptr().leg1().eta()-particle.vbfptr().leg2().eta()))
              fill('{pName}dphiVBF'.format(pName=pName), deltaPhi(particle.vbfptr().leg1().phi(), particle.vbfptr().leg2().phi()))
              fill('{pName}massVBF'.format(pName=pName), particle.vbfptr().mass())     
              #
            fill('{pName}Classifier'.format(pName=pName), classifierValue)
            fill('{pName}LD'.format(pName=pName), particle.LD)
                       
        subevent = getattr( event, self.cfg_ana.anaName )
        fill('step',subevent.step)
        #fill('iszee',subevent.iszee)
        #fill('iszmumu',subevent.iszmumu)
        #fill('truezlepmass',subevent.truezlepmass)
        fill('weight',subevent.myweight)
        fill('nvertices',subevent.nvertices)
        fill('njets',len(subevent.highptjets))
        #fill('dimuonTrigger', subevent.dimuonTrigger)
        #fill('dielectronTrigger', subevent.dielectronTrigger)
        #fill('dimuonHtTrigger', subevent.dimuonHtTrigger)
        #fill('dielectronHtTrigger', subevent.dielectronHtTrigger)
        #fill('ht', subevent.ht)

        #if len(subevent.highptjets)>0:
        #  fJetVars('j1rec', subevent.highptjets[0])
        #if len(subevent.highptjets)>1:
        #  fJetVars('j2rec', subevent.highptjets[1])
        #if len(subevent.highptjets)>2:
        #  fJetVars('j3rec', subevent.highptjets[2])
        #if len(subevent.highptjets)>3:  
        #  fJetVars('j4rec', subevent.highptjets[3])  
#        fill('cosdeltaphigen',math.cos(subevent.genVBFdeltaPhi))
#        fill('njets',len(subevent.highptjets))
#        fill('dimuonTrigger', subevent.dimuonTrigger)
#        fill('dielectronTrigger', subevent.dielectronTrigger)

       # if (len(subevent.truezhad)):
       #   fParticleVars('trueZhad', subevent.truezhad[0])

        #if len(subevent.highptelectrons) > 0:
        #  fParticleVars('e1rec', subevent.highptelectrons[0])
        #if len(subevent.highptelectrons) > 1:
        #  fParticleVars('e2rec', subevent.highptelectrons[1])

        #if len(subevent.highptmuons) > 0:
        #  fParticleVars('mu1rec', subevent.highptmuons[0])
        #if len(subevent.highptmuons) > 1:
        #  fParticleVars('mu2rec', subevent.highptmuons[1])   

        #if (subevent.step >= 6):
        #  fill('deltaeta', subevent.deltaeta)
        #  fill('mjj', subevent.mjj)
        #  if subevent.deltaphi > -99:
        #    fill('cosdeltaphi', math.cos(subevent.deltaphi))
        #if (subevent.step >= 3):
        #  fill('dimuonmass', subevent.dimuonmass)
        #  fill('dielectronmass', subevent.dielectronmass)

        #if len(subevent.dimuons) > 0:
        #  fParticleVars('mumu', subevent.dimuons[0])

        #if len(subevent.dielectrons) > 0:
        #  fParticleVars('ee', subevent.dielectrons[0])

        #if len(subevent.dijets) > 0:
        #  fParticleVars('jj', subevent.dijets[0])

        #if len(subevent.hbest) > 0:
        #  fParticleVars('hmumujjrefit', subevent.hbest[0])
        #  fill('minDeltaPhiLJ', subevent.deltaPhiLJ[0])
        #  fill('deltaPhiJJ', subevent.deltaPhiJJ)
        #  fill('deltaPhiZJ1', subevent.deltaPhiZJ1)
        #  fill('deltaPhiZJ2', subevent.deltaPhiZJ2)
        #  fill('minDeltaPhiZJ', subevent.deltaPhiZJ[0])
        #  fill('maxDeltaPhiZJ', subevent.deltaPhiZJ[1]) 

#        if (subevent.step >= 2):
#          fill('deltaeta', subevent.deltaeta)
#          fill('mjj', subevent.mjj)
#          if subevent.deltaphi > -99:
#            fill('cosdeltaphi', math.cos(subevent.deltaphi))
#        if (subevent.step >= 3):
#          fill('dimuonmass', subevent.dimuonmass)
#          fill('dielectronmass', subevent.dielectronmass)

#        if len(subevent.hmumujj) > 0:
#          fParticleVars('hmumujj', subevent.hmumujj[0])
#          fParticleVars('hmumu', subevent.mumu[0])
#          fParticleVars('hjj', subevent.jj[0])


#        if len(subevent.heejj) > 0:
#          fParticleVars('heejj', subevent.heejj[0])
#          fParticleVars('hee', subevent.ee[0])
#          fParticleVars('hjj', subevent.jj[0])  
        
#        if len(subevent.hbest) > 0:
#          fParticleVars('hmumujjrefit', subevent.hbest[0])
#          fill('minDeltaPhiLJ', subevent.deltaPhiLJ[0])
        if (len(subevent.hmumujj_withmatchinfo)>0):
          #vbfmaxdeta = 0.   
          #vbfmaxmass = 0.                   
          #for cand in subevent.hmumujj_withmatchinfo:
          #  #if(abs(cand[0].vbfptr().leg1().eta() - cand[0].vbfptr().leg2().eta()) ) > vbfmaxdeta:
          #  if(cand[0].vbfptr().mass()) > vbfmaxmass:  
          #    #vbfmaxdeta = abs(cand[0].vbfptr().leg1().eta() - cand[0].vbfptr().leg2().eta())   
          #    vbfmaxmass = cand[0].vbfptr().mass()
          goldenCandidate = subevent.hmumujj_withmatchinfo[0] #cand
          #print "Mu candidate. VBF max deltaEta: ", vbfmaxdeta
          #print "Mu candidate. VBF max mass: ", vbfmaxmass
          
        elif (len(subevent.heejj_withmatchinfo)>0):
          #vbfmaxdeta = 0.
          #vbfmaxmass = 0.
          #for cand in subevent.heejj_withmatchinfo:
          #  if(cand[0].vbfptr().mass()) > vbfmaxmass:
#         #   if(abs(cand[0].vbfptr().leg1().eta() - cand[0].vbfptr().leg2().eta()) ) > vbfmaxdeta:
#         #     vbfmaxdeta = abs(cand[0].vbfptr().leg1().eta() - cand[0].vbfptr().leg2().eta()) 
          #    vbfmaxmass = cand[0].vbfptr().mass()
          goldenCandidate = subevent.heejj_withmatchinfo[0]
          #print "Ele candidate. VBF max mass: ", vbfmaxmass
       
        if (len(subevent.hmumujj_withmatchinfo)>0):
          #goldenCandidate = subevent.hmumujj_withmatchinfo[0]
          fHiggsVars('HMMJJ', goldenCandidate, -1)
          #fill('isDecayMatched',goldenCandidate[1])
          #fill('isVBFMatched',goldenCandidate[2])
          fParticleVars('ZMM', goldenCandidate.leg1())
          fParticleVars('ZJJ', goldenCandidate.leg2())
          fParticleVars('M1', goldenCandidate.leg1().leg1())
          fParticleVars('M2', goldenCandidate.leg1().leg2())
          fParticleVars('J1', goldenCandidate.leg2().leg1())
          fParticleVars('J2', goldenCandidate.leg2().leg2())
          fJetVars('VBFJ1',goldenCandidate.vbfptr().leg1())
          fJetVars('VBFJ2',goldenCandidate.vbfptr().leg2())
        elif (len(subevent.heejj_withmatchinfo)>0):
          #goldenCandidate = subevent.heejj_withmatchinfo[0]
          fHiggsVars('HEEJJ', goldenCandidate, -1)
          #fill('isDecayMatched',goldenCandidate[1])
          #fill('isVBFMatched',goldenCandidate[2])
          fParticleVars('ZEE', goldenCandidate.leg1())
          fParticleVars('ZJJ', goldenCandidate.leg2())
          fParticleVars('E1', goldenCandidate.leg1().leg1())
          fParticleVars('E2', goldenCandidate.leg1().leg2())
          fParticleVars('J1', goldenCandidate.leg2().leg1())
          fParticleVars('J2', goldenCandidate.leg2().leg2()) 
          fJetVars('VBFJ1',goldenCandidate.vbfptr().leg1())
          fJetVars('VBFJ2',goldenCandidate.vbfptr().leg2())                  
                    
        self.tree.fill()
