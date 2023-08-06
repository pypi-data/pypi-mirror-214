import datetime
import inspect
import random
from os.path import getsize


def getCurrentDateTime():
    return datetime.datetime.now().strftime("%H:%M:%S %y/%m/%d")


def getCaller():
    return inspect.stack()[2][3]


def getFileSize(filepath):
    return getsize(filepath)


def generateRandomId(length=16):
    
    characterSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    generatedId = []
    
    while len(generatedId) < length:
        sampleSize = min(length - len(generatedId), len(characterSet))
        sample = random.sample(characterSet, sampleSize)
        generatedId.extend(sample)
        
    return ''.join(generatedId)