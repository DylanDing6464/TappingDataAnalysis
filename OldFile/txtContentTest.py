import txtContentProcessAnalysis
import numpy as np
import pandas as pd
#
# dataFolderPath = r"D:\MyFile\Penn State University Files\Pitch Exploration Lab\Tapping Data\Label export\GS"
# print(txtContentProcessAnalysis.getFileDict(dataFolderPath))

# # creat a list that have the target data file name     and process those.

universityName1 = "PSU"
universityName2 = "GS"
dataFolderPath1 = r"D:/MyFile/Penn State University Files/Pitch Exploration Lab/Tapping Data/Label export/PSU"
dataFolderPath2 = r"D:/MyFile/Penn State University Files/Pitch Exploration Lab/Tapping Data/Label export/GS_Copy"

newAnalysis = txtContentProcessAnalysis.TxtContentProcessAnalysis(universityName1, dataFolderPath1)
# print(newAnalysis.generateFileDict())

# print(newAnalysis.sortingTappingData_BPM())

# print(newAnalysis.Runner())
newAnalysis.Runner()
print(newAnalysis.getRawData())
print("_______________________________")
print(newAnalysis.getProcessedData())
# IOIAll = newAnalysis.getProcessedData()["stdIOI"]["stdIOIAll"]
# print(IOIAll)
print("_______________________________")

