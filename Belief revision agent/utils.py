
import numpy as np
np.set_printoptions(threshold=10000)


def eliminateIff(sentence_list_total):  # try first to use "modes Ponens"

    for i in range(len(sentence_list_total)):
        #print("sentence i", sentence_list_total[i])

        if 'f' in sentence_list_total[i]:
            #print("sentence i after f found", sentence_list_total[i])
            for j in range(len(sentence_list_total[i])):
                if sentence_list_total[i][j] == 'f':
                    sentence_temp = sentence_list_total[i][0:j]+'i'+sentence_list_total[i][j+1:]+'a'+sentence_list_total[i][j+1:]+'i'+sentence_list_total[i][0:j]
                    #print("sent_temp" ,sentence_temp)

            sentence_list_total_temp = []
            sentence_list_total_temp = seperateAnd(sentence_list_total_temp, sentence_temp)
            sentence_list_total_temp = eliminateImply(sentence_list_total_temp)
            sentence_list_total_temp = ')a('.join(sentence_list_total_temp)
            sentence_list_total_temp = '('+sentence_list_total_temp+')'
            sentence_list_total[i]=sentence_list_total_temp

    return sentence_list_total


def eliminateImply(sentence_list_total):
    for i in range(len(sentence_list_total)):
        #print(elem)
        if 'i' in sentence_list_total[i]:
            for j in range(len(sentence_list_total[i])):
                if sentence_list_total[i][j] == 'i':
                    sentence_temp = 'n' + sentence_list_total[i][0:j] + 'o' + sentence_list_total[i][j + 1:]
                    sentence_list_total[i] = sentence_temp

    return sentence_list_total


def seperateAnd(sentence_list_total, sentence):  # seperate all sentences containing AND (not within parentheses)
    paran = 0
    for i in range(len(sentence)):

        if sentence[i] == '(':
            paran += 1

        if sentence[i] == 'a' and paran == 0:
            if len(sentence[0:i]) > 0:
                sentence_list_total.append(sentence[0:i])
            sentence_temp = sentence[i + 1:]
            return seperateAnd(sentence_list_total, sentence_temp)

        if sentence[i] == ')' and paran == 0:
            sentence_list_total.append(sentence[0:i + 1])
            sentence_temp = sentence[i + 1:]
            return seperateAnd(sentence_list_total, sentence_temp)

        if sentence[i] == ')':
            paran -= 1

        if not 'a' in sentence:
            sentence_list_total.append(sentence)
            break

        if i == len(sentence)-1:
            sentence_list_total.append(sentence)
            break

    return sentence_list_total

def regitrerBooleans(beliefBase):
    boolean_list = []
    for elem in beliefBase:
        for l in elem:
            if l.isupper() and l not in boolean_list:
                boolean_list.append(l)
    boolean_list.sort()
    return boolean_list

def createTruthTable(boolean_list_lenth):
        if boolean_list_lenth < 1:
            return [[]]
        subtable = createTruthTable(boolean_list_lenth - 1)
        #print(subtable)
        return [row + [v] for row in subtable for v in [False, True]]


def translateSentencesToSyntax(sentence_list_total,boolean_list):
    translated_sentences = []
    for i in range(len(sentence_list_total)):
        translated_sentence = []
        for j in range(len(sentence_list_total[i])):
            if sentence_list_total[i][j].isupper():
                sentence_temp = []
                for k in range(len(boolean_list)):

                    if sentence_list_total[i][j] == boolean_list[k]:
                        sentence_temp.append(['updated_truth_table[i][',str(k),']'])

                translated_sentence.append(''.join(sentence_temp[0]))


            if sentence_list_total[i][j] == "(":
                translated_sentence.append("(")

            if sentence_list_total[i][j] == ")":
                translated_sentence.append(")")

            if sentence_list_total[i][j] == "n":
                translated_sentence.append(" not ")

            if sentence_list_total[i][j] == "o":
                translated_sentence.append(" or ")

            if sentence_list_total[i][j] == "a":
                translated_sentence.append(" and ")

        translated_sentence =''.join(translated_sentence)
        translated_sentences.append(translated_sentence)

    return translated_sentences

def addRuleColumns(truth_table,sentence_list_total_translated):
    rule_columns = np.zeros((np.size(truth_table,0),len(sentence_list_total_translated)),dtype=bool)
    updated_truth_table = np.concatenate((truth_table,rule_columns),axis=1)

    for j in range(np.size(truth_table,1),np.size(updated_truth_table,1)):
        A = sentence_list_total_translated[j - np.size(truth_table, 1)]
        for i in range(np.size(updated_truth_table,0)):
            Z = eval(A)
            updated_truth_table[i][j] = Z

    kb_column = np.zeros(((np.size(truth_table,0),1)),dtype=bool)
    updated_truth_table = np.concatenate((updated_truth_table, kb_column), axis=1)

    for k in range(np.size(updated_truth_table,0)):
        updated_truth_table[k][-1] = np.product(updated_truth_table[k][truth_table.shape[1]:-1])
    return updated_truth_table


def testForTrueKb(updated_truth_table):
    ret = False
    for i in range(updated_truth_table.shape[0]):
        if updated_truth_table[i][-1] == 1:
            #print("Line ",i," makes this kb true")
            ret = True  
    return ret


##################################################################################

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


def testProperties(outcome):
    pass
