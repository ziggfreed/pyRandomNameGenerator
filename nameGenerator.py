import random
import argparse

alphabet = "abcdefghijklmnopqrstuvqxyz"
threeLetterDict = {}

# Random Greek names
inputNames = ["Achillios", "Adonia", "Adonis", "Agalia", "Agapios", "Agathe", "Akilina", "Aleka", 
              "Alekos", "Alethea", "Alethia", "Alexandros", "Alexios", "Alithea", "Altair", "Anastasia", 
              "Anastasios", "Anatolios", "Andrianna", "Angele", "Angeliki", "Antheia", "Antonia", 
              "Apollo", "Apolo", "Arete", "Argus", "Aristides", "Aristokles", "Aristotelis", "Aristotle", 
              "Arsenios", "Artemisia", "Aspasia", "Athanasia", "Athanasios", "Athena", "Augustine"]


def GenerateName(dictionaryInput, length):
    '''Generates a random name based on the supplied dictionary and minimum length'''
    # Get the start of the name 
    name = GetNamePart(dictionaryInput)

    #keep looping until we get a name that exceeds the minumum length
    while (len(name) < length):
        # To make the word sound better, we'll ensure the first letter = the last letter of the name we have so far
        # so abc would require something starting with c to continue the name -> cde etc
        newDict = {k:v for k,v in dictionaryInput.items() if k[:1] == name[-1]}
        if len(newDict) < 0: # what if we don't have any items? lets send the full dictionary
            newDict = dictionaryInput
            
        # take the name we have, drop the last letter and append the new section
        # abc + cde = abcde (no duplicate c)
        name = name[:-1] + GetNamePart(newDict)

    return name.capitalize()

def GetNamePart(dictionaryInput):
    '''This is the part that actually gets the name'''
    # Get total count of all these values
    totalCount = sum(list(dictionaryInput.values()))

    rnd = random.random()
    total = 0
    for k,v in dictionaryInput.items():
        total += v / totalCount #This will normalise them
        if rnd <= total:
            return k

def LoadFile(FileName):
    ''' Read the file '''
    global inputNames
    global threeLetterDict
    with open(FileName, mode='r', encoding='utf-8') as file:
        inputNames = list(file.readlines())
        totalNames = len(inputNames)
        threeLetterDict = {x+y+z : c.lower().count(x+y+z)/totalNames for x in alphabet for y in alphabet for z in alphabet for c in inputNames if c.lower().count(x+y+z) > 0}

parser = argparse.ArgumentParser(description="Generate random name from file")
parser.add_argument("-f", "--file", action="store", dest="inputFile", help="Input File", default=None)

args = parser.parse_args()

if args.inputFile == None:
    totalNames = len(inputNames)
    threeLetterDict = {x+y+z : c.lower().count(x+y+z)/totalNames for x in alphabet for y in alphabet for z in alphabet for c in inputNames if c.lower().count(x+y+z) > 0}
else:
    LoadFile(args.inputFile)
    totalNames = len(inputNames)

print(GenerateName(threeLetterDict, int(random.random() * 10 + 3)))