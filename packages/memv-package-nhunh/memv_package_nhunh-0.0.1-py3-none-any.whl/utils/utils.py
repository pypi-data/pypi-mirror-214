# This function is used to check if the rectangles overlaps with other rectangles, if it does, calculate the overlapped area
# Text is rectangle bound the text
# def calculateOverlappedArea(textX1, test_link, ignore_roi_path):
import numpy as np
import math

def removeSpecialCharacters(text):
    text = text.replace('(', '')
    text = text.replace('GB', '')
    text = text.replace('G', '')
    text = text.replace('MB', '')
    text = text.replace('M', '')

    return text

def convertToMB(memSize):
    if "G" in memSize:
        memSize = removeSpecialCharacters(memSize)
        return math.ceil(float(memSize) * 1024)
    elif "M" in memSize:
        memSize = removeSpecialCharacters(memSize)
        return math.ceil(float(memSize))
    
def parseDurationToSecond(duration_str):
    duration_unit = duration_str[-1]
    duration_value_str = duration_str[:-1]
    try:
        duration_value = int(duration_value_str)
    except ValueError:
        print(f'Invalid duration format: "{duration_str}". Supported 30s | 30m | 8h | 3d')
        return None
    
    if duration_unit == 's':
        return duration_value
    elif duration_unit == 'm':
        return duration_value * 60
    elif duration_unit == 'h':
        return duration_value * 60 * 60
    elif duration_unit == 'd':
        return duration_value * 60 * 60 * 24
    else:
        print(f'Invalid duration format: "{duration_str}". Supported 30s | 30m | 8h | 3d')
        return None