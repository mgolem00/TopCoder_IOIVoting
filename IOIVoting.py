#Problem statement: https://community.topcoder.com/stat?c=problem_statement&pm=17039

import numpy as np
from time import perf_counter_ns

def getSubtractedVotes(n, votes):
    subtractedVotes = np.zeros((n,n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j:
                subtractedVotes[i][j] = votes[i][j] - votes[j][i]
    print(subtractedVotes)
    return subtractedVotes

def sequenceStrenght(seq, B, subtractedVotes):
    while seq[-1] != B and len(seq) != len(subtractedVotes):
        temp = subtractedVotes[seq[-1]].tolist()
        if len(seq) == 1:
            temp.pop(seq[0])
            if B == 0 or seq[0] > B:
                temp.pop(B)
            else:
                temp.pop(B-1)
        elif len(seq) >= 2:
            popped = 0
            for i in seq:
                if i == seq[0]:
                    temp.pop(i)
                    popped += 1
                else:
                    if i == 0:
                        temp.pop(i)
                        popped += 1
                    else:
                        temp.pop(i-popped)
                        popped += 1
        
        maxVote = max(temp)
        if maxVote >= subtractedVotes[seq[0]][B]:
            maxVotePos = subtractedVotes[seq[-1]].tolist().index(maxVote)
            seq.append(maxVotePos)
        else:
            break
    
    return seq

def getWinners(n, votes):
    winners= []
    for i in range(n):
        winners.append(i)
        
    subtractedVotes = getSubtractedVotes(n, votes)
    
    equalFlag = False
    lastStop = 0
    for i in range(n-1):
        if equalFlag == False:
            j = winners[0]
            k = winners[1]
        else:
            j = lastStop
            k = lastStop+1
            
        if votes[j][k] > votes[k][j]:
            toRemove = k
            equalFlag = False
            seq = sequenceStrenght([k], j, subtractedVotes)
            if seq[-1] == j:
                temp = []
                for l in range(len(seq)-1):
                    temp.append(subtractedVotes[l][l+1])
                if min(temp) > votes[j][k]:
                    toRemove = j
                elif min(temp) == votes[j][k]:
                    equalFlag = True
                    lastStop = k
                    continue
            winners.remove(toRemove)
                
        elif votes[j][k] == votes[k][j]:
            equalFlag = True
            lastStop = k
            continue
            
        elif votes[j][k] < votes[k][j]:
            toRemove = j
            equalFlag = False
            seq = sequenceStrenght([j], k, subtractedVotes)
            if seq[-1] == k:
                temp = []
                for l in range(len(seq)-1):
                    temp.append(subtractedVotes[l][l+1])
                if min(temp) > votes[k][j]:
                    toRemove = winners[1]
                elif min(temp) == votes[k][j]:
                    equalFlag = True
                    lastStop = k
                    continue
            winners.remove(toRemove)
    
    return winners

def getVotes():
    while 1:
        n = int(input("Enter number of options: "))
        if n >= 1 and n <= 50:
            break
        else:
            print("Must be a number between 1 and 50!")
    voteMatrix = np.zeros((n,n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j:
                while 1:
                    voteMatrix[i][j] = int(input("Enter number of votes for option [{}, {}]: ".format(i,j)))
                    if voteMatrix[i][j] >= 0 and voteMatrix[i][j] <= 9999:
                        break
                    else:
                        print("Must be a number between 0 and 9999!")
    print("Vote matrix:")
    print(voteMatrix)
    return n, voteMatrix

def getVotesFromFile(filename):
    f = open(filename, 'r')
    n = 0
    votesRow = []
    while 1:
        line = f.readline()
        if line == "":
            break
        votesRow.append(line.split())
        n += 1
    f.close()
    
    voteMatrix = np.zeros((n,n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j:
                voteMatrix[i][j] = votesRow[i][j]
    
    print("Vote matrix:")
    print(voteMatrix)
    return n, voteMatrix

def main():
    t_start = perf_counter_ns()
    
    #n, votes = getVotes() #if you want to enter your own vote example
    n, votes = getVotesFromFile("Example2.txt") #Examples from the problem statement in files: Example0.txt, Example1.txt, Example2.txt, Example3.txt, Example4.txt
    winners = getWinners(n, votes)
    print("The winners are:", winners)
    
    t_stop = perf_counter_ns()
    print("Elapsed time during the whole program:", t_stop-t_start, "ns")

if __name__ == "__main__":
    main()