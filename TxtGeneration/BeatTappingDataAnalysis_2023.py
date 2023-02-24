# @author: Dylan Ding
# Date: 2/22/2022

# need two python libraries
import pandas as pd
import pathlib

"""
This file input the data txt file generated from audacity, and output the IOI into csv file.
"""


def getData(filePath):
    """
    import the data from the txt file, select the 1st column and first 25 rows

    :param filePath: the path to the txt file that mast named in format "[participant index]_[BPM]_[test number]"
    E.g."215_75_t1" and the first column must be the data (timestamps)

    :return: list contain df.diff().drop(0).reset_index(drop=True) is the cleaned up data, which is
    Inter-Onset Interval (IOI) for the first 25 rows and index has been reset;
    fileName.split("_")[1] is the BPM of this data (75BPM or 100BPM)

    :rtype: list
    """

    # get the data (the first column and first 25 rows) from the txt file
    df = pd.read_csv(filePath, sep="\t", header=None, usecols=[0], nrows=25)
    # get the file name
    fileName = filePath.split("\\")[-1].split(".")[0]
    # name the column using the filename
    df.columns = [fileName]

    # df.diff().drop(0).reset_index(drop=True) is the cleaned up data, which is IOI (Inter-Onset Interval) for the
    # first 25 rows and index has been reset.
    # fileName.split("_")[1] is the BPM of this data (75BPM or 100BPM)
    return df.diff().drop(0).reset_index(drop=True), fileName.split("_")[1]


def displayData(filePath):
    """
    display the data
    :param filePath: the path to the file to display
    """
    df = pd.read_csv(filePath)
    print(df)


def outputDataframe(folderPath):
    """
    output two dataframe that contains 75 and 100 BPM data from for all txt files with in the folder at folderPath

    :param folderPath: the folder path to the folder
    :return:    data75BPM records all data with 75 BPM; data75BPM records all data with 100 BPM
    """

    # load folder-path into pathlib
    plfolderPath = pathlib.Path(folderPath)

    # create two null dataframe record 75BOM and 100BPM
    data75BPM = pd.DataFrame()
    data100BPM = pd.DataFrame()

    # for each txt files in the folder; list(plfolderPath.iterdir()) returns the path of each file in the folder
    for txtFile in list(plfolderPath.iterdir()):

        # convert txtFile into string
        txtFileStr = str(txtFile)

        # only select the txt file
        if ".txt" in txtFileStr:
            dataList = getData(txtFileStr)
        # skip the one that is not
        else:
            continue

        # if the txt file is 75BPM, add it to
        if dataList[1] == "75":
            data75BPM = pd.concat([data75BPM, dataList[0]], axis=1)
        # if the txt file is 100BPM
        elif dataList[1] == "100":
            data100BPM = pd.concat([data100BPM, dataList[0]], axis=1)
        # wrong filename
        else:
            print("Wrong fileName")

    # data75BPM records all data with 75 BPM; data75BPM records all data with 100 BPM
    return data75BPM, data100BPM


def dataFrameToCSV(folderPath, savePath, saveName):
    """
    output CSV file containing all data with 75BPM and 100BPM

    :param folderPath: the path to the folder
    :param savePath: where to save
    :param saveName: what name you want to save
    """
    # run get clean data
    dataframeList = outputDataframe(folderPath)

    try:
        dataframeList[0].to_csv(savePath + "\\" + saveName[0] + ".csv")
        dataframeList[1].to_csv(savePath + "\\" + saveName[1] + ".csv")
    # if anything happened print wrong message
    except Exception:
        print("Unable to save")

    print("Success")


if __name__ == '__main__':

    # example code

    # data folder
    folder = r"D:\MyFile\Study\Penn State University Files\Pitch Exploration Lab\Tapping Data\New Data\PSU_Tapping_2"

    savedPath = r"D:\MyFile\Study\Penn State University Files\Pitch Exploration Lab\Tapping Data\New Data\Collection"
    saveFileName = ["PSU_75BPM", "PSU_100BPM"]

    # output csv file with data
    dataFrameToCSV(folder, savedPath, saveFileName)

    displayData(r"D:\MyFile\Study\Penn State University Files\Pitch Exploration Lab\Tapping Data\New Data\Collection\PSU_75BPM.csv")
