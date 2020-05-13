
from utils import *
#from Johan import *

class BeliefBase(object):
    def __init__(self):
        self.beliefBase = []  

    def CheckEntailment(self, formula, base = None):
        '''
        The priciple here is proof by refutation
        (A entail s) if and only if the sentence (A and not(s) ) is unsatisable
        '''
        ret = self.checkConsistancy("n("+ formula +")", base)
        if ret == True:
            return False
        else:     
            return True   

    def checkConsistancy(self, formula, base = None):
        '''
        check if the new formula consistant with exist belief base using truth table
        '''
        formula = eliminateIff(formula)
        formula = eliminateImply(formula)

        if base:
            bcopy = base.copy()
        else:
            bcopy = self.beliefBase.copy()
      
        bcopy.append(formula)

        boolean_list = regitrerBooleans(bcopy)
        #print(boolean_list )
        truth_table = np.asarray(createTruthTable(len(boolean_list)))
        beliefBase_translated = translateSentencesToSyntax(bcopy, boolean_list)
        updated_truth_table = addRuleColumns(truth_table, beliefBase_translated)
        np.savetxt('data.csv', updated_truth_table , delimiter=';',fmt='%d')

        return testForTrueKb(updated_truth_table) 

    def revision(self,formula):
        '''
        Using Levi identity
        '''
        if not self.checkConsistancy(formula):
            print("Beliefs are inconsistent if you add '{}', doing contraction now:".format(formula))    
            self.contraction('n('+formula+')')

        self.add(formula)
        self.printBeliefBase()

    def contraction(self,formula):
        '''
        partial meet contraction
        '''
        remainder_set = self.findRemainderSet(formula)
        selectedRemainders = self.selectionFunction(remainder_set)

        if len(selectedRemainders)==1:
            self.beliefBase = selectedRemainders[0]
        else:
            # find the intersection part
            # using map() + intersection() 
            res = list(set.intersection(*map(set, selectedRemainders))) 
            self.beliefBase = res
        print("After contraction, belief base = ", self.beliefBase)

    def findRemainderSet(self,formula):
        '''
        Find the set of inclusion-maximal subsets of beliefBase that do not imply given formula.
        '''
        remainder_set = []
        subset = findSubset(self.beliefBase)
        #print("subset:",subset)
        for s in subset:     
            if not self.CheckEntailment(formula,base=s):
                remainder_set.append(s)

        delete_set = []  
        for i in remainder_set:
            for j in remainder_set:
                if i!=j:
                    if i in findSubset(j):
                        if i not in delete_set:
                            delete_set.append(i)

        for i in delete_set:
            remainder_set.remove(i)  

        print("remainder set:", remainder_set)                
        return remainder_set

    def selectionFunction(self,remainder_set):
        '''
        An very simple selection function, just choose the largest remainder
        Further improvement should be added (Using plausibility orders)
        '''
        #In the limiting case when remainderSet is empty, then return beliefBase
        if len(remainder_set)==0:
            return self.beliefBase

        selectedRemainders=[]
        maxlen =-1
        for r in remainder_set:
            if len(r)>maxlen:
                maxlen = len(r)
                largest = r
        selectedRemainders.append(largest)

        print("Selected remainder(s):", selectedRemainders)   
        return selectedRemainders

    # def add(self,formula):
    #     '''
    #     Add a new formula in belief base if it is consistent
    #     If inconsistent, will not be added
    #     '''
    #     fs = seperateAnd([], formula)
    #     for f in fs:
    #         if not self.checkConsistancy(f):
    #             print("failed")
    #             print("Beliefs are inconsistent if you add {}, try revision function".format(formula))    
    #             return 
    #         if self.CheckEntailment(f):
    #             print("failed")
    #             print("The formula {} and be deducted from other formulas in the belief base".format(formula))    
    #             return             
    #         if f not in self.beliefBase:
    #             self.beliefBase.append(f)
    #     self.printBeliefBase()

    def add(self,f):
        '''
        Add a new formula in belief base if it is consistent
        If inconsistent, will not be added
        '''
        if not self.checkConsistancy(f):
            print("failed")
            print("Beliefs are inconsistent if you add '{}', try revision function".format(formula))    
            
        elif self.CheckEntailment(f):
            print("failed")
            print("The formula '{}' can be deducted from other formulas in the belief base".format(formula))    
                       
        else: 
            self.beliefBase.append(f)
        self.printBeliefBase()

    def printBeliefBase(self):
        print("Current belief base:", self.beliefBase)            



if __name__ == "__main__":

    #This formula is equevilent with  R1 to R5 on page 247 in the AI book
    #Where 'a' which are not inside brackets symbolize the seperation of rules
    #formula = "nCaAf(DoE)aBf(CoFoG)anAaB" 

    bb = BeliefBase()

    # formula = "PiQ" 
    # bb.add(formula)
    # formula = "P" 
    # bb.add(formula)
    # formula = "Q" 
    # bb.add(formula)

    # formula = "nQ"
    # bb.revision(formula)

# ------------------------------- test checkEntailment-----------------#
    # #play the game "little mastermind" in ex10
    # # t1 = T, s1 = S, d1 = D
    # # t2 = Y, s2 = B, d2 = P

    # formula = "ToSoD" 
    # bb.add(formula)
    # formula = "YoBoP" 
    # bb.add(formula)
    # formula = "(nTonS)a(nSonD)a(nDonT)" 
    # bb.add(formula) 
    # formula = "(nYonB)a(nBonP)a(nPonY)" 

    # bb.add(formula)
    # formula = "(TanP)o(PanT)"
    # bb.add(formula)
    # formula = "nTanY"
    # bb.add(formula)
    # formula = "(DanP)o(PanD)"
    # bb.add(formula)

    # formula = "DaY"
    # print(bb.CheckEntailment(formula))
    # formula = "TaP"
    # print(bb.CheckEntailment(formula))
    # formula = "SaB"
    # print(bb.CheckEntailment(formula))        
    # formula = "SaP"
    # print(bb.CheckEntailment(formula))

#------------------------------ test revision ------------------------#
    # pre-KB
    formula = "ToSoD" 
    bb.add(formula)
    formula = "YoBoP" 
    bb.add(formula)
    formula = "(nTonS)a(nSonD)a(nDonT)" 
    bb.add(formula) 
    formula = "(nYonB)a(nBonP)a(nPonY)" 
    bb.add(formula) 

    # deduct 1
    formula = "TaP"
    bb.add(formula)
    formula = "(TanP)o(PanT)"
    bb.revision(formula)

    # deduct 2
    formula = "TaY"
    bb.add(formula)
    formula =  "nTanY"
    bb.revision(formula)

    # deduct 3
    formula = "DaP"
    bb.add(formula)
    formula = "(DanP)o(PanD)"
    bb.revision(formula)    