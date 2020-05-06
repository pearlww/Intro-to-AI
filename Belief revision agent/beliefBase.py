
from utils import *


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
        if base:
            bcopy = base.copy()
        else:
            bcopy = self.beliefBase.copy()
        bcopy.append(formula)

        bcopy = eliminateIff(bcopy)
        bcopy = eliminateImply(bcopy)
        boolean_list = regitrerBooleans(bcopy)
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
        remainderSet = self.findRemainderSet(formula)
        selectedRemainders = self.selectionFunction(remainderSet)

        if len(selectedRemainders)==1:
            self.beliefBase = selectedRemainders
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
        remainderSet = []
        subset = findSubset(self.beliefBase)
        print("subset:",subset)
        for s in subset:     
            if not self.CheckEntailment(formula,base=s):
                remainderSet.append(s)
        for i in remainderSet:
            for j in remainderSet:
                if i!=j:
                    if i in findSubset(j):
                        remainderSet.remove(i)
        print("remainder set:", remainderSet)                
        return remainderSet

    def selectionFunction(self,remainderSet):
        '''
        An very simple selection function, just choose the largest remainder
        Further improvement should be added (Using plausibility orders)
        '''
        #In the limiting case when remainderSet is empty, then return beliefBase
        if len(remainderSet)==0:
            return self.beliefBase

        selectedRemainders=remainderSet[0]
        for r in remainderSet:
            if len(r)>len(selectedRemainders):
                selectedRemainders = r

        print("Selected remainder(s):", selectedRemainders)   
        return selectedRemainders

    def add(self,formula):
        '''
        Add a new formula in belief base if it is consistent
        If inconsistent, will not be added
        '''
        if not self.checkConsistancy(formula):
            print("Beliefs are inconsistent if you add {}".format(formula))    
            print("Try revision function")
            return 

        if formula not in self.beliefBase:
            self.beliefBase.append(formula)
        self.printBeliefBase()

    def printBeliefBase(self):
        print("Current belief base:", self.beliefBase)
            



if __name__ == "__main__":

    #This formula is equevilent with  R1 to R5 on page 247 in the AI book
    #Where 'a' which are not inside brackets symbolize the seperation of rules
    #formula = "nCaAf(DoE)aBf(CoFoG)anAaB" 

    bb = BeliefBase()

    formula = "PiQ" 
    bb.add(formula)
    formula = "P" 
    bb.add(formula)
    formula = "Q" 
    bb.add(formula)

    formula = "nQ"
    bb.revision(formula)



