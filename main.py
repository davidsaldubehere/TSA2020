import eel #third party (open source)
import wx #third party (open source)
import ctypes #third party (open source)
from decimal import Decimal 
from itertools import permutations  
from fileController import getPath #custom for project
from proteinTranscriber import matchBases #custom for project
from loopingTools import generateInitiator, findAll, getExonCombinations #custom for project

terminator = "CGCGCGCGAAACGCGCGCGTTTTTTT"
promoters = generateInitiator() #generates all of the possible initiators
substrings = []
totalExons = []
proteins = []

try: #prevents the file dialog from looking blurry
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception: #testing for any exception is usually too broad but this feature is uneccessary so there is no risk benifit
    pass
#sends data to the front-end
def send(data, target):
    eel.update(str(data), target)

@eel.expose
def findPromoters(data):
    DNA = data
    #creates a list of all promoter positions using list comprehension
    promoterPos = [list(findAll(DNA, promoter)) for promoter in promoters if list(findAll(DNA, promoter)) != []]
    terminatorPos = list(findAll(DNA, terminator))
    #strings are immutable so conversion to a list is neccessary to use indices
    temp = list(DNA)
    for i in promoterPos:
        count = 0
        for start in i:
            length, startCount = 7, 2
            if DNA[start:start+6] == "TATAAA": #the special case
                length, startCount = 6, 25
                #for every other promoter
            if len(terminatorPos) == 0:
                send("Please input at least one terminator", "output")
                break
            if start + length < terminatorPos[count]: #if the string is withing the current terminator
                substrings.append(DNA[start+startCount: terminatorPos[count]+26])
            elif start + length > terminatorPos[count]:
                count += 1
                try: #attempts to go to the next terminator
                    substrings.append(DNA[start+startCount: terminatorPos[count]+26])
                except IndexError:
                    continue
                    
            temp[start] = f'>{temp[start]}' #replaces at that specific index
            temp[terminatorPos[count]] = f'<{temp[terminatorPos[count]]}'
    #sends to the output 
    send(f"Promoters followed by a '>' \nTerminators followed by a '<'\n {''.join(temp)}", 'output')
    send("Promoters and terminators successfully found \nDNA converted to RNA", "status")

@eel.expose
def findExons():
    #converts every substring into RNA and splits by exons
    splicedStrings = [string.replace("T", "U").split("GUAAGU") for string in substrings]

    for spliced in splicedStrings:
        innerExons = []
        for individualString in spliced:
            endPos = individualString.find("CAG")
            if(endPos > -1): #if the endPos doesn't exist
                endRemoved = individualString[endPos+3: len(individualString)]
                innerExons.append(endRemoved)
            else: #appends everything between the exons
                innerExons.append(individualString)
        totalExons.append(innerExons)
    #gets all combinations of exons and sends it to the ouput
    send(f"All Total Exons - \n {totalExons}\n All total combinations - \n {getExonCombinations(totalExons)}\n", "output")
    send("Exon Combinations Found", "status")

@eel.expose
def transcribeProteins():
    codonLists = []
    #loops throught the combinations of exons
    for combo in getExonCombinations(totalExons):
        codons = ([combo[i:i+3] for i in range(0, len(combo), 3)])#splits on every codon
        #finds the positions of start and stop codons
        startPos = [count for count, codon in enumerate(codons) if codon == "AUG"]
        endPos = [count for count, codon in enumerate(codons) if codon == "UGA" or codon == "UAA" or codon =="UAG"]
        count = 0 #used for codon sequences withing codon sequences
        for start in startPos:
            if start < endPos[count]:
                codonLists.append(codons[start:endPos[count]])
            else:
                count+=1
                try:      #attempts to find the next ending
                    codonLists.append(codons[start:endPos[count]])
                except IndexError:
                    continue
    print(codonLists)
    finalCodons = []
    [finalCodons.append(i) for i in codonLists if i not in finalCodons] #removes duplicates
    send(f'\nList of all codon combinations (duplicates removed) {finalCodons}\n', "output")
    send("Codon combinations found", "status")
    
    #Begins protein transcription
    for independentCodon in finalCodons:
        currentProtein = ""
        mass = Decimal(str("0")) #decimal module avoids floating point error
        charge = 0
        for codon in independentCodon:
            #adds all the values of the corresponding protein
            returnedProtein = matchBases(codon)
            currentProtein += returnedProtein[0]
            mass += Decimal(str(returnedProtein[1]))
            charge += returnedProtein[2]
        proteins.append([currentProtein, f'{mass}u', f'{charge}e'])
    #and outputs the result to console
    send("FINAL LIST OF PROTEINS\n", "output")
    for protein in proteins:
        send(f'{protein}\n', "output")
    send("Proteins found", "status")
    #If the VAL protein should be a LEU protein, then you may have a flawed test case
    #The challenge provider made a simple switch from GUU to CUU on accident
    #Please check the documentation for more info 
    send("WARNING some of the example test cases provided for this challenge have hand calculation errors and do not match this programs output (especially the Leu protein). Please check this program's documentation for the explanation", "output")
            
@eel.expose
def reset(): #resets variables to default values
    global substrings, totalExons, proteins
    substrings = []
    totalExons = []
    proteins = []
    send("Program Reset", "status")

@eel.expose
def getFile(): #opens file dialog from file controller
    path = getPath('*')
    if path != None:
        return open(path, "r").read()
    else:
        return 'No File Selected'

def startEel(): #starts the front-end server
    eel.init('web')
    eel.start('index.html')

if __name__ == "__main__":
    startEel()