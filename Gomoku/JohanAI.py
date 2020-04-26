import numpy as np
import sys

def testForConcat(GameMatrix):
    N,M = GameMatrix.shape
    concatList = []
    for j in range(M):
        for i in range(N):
            if GameMatrix[i][j] == 1:
                for k in range(1,5):
                    count = 1
                    testForConcatRecur(GameMatrix,i,j,k,count,concatList)
    return sortConcatList(concatList)




def testForConcatRecur(GameMatrix,i,j,k,count,concatList):
    #print("test", i,j,k)
    N,M = GameMatrix.shape
###################Direction1
    if k == 1 and 1 <= i < N and 0 <= j < M-1 and GameMatrix[i-1][j+1] == 1: #next in line control
        count += 1
        #print("count1:",count)
        return testForConcatRecur(GameMatrix,i-1,j+1,k,count,concatList)
     
    
    elif k == 1 and count > 1: #no more left in line
        concatList.append([k,(i,j),(i+(count-1),j-(count-1)),count])
        
        #print("apend1")
        return concatList    

###################Direction2        
    if k == 2 and 0 <= i < N and 0 <= j < M-1 and GameMatrix[i][j+1] == 1: #next in line control
        count += 1
        #print("count2:",count)
        return testForConcatRecur(GameMatrix,i,j+1,k,count,concatList)
     
    
    elif k == 2 and count > 1: #no more left in line
        concatList.append([k,(i,j),(i,j-(count-1)),count])
                     
        #if (i,j) != concatList[l-1][1]:
            
           
        
        #print("apend2")
        return concatList    

###################Direction3   
    if k == 3 and 0 <= i < N-1 and 0 <= j < M-1 and GameMatrix[i+1][j+1] == 1: #next in line control
        count += 1
        #print("count3:",count)
        return testForConcatRecur(GameMatrix,i+1,j+1,k,count,concatList)
     
    
    elif k == 3 and count > 1: #no more left in line
        concatList.append([k,(i,j),(i-(count-1),j-(count-1)),count])
        
        #print("apend3")
        return concatList    

        
#####################Direction 4
    if k == 4 and 0 <= i < N-1 and 0 <= j < M-1 and GameMatrix[i+1][j] == 1: #next in line control
        count += 1
        #print("count3:",count)
        return testForConcatRecur(GameMatrix,i+1,j,k,count,concatList)
     
    
    elif k == 4 and count > 1: #no more left in line
        concatList.append([k,(i,j),(i-(count-1),j),count])
        
        #print("apend3")
        return concatList



def sortConcatList(concatList):
    
    #print(concatList)
    #print()
    concatList.sort(key = lambda concatList: concatList[0])
    #print("heyhey",concatList)
    #print("")
    sortedList = []
    #sortedList.append([0,0,0,0])
    
 
    for l in range(0,len(concatList)):
        dub = 0
        for m in range(0,len(sortedList)):
            if concatList[l][0] == sortedList[m][0] and concatList[l][1] == sortedList[m][1]:
                dub = 1
                
        if dub != 1:
            sortedList.append(concatList[l])
  
    return sortedList


def calculateThreadCell(concat_type, d_count):
    #print(concat_type ,1/d_count)
    #print(concat_type, 5-d_count)
    return 2 * concat_type + np.round((1/d_count),1)



def calculateMatrix(GameMatrix, sortedList): #Used for both ThreadMatrix and Oppotynity Matrix
    N,M = GameMatrix.shape
    Matrix = np.zeros((N,M))
    for j in range(M):
        for i in range(N):
            cell_sum = 0
             # Direction
            for l in range(1,5): #Cell Distance from piece to concat
        
                for m in range(len(sortedList)):
                    #print((i-l,j+l),sortedList[m][2])
                    if sortedList[m][0] == 1 and (i-l,j+l) == sortedList[m][2]:  #direction -1

                        blocked = False
                        for n in range(l):
                            if i-n >= 0 and j+n < M and GameMatrix[i-n][j+n] == -1:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                        

#                    
                    if sortedList[m][0] == 1 and (i+l,j-l) == sortedList[m][1]: #direction 1
                        
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i+n][j-n] == -1 and i+n >= 0 and j-n < M:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break

#                            
                    if sortedList[m][0] == 2 and (i,j+l) == sortedList[m][2]:  #direction -2
                        #print(k,sortedList[m][0] )
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i][j+n] == -1 and j+n < M:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break

                    
                    
                    if sortedList[m][0] == 2 and (i,j-l) == sortedList[m][1]:  #direction 2
                        #print(k,sortedList[m][0] )
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i][j-n] == -1 and j-n >=0:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break
                        
                        
                    if sortedList[m][0] == 3 and (i+l,j+l) == sortedList[m][2]:  #direction -3
                        #print(k,sortedList[m][0] )
                        #print(k,sortedList[m][0] )
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i+n][j+n] == -1 and i+n < N and j+n < M:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break
                        
                    if sortedList[m][0] == 3 and (i-l,j-l) == sortedList[m][1]:  #direction 3
                        #print(k,sortedList[m][0] )
                        #print(k,sortedList[m][0] )
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i-n][j-n] == -1 and i-n >= 0 and j-n >= 0 :
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break
                        
                    if sortedList[m][0] == 4 and (i+l,j) == sortedList[m][2]:  #direction -4

                        blocked = False
                        for n in range(l):
                            if GameMatrix[i+n][j] == -1 and i+n < N:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break
                        
                    if sortedList[m][0] == 4 and (i-l,j) == sortedList[m][1]:  #direction 4
                        #print(k,sortedList[m][0] )
                        blocked = False
                        for n in range(l):
                            if GameMatrix[i-n][j] == -1 and i-n >= 0:
                                #print([i+n][j-n])
                                blocked = True
                            
                        if blocked == False:
                            
                            concat_type = sortedList[m][3]
                            cell_sum += calculateThreadCell(concat_type, l)
                            break
                            
                        else:
                            break

                    
                    if GameMatrix[i][j] == 1 or GameMatrix[i][j] == -1:
                        cell_sum=0
                        
            Matrix[i][j] = cell_sum
    return Matrix

def oppoMatrixaddOn(GameMatrix, OppoMatrix):
    next_to_own_piece_bonus = 0.1
    N,M = GameMatrix.shape
    for j in range(M):
        for i in range(N):
            if GameMatrix[i][j] == -1:
                
                if i-1 >= 0 and j+1 < M and GameMatrix[i-1][j+1] != 1 and GameMatrix[i-1][j+1] != -1: #direction 1
                    OppoMatrix[i-1][j+1] += next_to_own_piece_bonus
                
                if j+1 < M and GameMatrix[i][j+1] != 1 and GameMatrix[i][j+1] != -1: #direction 2
                    OppoMatrix[i][j+1] += next_to_own_piece_bonus
                    
                if i+1 < N and j+1 < M and GameMatrix[i+1][j+1] != 1 and GameMatrix[i+1][j+1] != -1: #direction 3
                    OppoMatrix[i+1][j+1] += next_to_own_piece_bonus
    
                if i+1 < N and GameMatrix[i+1][j] != 1 and GameMatrix[i+1][j] != -1: #direction 4
                    OppoMatrix[i+1][j] += next_to_own_piece_bonus
                  
                if i+1 < N and j-1 >= 0 and GameMatrix[i+1][j-1] != 1 and GameMatrix[i+1][j-1] != -1: #direction -1
                    OppoMatrix[i+1][j-1] += next_to_own_piece_bonus
                    
                    
                if j-1 >= 0 and GameMatrix[i][j-1] != 1 and GameMatrix[i][j-1] != -1: #direction -2
                    OppoMatrix[i][j-1] += next_to_own_piece_bonus
                    
                if i-1 >= 0 and j-1 >=0 and GameMatrix[i-1][j-1] != 1 and GameMatrix[i-1][j-1] != -1: #direction -3
                    OppoMatrix[i-1][j-1] += next_to_own_piece_bonus
                    
                if i-1 >=0 and GameMatrix[i-1][j] != 1 and GameMatrix[i-1][j] != -1: #direction -4
                    OppoMatrix[i-1][j] += next_to_own_piece_bonus
    return OppoMatrix

def SumMatrixWhite(GameMatrix):
    thread_oppo_factor = 0.1 #Thread/oppotunity Ratio 
    #print(GameMatrix)
    ####################Create concat lists for white and black pieces
    sortedList_Black = testForConcat(GameMatrix)
    sortedList_White = testForConcat(GameMatrix*-1)
    
    ####################
    ThreadMatrix_White = calculateMatrix(GameMatrix,sortedList_Black)
    OppoMatrix_White = (calculateMatrix(GameMatrix,sortedList_White))*thread_oppo_factor
    
    OppoMatrix_White = oppoMatrixaddOn(GameMatrix, OppoMatrix_White)
    SumMatrix_White = ThreadMatrix_White+OppoMatrix_White
    print("")
    print("SumMatrix_White")
    print(SumMatrix_White)
    return SumMatrix_White