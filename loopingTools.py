import itertools

#generates all of the 129 promoters
def generateInitiator():
    special = "TATAAA"
    combinations = [["C", "T"], ["C", "T"], ["A"], ["A", "G", "C", "T"], ["A", "T"], ["C", "T"], ["C", "T"]]
    promoters = list(''.join(i) for i in itertools.product(*combinations))
    promoters.append(special)
    return promoters

#finds all positions of a string in another string
def findAll(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) 
#returns all of the combinations of Exons
def getExonCombinations():
    pass