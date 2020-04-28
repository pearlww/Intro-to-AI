
from beliefBase import *

def createMask(lenth):
        if lenth < 1:
            return [[]]
        subtable = createMask(lenth - 1)
        #print(subtable)
        return [row + [v] for row in subtable for v in [False, True]]
        
def findSubset(beliefBase):
    subset = []
    masks = createMask(len(beliefBase))
    for mask in masks:
        index = []
        for i in range(len(mask)):
            if mask[i]==True:
                index.append(i)
        s = [beliefBase[i] for i in index]
        subset.append(s)
    return subset


def findRemainderSet(beliefBase,sentence):
    '''
    Find the set of inclusion-maximal subsets of beliefBase that do not imply given sentence.
    '''
    remainderSet = []
    subset = findSubset(beliefBase)
    print("subset:",subset)
    for s in subset:     
        if enterAndCheck(s.copy(), 'n('+sentence+')'):
            remainderSet.append(s)
    for i in remainderSet:
        for j in remainderSet:
            if i!=j:
                if i in findSubset(j):
                    remainderSet.remove(i)

    return remainderSet

def selectionFunction(beliefBase,remainderSet):
    #In the limiting case when remainderSet is empty, then return beliefBase
    if len(remainderSet)==0:
        return beliefBase

    max_len = max(len(i) for i in remainderSet)
    selectedRemainders=[]
    for i in remainderSet:
        if len(i)>max_len:
            selectedRemainders.append(i)

    return selectedRemainders

def contraction(selectedRemainders):

    return outcome

def testProperties(outcome):
    pass

def add():
    pass

def revision(beliefBase,sentence):
    contraction()
    add()



if __name__ == "__main__":

    beliefBase = ['P', 'Q', 'nPoQ']
    sentence = "Q"
    r = findRemainderSet(beliefBase,sentence)
    print(r)