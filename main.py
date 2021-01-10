import eel
import wx
import ctypes
from itertools import permutations  
#ALL IMPORTS BELOW CONTAIN CODE MADE SPECIFICALLY FOR THIS PROJECT
from fileController import getPath
from proteinTranscriber import matchBases
from loopingTools import generateInitiator, findAll, getExonCombinations

terminator = "CGCGCGCGAAACGCGCGCGTTTTTTT"
promoters = generateInitiator()
substrings = []
#prevents the file dialog from looking blurry
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
#testing for any exception is usually too broad but this feature is uneccessary so there is no risk benifit
except Exception:
    pass
#sends data to the front-end
def send(data, target):
    eel.update(str(data), target)

@eel.expose
def findPromoters(data):
    RNA = data
    #creates a list of all promoter positions using list comprehension
    promoterPos = [list(findAll(RNA, promoter)) for promoter in promoters if list(findAll(RNA, promoter)) != []]
    terminatorPos = list(findAll(RNA, terminator))
    #strings are immutable so conversion to a list is neccessary to use indices
    temp = list(RNA)
    for i in promoterPos:
        count = 0
        for start in i:
            length, startCount = 7, 2
            #The special case
            if RNA[start:start+6] == "TATAAA":
                length, startCount = 6, 25
                #for every other promoter
            if len(terminatorPos) == 0:
                send("Please input at least one terminator", "output")
                break
            if start + length < terminatorPos[count]:
                print("Case 1")
                substrings.append(RNA[start+startCount: terminatorPos[count]+26])
            elif start + length > terminatorPos[count]:
                print("Case 2")
                count += 1
                try:
                    substrings.append(RNA[start+startCount: terminatorPos[count]+26])
                except IndexError:
                    continue
                    
            temp[start] = f'>{temp[start]}'
            temp[terminatorPos[count]] = f'<{temp[terminatorPos[count]]}'
    print(substrings)
    #sends to the output 
    send(f"Promoters followed by a '>' \nTerminators followed by a '<'\n {''.join(temp)}", 'output')
    send("Promoters and terminators successfully found \nDNA converted to RNA", "status")

@eel.expose
def findExons():
    #converts every substring into RNA and splits by exons
    splicedStrings = [string.replace("T", "U").split("GUAAGU") for string in substrings]
    print(splicedStrings)
    totalExons = []
    for spliced in splicedStrings:
        innerExons = []
        for individualString in spliced:
            endPos = individualString.find("CAG")
            if(endPos > -1):
                endRemoved = individualString[endPos+3: len(individualString)]
                innerExons.append(endRemoved)
            else:
                innerExons.append(individualString)
        totalExons.append(innerExons)
    
    #gets all combinations of exons and sends it to the ouput
    send(f"All Total Exons - \n {totalExons}\n All total combinations - \n {getExonCombinations(totalExons)}", "output")
    send("Exon Combinations Found", "status")

@eel.expose
def reset(): #resets variables to default values
    global substrings
    substrings = []
    send("Program Reset", "status")

@eel.expose
def getFile():
    path = getPath('*')
    if path != None:
        return open(path, "r").read()
    else:
        return 'No File Selected'

def startEel():
    eel.init('web')
    eel.start('index.html')

if __name__ == "__main__":
    startEel()
