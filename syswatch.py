from sys import argv, platform, path as syspath
from os import path as ospath
BASE_DIR = ospath.dirname(ospath.abspath(__file__))
LIBS_DIR = BASE_DIR+"/libs/"
syspath.append(LIBS_DIR)
from _signals_ import initSignals
from _sql_functions_ import initSql, closeSql
from _listener_functions_ import initListeners
from _cv_ import initCV, closeCV, getUsersInFrame, getUsersInFrameAndShow, trainModel, addUserImage
from _signals_ import initSignals
from sys import platform
from _globals_ import helpMessage


def initAll():
    initSignals();
    initSql();
    initCV();
    initListeners();
def closeAll():
    closeSql();
    closeCV();
def mainWithCameraShown():
    initAll();
    print("starting app with camera feed shown\n\tpress ESC to close ")
    while 1:
        checkActiveWindow();
        getUsersInFrameAndShow();
    closeAll();
def basicMain():
    initAll();
    print("starting app with camera feed not shown")
    while 1:
        checkActiveWindow();
        getUsersInFrame();
    closeAll();
    
if __name__ == "__main__":
    #verify OS is supported
    if (platform == "win32"):
        from _windows_ import *;
    elif (platform == "linux"):
        from _linux_ import *;
    else:
        print("unsupported operating system");
        exit();
    #show help message if prompted
    if "--help" in argv or "-H" in argv or "-h" in argv:
        helpMessage();
        exit();
    #add user images if prompted
    if "--add-user" in argv or "-au" in argv or "-AU" in argv:
        addUserImage();
        exit()
    #retrain FR model if prompted
    if "--train" in argv or "-T" in argv or "-t" in argv:
        trainModel();
    #run the webserver on port 3000 if prompted
    if "--server" in argv or "-S" in argv or "-s" in argv:
        print("webserver")
        exit()
    #begin runtime : (with camera if prompted)
    if "--camera" in argv or "-C" in argv or "-c" in argv:
        mainWithCameraShown()
    else:
        basicMain();
