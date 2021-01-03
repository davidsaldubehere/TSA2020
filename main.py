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
                print("eyysyadfyadsyf")
                length, startCount = 6, 25
                #for every other promoter
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
    send("Promoters followed by a '>'", 'output')
    send("Terminators followed by a '<'", 'output')   
    send("".join(temp), 'output')
    send("Promoters and terminators successfully found", "status")
    send("DNA converted to RNA", "status")

@eel.expose
def findExons():
    splicedStrings = []
    for string in substrings:
        string = string.replace("T", "U")
        splicedStrings.append((string.split("GUAAGU")))


@eel.expose
def getFile():
    path = getPath('*')
    if path != None:
        return open(path, "r").read()
    else:
        return 'No File Selected'


eel.init('web')
eel.start('index.html')
