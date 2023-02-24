# @author: Dylan Ding
# Date: 1/24/2022
"""
pyautogui
This product includes software developed by
Al Sweigart

Visit https://github.com/asweigart/pyautogui/blob/master/LICENSE.txt for more information of XLWT Package license
"""
import pyautogui as pg





def OpenBeatFinder(analyzeButtonCoordinate, beatFinderButtonCoordinate,startCoordinate):
    ABC = analyzeButtonCoordinate
    BFC = beatFinderButtonCoordinate
    SC = startCoordinate
    # switchWindows()

    # move the bar to the start
    SC = startCoordinate
    pg.moveTo(SC[0], SC[1])
    pg.click()
    pg.click()
    pg.click()
    pg.click()

    selectAll()

    # select Analyze
    # Analyze button coordinate
    pg.moveTo(ABC[0], ABC[1])
    pg.click()

    # select beat finder
    pg.moveTo(BFC[0], BFC[1])
    pg.click()



def switchWindows():
    pg.keyDown("alt")
    pg.press("tab")
    pg.keyUp("alt")


def selectAll():
    pg.keyDown("ctrl")
    pg.press("a")
    pg.keyUp("ctrl")


if __name__ == '__main__':
    startCoordinate = [207, 968]
    analyzeButtonCoordinate = [481, 40]
    beatFinderButtonCoordinate = [481, 196]

    OpenBeatFinder(analyzeButtonCoordinate, beatFinderButtonCoordinate, startCoordinate)
