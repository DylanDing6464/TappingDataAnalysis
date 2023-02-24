# @author: Dylan Ding
# Date: 1/24/2022
"""
pyautogui
This product includes software developed by
Al Sweigart

Visit https://github.com/asweigart/pyautogui/blob/master/LICENSE.txt for more information of XLWT Package license
"""
import pyautogui as pg
import OpenBeatFinderScript as OBFS


def exportLabel(fileButtonCoordinate, exportButtonCoordinate, moveTowordsLeftCoordinate, labelButtonCoordinate):
    FBC = fileButtonCoordinate
    EBC = exportButtonCoordinate
    MTLC = moveTowordsLeftCoordinate
    LBC = labelButtonCoordinate

    # OBFS.switchWindows()
    # save the file first
    saveFile()

    # Click on File
    pg.moveTo(FBC[0], FBC[1])
    pg.click()

    # Select export
    pg.moveTo(EBC[0], EBC[1])
    pg.click(interval=0.005)

    # Select lable
    # Mouse Curser Move to left
    pg.moveTo(MTLC[0], MTLC[1])
    # Select
    pg.moveTo(LBC[0], LBC[1])
    pg.click()


def saveFile():
    pg.keyDown("ctrl")
    pg.press("s")
    pg.keyUp("ctrl")


if __name__ == '__main__':
    fileButtonCoordinate = [8, 43]
    exportButtonCoordinate = [177, 230]
    moveTowordsLeftCoordinate = [426, 224]
    labelButtonCoordinate = [366, 363]

    exportLabel(fileButtonCoordinate, exportButtonCoordinate, moveTowordsLeftCoordinate, labelButtonCoordinate)
