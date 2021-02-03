import itertools

#generates all of the 129 promoters
def generateInitiator():
    special = "TATAAA"
    combinations = [["C", "T"], ["C", "T"], ["A"], ["A", "G", "C", "T"], ["A", "T"], ["C", "T"], ["C", "T"]]
    promoters = list(''.join(i) for i in itertools.product(*combinations))
    promoters.append(special)
    return promoters

#finds all positions of a string in another string (useful in many cases)
def findAll(aStr, sub):
    start = 0
    while True:
        start = aStr.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) 

def allCombinations(list):
    return itertools.chain.from_iterable(
        itertools.combinations(list, i + 1)
        for i in range(len(list)))
#returns all of the combinations of Exons
def getExonCombinations(exonList):
    exonCombos = []

    for exon in exonList:
        if len(exon) > 2:
            middleList = [list(l) for l in (allCombinations(exon[1:len(exon)-1]))]

            for i in middleList:
                exonCombos.append(f"{exon[0]}{''.join(i)}{exon[-1]}")
            #adds the first and last element without any middleList elements
            exonCombos.append(exon[0]+ exon[-1])
        elif len(exon) == 2:
            exonCombos.append(exon[0]+exon[1])
        #return the original if there aren't any introns
        else:
            exonCombos.append(exon[0])
    return exonCombos
