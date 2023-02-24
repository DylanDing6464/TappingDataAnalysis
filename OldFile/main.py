# @author: Dylan Ding
# Date: 1/25/2022
import os
# need to install(commond in cmd): pip install xlwt
# it is an open sourse package (https://groups.google.com/g/python-excel/c/P6TjJgFVjMI/m/g8d0eWxTBQAJ)
# xlwt is a fork of the pyExcelerator package, which was developed by Roman V. Kiseliov
import xlwt
import statistics


def ClassifyFiles(dataFolderPath):
    """
    This function is to classify file names of files from the target folder (where store the txt files)(path) into a dictionary

    @param dataFolderPath:  the path(location) of the target folder
    @return fileClassifiedDict:
    """
    # output the file names within the target folder
    fileList = os.listdir(dataFolderPath)

    classifiedNameDict = {}
    for file in fileList:
        fileNameSeparate = file.split("_")
        FCDList = classifiedNameDict.keys()
        participantName = fileNameSeparate[0]
        if participantName in FCDList:
            classifiedNameDict[participantName].append(file)
        else:
            classifiedNameDict[participantName] = [file]
    return classifiedNameDict


def createDataFile(dataFolderPath, fileDict, saveAddress):
    """
        This function is to generate a exccel file
    :param dataFolderPath:
    :param fileDict:
    :param saveAddress:
    :return:
    """
    # create a new excel file
    dylanData = xlwt.Workbook()
    dataWorksheet = dylanData.add_sheet("Sheet1")
    containFirstEightBeat = True

    # the list f the fileDict's keys
    fileDictKeyList = list(fileDict.keys())

    for participantIndex in range(len(fileDictKeyList)):

        # participant's CodeName
        participantCodeName = fileDictKeyList[participantIndex]

        # the list of name of trail
        trailList = fileDict[participantCodeName]

        for trialIndex in range(len(trailList)):

            # the file name with its format (.txt)
            trailFile = trailList[trialIndex]
            with open(os.path.join(dataFolderPath, trailFile))as dataTxt:

                # Header setting process
                # set header
                fileName = trailFile.strip(".txt")
                header = [fileName, 'IOI', 'Mean IOI', 'SD']
                trailNumber = int(fileName[-1])

                # create Pattern to add color to a cell
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                """
                0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
                6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow, 
                20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
                """
                pattern.pattern_fore_colour = 5
                cellColor = xlwt.XFStyle()
                cellColor.pattern = pattern

                # write the header into excel file
                # 30 is the total amount of row of one trail
                headerRow = 30 * participantIndex
                for i in range(len(header)):
                    dataWorksheet.write(headerRow, 4 * (trailNumber - 1) + i, header[i], cellColor)

                # Setting content
                dataAmountCounter = 0

                # content storage list area
                timeContentStoreList = []
                IOIContentStoreList = []

                while True:
                    # condition to stop the loop
                    line = dataTxt.readline()
                    if not line:
                        break
                    if dataAmountCounter == 25:
                        break

                    # Content under the Column trail name
                    # get the time of each beat occurs
                    line = line.strip('\n')
                    line = line.split("	")
                    timeOfBeat = float(line[0])
                    # put timeOfBeat into a list for IOI calculation using
                    timeContentStoreList.append(timeOfBeat)

                    # put timeOfBeat into cell (in excel)
                    timeRow = (30 * participantIndex) + dataAmountCounter + 1
                    timeColumn = 4 * (trailNumber - 1)
                    # write the timeofBeat into excel file
                    dataWorksheet.write(timeRow, timeColumn, timeOfBeat)

                    # Content under the Column IOI
                    if dataAmountCounter >= 1 and timeContentStoreList[dataAmountCounter]:
                        IOIRow = (30 * participantIndex) + dataAmountCounter
                        IOIColumn = timeColumn + 1

                        # Calculate the IOI
                        IOIContent = timeContentStoreList[dataAmountCounter] - timeContentStoreList[
                            dataAmountCounter - 1]
                        IOIContentStoreList.append(IOIContent)
                        # write the IOI into excel file
                        dataWorksheet.write(IOIRow, IOIColumn, IOIContent)

                    # counter self-add area
                    dataAmountCounter += 1

                # Content under the Column MeanIOI
                sumIOI = 0
                for IOI in IOIContentStoreList:
                    sumIOI += IOI

                meanIOIRow = headerRow + 1
                meanIOIContent = sumIOI / len(IOIContentStoreList)
                dataWorksheet.write(meanIOIRow, 4 * (trailNumber - 1) + 2, meanIOIContent)

                # Content under the Column DS
                SDRow = headerRow + 1
                SDContent = statistics.stdev(IOIContentStoreList)
                dataWorksheet.write(SDRow, 4 * (trailNumber - 1) + 3, SDContent)

                # save the excel file at the location
                dylanData.save(saveAddress)



if __name__ == '__main__':
    # Where data(txt file from Audacity) are stored
    dataFolderPath = r"C:\Users\Dylan Ding\Desktop\Tapping data"
    saveAddress = r"C:\Users\Dylan Ding\Desktop\SortedData\Dylan_Data.xls"
    classifiedDict = ClassifyFiles(dataFolderPath)

    createDataFile(dataFolderPath, classifiedDict,saveAddress   )
