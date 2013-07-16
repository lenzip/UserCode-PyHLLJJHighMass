from CMGTools.RootTools.analyzers.TreeAnalyzer import TreeAnalyzer
import math
from CMGTools.RootTools.utils.DeltaR import deltaR, deltaPhi
from ROOT import gSystem
gSystem.CompileMacro("TMVAClassification_BDT.class.C")
from ROOT import ReadBDT,vector

class hjjllcombinatorialhm ( TreeAnalyzer ):
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
            var('{pName}deltaEtaDecay'.format(pName=pName))
            var('{pName}deltaPhiDecay'.format(pName=pName))
            var('{pName}deltaRDecay'.format(pName=pName))
            var('{pName}btag1'.format(pName=pName))
            var('{pName}btag2'.format(pName=pName))
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
    
#        particleVars('jj')
#        particleVars('mumu')
#        higgsVars('jjmumu')
        #particleVars('jje')
#        var('step')
        var('isDecayMatched')
        var('isVBFMatched')
        var('eventNumber')
        var('weight')
        print "tree producer matchgen", self.cfg_ana.matchgen

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
            if particle.numberOfDaughters() > 1:
              fill('{pName}deltaEtaDecay'.format(pName=pName), abs(particle.daughter(0).eta() - particle.daughter(1).eta() ))
              fill('{pName}deltaPhiDecay'.format(pName=pName), deltaPhi(particle.daughter(0).phi(), particle.daughter(1).phi() ))
              fill('{pName}deltaRDecay'.format(pName=pName), deltaR(particle.daughter(0).eta(), 
                                                                    particle.daughter(0).phi(), 
                                                                    particle.daughter(1).eta(), 
                                                                    particle.daughter(1).phi() ))
              if (pName == 'jj'):                                                      
                fill('{pName}btag1'.format(pName=pName), particle.daughter(0).btag(7)) 
                fill('{pName}btag2'.format(pName=pName), particle.daughter(1).btag(7))                                                       

        def fHiggsVars( pName, particle , classifierValue):
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
            fill('{pName}Classifier'.format(pName=pName), classifierValue)


        def fgenParticleVars( pName, particle ):
            fill('g_{pName}Mass'.format(pName=pName), particle.mass() )
            fill('g_{pName}Pt'.format(pName=pName), particle.pt() )
            fill('g_{pName}Energy'.format(pName=pName), particle.energy() )
            fill('g_{pName}Eta'.format(pName=pName), particle.eta() )
#
        subevent = getattr( event, self.cfg_ana.anaName )
       
        
        #print "number of matched candidates  ",len(subevent.hmumujj_mcmatch)
        #print "number of unmatched candidates",len(subevent.hmumujj_nomcmatch)
        #for cand in subevent.hmumujj_mcmatch:
        first=True
        for cand in subevent.hmumujj_withmatchinfo:
          fill('step',subevent.step)
          fill('eventNumber', subevent.iEv) 
          fill('weight', subevent.myweight)
          if self.cfg_ana.matchgen:
            fill('isDecayMatched',cand[1])
            fill('isVBFMatched',cand[2])
          else:
            fill('isDecayMatched',first)
            fill('isVBFMatched',first)
          fParticleVars('ZJJ',cand[0].leg2())
          fParticleVars('ZMM',cand[0].leg1())
          fJetVars('J1',cand[0].leg2().leg1())
          fJetVars('J2',cand[0].leg2().leg2())
          fParticleVars('M1',cand[0].leg1().leg1())
          fParticleVars('M2',cand[0].leg1().leg2())
          fHiggsVars('HMMJJ',cand[0], cand[3])
          fJetVars('VBFJ1',cand[0].vbfptr().leg1())
          fJetVars('VBFJ2',cand[0].vbfptr().leg2())
          first=False
          self.tree.fill()
          #to clear all variables
          self.tree.reinit()


        first=True
        for cand in subevent.heejj_withmatchinfo:
          fill('step',subevent.step)
          fill('eventNumber', subevent.iEv) 
          fill('weight', subevent.myweight)
          if self.cfg_ana.matchgen:
            fill('isDecayMatched',cand[1])
            fill('isVBFMatched',cand[2])
          else:
            fill('isDecayMatched',first)
            fill('isVBFMatched',first)
          fParticleVars('ZJJ',cand[0].leg2())
          fParticleVars('ZEE',cand[0].leg1())
          fJetVars('J1',cand[0].leg2().leg1())
          fJetVars('J2',cand[0].leg2().leg2())
          fParticleVars('E1',cand[0].leg1().leg1())
          fParticleVars('E2',cand[0].leg1().leg2())
          fJetVars('VBFJ1',cand[0].vbfptr().leg1())
          fJetVars('VBFJ2',cand[0].vbfptr().leg2())
          fHiggsVars('HEEJJ',cand[0], cand[3])
          first=False
          self.tree.fill()
          self.tree.reinit()

