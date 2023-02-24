# @author: Dylan Ding
# Date: 1/24/2022
"""
pyautogui
This product includes software developed by
Al Sweigart

Visit https://github.com/asweigart/pyautogui/blob/master/LICENSE.txt for more information of XLWT Package license
"""
import pyautogui as pg


def printMCPosition():
    # PrintMouseCursorPosition
    a = pg.position()
    return a


def outPutStr(MCPosition):
    position = MCPosition.split(",")
    MCPositionList = []

    for axis in position:
        numberList = []
        for letter in axis:
            if letter.isnumeric():
                numberList.append(letter)
        number = "".join(numberList)
        MCPositionList.append(number)

    return MCPositionList


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MCPosition = str(printMCPosition())
    MCPositionList = outPutStr(MCPosition)
    for axis in MCPositionList:
        print(axis)
