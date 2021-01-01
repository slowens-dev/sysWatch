#!/usr/bin/python3
from win32gui import GetWindowText, GetForegroundWindow;
from _sql_functions_ import resetSqlRecord, setStartTime, setEndTime, postSqlRecord, closeSqlConnection,\
        initSql, sqlSetWindowTitle, sqlSetWindowPid
from _listener_functions_ import initListeners
from _globals_ import *


def postRecord():
    global record
    if (record != ""): 
        record = setEndTime();
        postSqlRecord();

def resetRecord():
    global record
    resetSqlRecord();
    record = setStartTime();

def checkActiveWindow():
    global active_window_title, active_pid;
    if (active_pid != GetForegroundWindow()):
        active_pid = GetForegroundWindow();
        sqlSetWindowPid(active_pid);
        if active_window_title != GetWindowText(GetForegroundWindow()):
            active_window_title  = GetWindowText(GetForegroundWindow());
            sqlSetWindowTitle(active_window_title);
            if (active_window_title not in ignore_titles):
                postRecord();
                resetRecord();
