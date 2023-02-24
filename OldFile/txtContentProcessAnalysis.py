# @author: Dylan Ding
# Date: 1/25/2022

# <editor-fold desc="import">
# Operate system interface
import os
import statistics
import openpyxl as opx
import numpy as np
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows



# </editor-fold>


class TxtContentProcessAnalysis:
    """
    A class's goal is to create a excel file from a series of txt files that contain the tapping data

    Method: includes
    """

    def __init__(self, universityName="", dataFolderPath=r""):
        # the name of the university
        self.universityName = universityName
        # the path of the folder that contains text files
        self.dataFolderPath = dataFolderPath
        # a dictionary that contains all files' name classified by participants' index
        self.fileDict = {}
        # a dictionary that contains classified data in type of Data Frame
        self.rawData = {}
        # a dictionary that contains calculated data (e.g. IOI, mean IOI, standard deviation)
        self.processedData = {}

    # <editor-fold desc="Getter and Setter">
    # setter and getter start
    def getUniversityName(self):
        return self.universityName

    def setUniversityName(self, newUniversityName):
        self.universityName = newUniversityName

    def getFileDict(self):
        return self.fileDict

    def setFileDict(self, newFileDict):
        self.fileDict = newFileDict

    def getRawData(self):
        return self.rawData

    def setRawData(self, newRawData):
        self.rawData = newRawData

    def getProcessedData(self):
        return self.processedData

    def setProcessedData(self, newProcessedData):
        self.processedData = newProcessedData

    # setter and getter end
    # </editor-fold>

    def renameFile(self):
        """
        The method is to rename the files in the target folder into optimal format.
        The original filename format must be like "Participant's index_BPM_Trail Number_University Name"
                                            E.g. "P1_75_T1_PSU"

        :return: True as a flag shows that the file names are being reformatted into a correct format

        """
        # Put the files' name in the target folder into a list
        fileList = os.listdir(self.dataFolderPath)

        for fileName in fileList:
            # create a list (["Participant's index", "BPM", "Trail Number"])
            fileNameSplitList = fileName.split("_")
            # get the numbers in each element
            for i in range(len(fileNameSplitList)):
                tempString = ""
                for element in fileNameSplitList[i]:
                    # put digits from the each element in fileNameSplitList into a new string to replace
                    # the original element
                    if element.isdigit():
                        tempString += element
                # replace
                fileNameSplitList[i] = tempString

            # generate the correct format of the file name E.g. P1_75_T1.txt
            changedFileName = f"P{fileNameSplitList[0]}_{fileNameSplitList[1]}_T{fileNameSplitList[2]}_" \
                              f"{self.universityName}.txt "

            # rename
            originFileNamePath = fr"{self.dataFolderPath}/{fileName}"
            changedFileNamePath = fr"{self.dataFolderPath}/{changedFileName}"

            os.rename(originFileNamePath, changedFileNamePath)

        return True

    def generateFileDict(self):
        """
        This function is to classify file names of files from the target folder (where store the txt files)(path)
        into a dictionary

            os.listdir(): method in python is used to get the list of all files and directories in the specified
            directory. If we don’t specify any directory, then list of files and directories in the current working
            directory will be returned.

        :rtype: dictionary
        :return: fileDict:  a dictionary that contains text files' name classified by participants' index

        """

        # fileList: a list contains the files' name in the target folder output E.g. 'P11_100_Trial2.txt'
        fileList = os.listdir(self.dataFolderPath)
        fileDict = {}
        # classify files and put them into dictionary
        for fileName in fileList:
            fileNameSeparate = fileName.split("_")
            # participantDict key list
            PDKeyList = fileDict.keys()
            participantIndex = fileNameSeparate[0]

            # if the participant's index(name) is not in the dictionary key
            if participantIndex not in PDKeyList:
                fileDict[participantIndex] = [fileName]
            # if the participant's index(name) is in the dictionary key
            else:
                fileDict[participantIndex].append(fileName)

        for participant in fileDict.keys():
            fileNameList = fileDict[participant]
            for i in range(1, len(fileNameList)):
                for j in range(0, len(fileNameList) - i):
                    if fileNameList[j].split("_")[2] > fileNameList[j + 1].split("_")[2]:
                        fileNameList[j], fileNameList[j + 1] = fileNameList[j + 1], fileNameList[j]

        # set the dict to self.fileDict
        self.setFileDict(fileDict)

    @staticmethod
    def differenceCalculation(fileData, fileName):
        """
        This method is to calculate the difference of each rows and the this row (each row) for dataFrame
        E.g. row2 - row1

        :param fileData: the time data of that was imported from the target folder
        :param fileName: the name of the file
        :return: IOIDataFrame: a DataFrame type that calculate the difference of each rows
        """
        # squeeze the data frame to convert it into a series
        fileDataSeries = fileData.squeeze()

        # a quantity or number from which another is to be subtracted.
        dataArrayMinuend = np.array(fileDataSeries.values).T

        # a quantity or number to be subtracted from another.
        dataArraySubtrahend = fileDataSeries.values.tolist()
        dataArraySubtrahend.pop(0)
        dataArraySubtrahend.append(0)
        dataArraySubtrahend = np.array(dataArraySubtrahend).T

        # do the calculation. And use the result to form a 
        IOI = dataArraySubtrahend - dataArrayMinuend
        IOI = IOI[:-1]
        # IOI = np.delete(IOI, 25, 0)
        IOIDataFrame = pd.DataFrame(IOI, columns=[f"{fileName}"])

        return IOIDataFrame

    def sortingTappingData_BPM(self):
        """
            This method is the calculation unit that use the imported data to calculate IOI, MeanIOI, stdIOI, contour
            and classify them into dictionaries.

        """

        # <editor-fold desc="Generate empty Data Frames for concatenation">
        # create an empty data frame that will contain sorted raw data (with 75BPM and 100BPM) of tapping
        dataAll = pd.DataFrame()
        data75BPM = pd.DataFrame()
        data100BPM = pd.DataFrame()

        IOIAll = pd.DataFrame()
        IOI75BPM = pd.DataFrame()
        IOI100BPM = pd.DataFrame()

        meanIOIAll = pd.DataFrame(columns=["Trail", "Mean IOI"])
        meanIOI75BPM = pd.DataFrame(columns=["Trail", "Mean IOI"])
        meanIOI100BPM = pd.DataFrame(columns=["Trail", "Mean IOI"])

        stdIOIAll = pd.DataFrame(columns=["Trail", "Std IOI"])
        stdIOI75BPM = pd.DataFrame(columns=["Trail", "Std IOI"])
        stdIOI100BPM = pd.DataFrame(columns=["Trail", "Std IOI"])

        contourAll = pd.DataFrame()
        contour75BPM = pd.DataFrame()
        contour100BPM = pd.DataFrame()

        # </editor-fold>

        # pull out the raw data from text files in target folder
        for participant in self.fileDict.keys():

            # sort the list of filename into a order from trail one to Trail four (increasing order)
            for fileName in self.fileDict[participant]:

                # <editor-fold desc="Preprocessing Unit (get the data and the file name)">
                # split the file name into
                fileNameSplitList = fileName.split("_")

                # get the data by reading the local file
                filePath = os.path.join(self.dataFolderPath, fileName)

                # get the file name without .txt
                reformattedFileName = fileNameSplitList[0] + "_" + fileNameSplitList[1] + "_" + fileNameSplitList[2]
                # read the txt file and generate a data frame
                fileData = pd.read_csv(filePath, sep="\t", header=None, names=[reformattedFileName], nrows=25,
                                       usecols=[0])
                # </editor-fold>

                # <editor-fold desc="Calculation Unit">
                # <editor-fold desc="Calculate IOI">

                # Calculate IOI for each data
                IOIDataFrame = self.differenceCalculation(fileData, fileName)

                # </editor-fold>

                # <editor-fold desc="Calculate meanIOI">
                meanIOI = IOIDataFrame.mean(axis=1)
                meanIOIDF = pd.DataFrame(columns=["Trail", "Mean IOI"])
                meanIOIDF["Trail"] = [reformattedFileName]
                meanIOIDF["Mean IOI"] = meanIOI
                # </editor-fold>

                # <editor-fold desc="Calculate stdIOI (standard Deviation)">

                # Calculate Standard Deviation for each data
                stdIOI = IOIDataFrame.std()
                stdIOIAllDF = pd.DataFrame(columns=["Trail", "Std IOI"])
                stdIOIAllDF["Trail"] = [reformattedFileName]
                stdIOIAllDF["Std IOI"] = stdIOI.values

                # </editor-fold>

                # <editor-fold desc="Calculate contour">

                # Calculate contour
                if fileNameSplitList[1] == "75":
                    preContour = IOIDataFrame - 0.8
                else:
                    preContour = IOIDataFrame - 0.6

                contour = self.differenceCalculation(preContour, fileName)

                # </editor-fold>
                # </editor-fold>

                # <editor-fold desc="Classification unit">
                # <editor-fold desc="All data (record data in dictionaries)">
                dataAll = pd.concat((dataAll, fileData), axis=1)
                IOIAll = pd.concat((IOIAll, IOIDataFrame), axis=1)
                contourAll = pd.concat((contourAll, contour), axis=1)
                meanIOIAll = pd.concat((meanIOIAll, meanIOIDF), axis=0, ignore_index=True)
                stdIOIAll = pd.concat((stdIOIAll, stdIOIAllDF), axis=0, ignore_index=True)
                # </editor-fold>

                # <editor-fold desc="75BPM Data">
                # if the BPM of the file is 75, classify it into 75BPM
                if fileNameSplitList[1] == "75":
                    data75BPM = pd.concat((data75BPM, fileData), axis=1)
                    IOI75BPM = pd.concat((IOI75BPM, IOIDataFrame), axis=1)
                    contour75BPM = pd.concat((contour75BPM, contour), axis=1)
                    meanIOI75BPM = pd.concat((meanIOI75BPM, meanIOIDF), axis=0, ignore_index=True)
                    stdIOI75BPM = pd.concat((stdIOI75BPM, meanIOIDF), axis=0, ignore_index=True)
                # </editor-fold>

                # <editor-fold desc="100BPM Data">
                # if the BPM of the file is 100, classify it into 100BPM
                else:
                    data100BPM = pd.concat((data100BPM, fileData), axis=1)
                    IOI100BPM = pd.concat((IOI100BPM, IOIDataFrame), axis=1)
                    contour100BPM = pd.concat((contour100BPM, contour), axis=1)
                    meanIOI100BPM = pd.concat((meanIOI100BPM, meanIOI), axis=0, ignore_index=True)
                    stdIOI100BPM = pd.concat((stdIOI100BPM, stdIOI),axis=0, ignore_index=True)
                # </editor-fold>
                # </editor-fold>

        # <editor-fold desc="Data saving Unit">

        # save data
        # save raw data into self.rawData
        raw_data = {"data": {"dataAll": dataAll, "data75BPM": data75BPM, "data100BPM": data100BPM}}
        processed_data = {
            "IOI": {"IOIAll": IOIAll, "IOI75BPM": IOI75BPM, "IOI100BPM": IOI100BPM},
            "meanIOI": {"meanIOIAll": meanIOIAll, "meanIOI75BPM": meanIOI75BPM, "meanIOI100BPM": meanIOI100BPM},
            "stdIOI": {"stdIOIAll": stdIOIAll, "stdIOI75BPM":stdIOI75BPM, "stdIOI100BPM": stdIOI100BPM},
            "contour": {"contourAll": contourAll, "contour75BPM": contour75BPM, "contour100BPM": contour100BPM}
        }

        # </editor-fold>

        self.setRawData(raw_data)
        self.setProcessedData(processed_data)

    @staticmethod
    def dataframeIntoXLSX(data, worksheetName):
        """
        This method is to put dataframe from storage dictionary into xlsx sheet

        :param worksheetName:
        :param data: a DataFrame indicate the data
        :return:
        """

        for r in dataframe_to_rows(data, index=True, header=True):
            worksheetName.append(r)


    def generateXlsxFile(self):
        """
        This method is to create a xlsx file that contains all data and processed data

        :return:
        """

        # create a new workbook
        wb = opx.Workbook()

        # <editor-fold desc="sheet raw data">
        rawDataSheet = wb.create_sheet("Raw Data")
        rawDataSheet.title = "Raw Data"
        # </editor-fold>




    def Runner(self):
        """
        Run the whole program


        :return: successfully generated.
        """
        # first check if the classifyMethod is correct or not
        self.renameFile()
        self.generateFileDict()
        self.sortingTappingData_BPM()

































































