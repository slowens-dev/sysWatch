#!/usr/bin/python3
from _globals_ import *
from sqlite3 import connect
from time import time, localtime;
import hashlib
import os


##INIT##
def initSqlConnection():
    global sql_conn
    sql_conn = connect(os.path.dirname(os.path.abspath(__file__))+"/data.db");
def initSqlController():
    global sql_ctrl;
    sql_ctrl = sql_conn.cursor();
def initSql():
    global sql_ctrl, sql_record;
    initSqlConnection();
    initSqlController();
    sql_ctrl.execute("CREATE TABLE IF NOT EXISTS usage(year INT, month INT, day INT, date DATE,start_hour INT, start_minutes INT, start_seconds INT, start_time TIME, window_pid INT, window_title TEXT, mouse_record TEXT, key_record TEXT, combined_record TEXT, end_hour INT, end_minutes INT, end_seconds INT, end_time TIME, username TEXT)");
    sql_ctrl.execute("CREATE TABLE IF NOT EXISTS accounts(username TEXT NOT NULL PRIMARY KEY UNIQUE, password TEXT NOT NULL )")
    sql_record = {"year":0, "month":0, "day":0, "date":"", "start_hour":0, "start_minutes":0, "start_seconds":0, "start_time":"", "window_pid":0, "window_title":"","mouse_record":"", "key_record":"","combined_record":"", "end_hour":0, "end_minutes":0, "end_seconds":0, "end_time":"", "username":"UNKNOWN"};
  ##CLOSE##
def closeSqlController():
    global sql_ctrl;
    sql_ctrl.close();
def closeSqlConnection():
    global sql_conn
    sql_conn.close();
def closeSql():
    postSqlRecord()
    closeSqlConnection();
   
    ##USAGE##
def resetSqlRecord():
    global sql_record;
    sql_record["window_pid"] = 0;
    sql_record["window_title"] = "";
    sql_record["mouse_record"] = "";
    sql_record["key_record"] = "";
    sql_record["combined_record"] = "";
def postSqlRecord():
    global sql_conn, sql_ctrl;
    initSqlController();
    sql_insert_string = "INSERT INTO usage VALUES({},{},{},'{}',{},{},{},'{}',{},'{}','{}','{}','{}',{},{},{},'{}','{}')".format(\
                sql_record["year"], sql_record["month"], sql_record["day"], sql_record["date"],\
                sql_record["start_hour"],sql_record["start_minutes"], sql_record["start_seconds"], sql_record["start_time"],
                sql_record["window_pid"],sql_record["window_title"],sql_record["mouse_record"], sql_record["key_record"],\
                sql_record["combined_record"], sql_record["end_hour"], sql_record["end_minutes"], sql_record["end_seconds"],\
                sql_record["end_time"], sql_record["username"]);
    sql_ctrl.execute(sql_insert_string);	
    sql_conn.commit();
    closeSqlController();

def sqlSetWindowTitle(title):
    sql_record["window_title"] = title;
def sqlSetWindowPid(pid):
    sql_record["window_pid"] = pid;
def setStartTime():
    global sql_record;
    tm = localtime(time());
    timeString = "{}:{}:{} ".format( tm.tm_hour, tm.tm_min, tm.tm_sec);
    dateString = "{}/{}/{}".format(tm.tm_mon, tm.tm_mday, tm.tm_year);
    sql_record["date"] = dateString;
    sql_record["year"] = tm.tm_year;
    sql_record["month"] = tm.tm_mon;
    sql_record["day"] = tm.tm_mday;
    sql_record["start_time"] = timeString;
    sql_record["start_hour"] = tm.tm_hour;
    sql_record["start_minutes"] = tm.tm_min;
    sql_record["start_seconds"] = tm.tm_sec;
def setEndTime():
    global sql_record;
    tm = localtime(time());
    timeString = "{}:{}:{} ".format( tm.tm_hour, tm.tm_min, tm.tm_sec);
    sql_record["end_time"] = timeString;
    sql_record["end_hour"] = tm.tm_hour;
    sql_record["end_minutes"] = tm.tm_min;
    sql_record["end_seconds"] = tm.tm_sec;
def sqlKeyRecordAppend( string ):
        global sql_record;
        sql_record["key_record"] += string;
def sqlMouseRecordAppend( string ):
        global sql_record;
        sql_record["mouse_record"] += string;
def sqlCombinedRecordAppend( string ):
    global sql_record;
    sql_record["combined_record"] += string;
def sqlAppendActiveUser( user ):
        sql_record["username"] = user

def sqlGetActionsByUser(name:str):
    initSql()
    sql_query_string = "select * from usage where username='{}'".format(name);
    sql_ctrl.execute(sql_query_string);
    rows = sql_ctrl.fetchall();
    return rows
def sqlGetUniqueApplicationsByUser(name:str):
    initSql()
    sql_query_string = "select distinct window_pid, window_title from usage where username='{}'".format(name);
    sql_ctrl.execute(sql_query_string);
    rows = sql_ctrl.fetchall()
    return rows;

    ##ACCOUNTS##
def makePasswordHash(password: str) -> str:
    return hashlib.sha256(str.encode(password)).hexdigest()
def sqlAddUserAccount(name:str, password:str) -> None:
    global sql_ctrl, sql_conn
    password_hash = makePasswordHash(password)
    initSql()

    sql_insert_string = "INSERT INTO accounts VALUES('{}','{}')".format(name, password_hash)
    sql_ctrl.execute(sql_insert_string);	
    sql_conn.commit();
    closeSqlController();
    
def sqlVerifyUserLogin(name:str, password:str) -> int:
    password_hash = makePasswordHash(password)
    initSql()
    sql_select_string = "select * from accounts where username='{}'".format(name)
    sql_ctrl.execute(sql_select_string);	
    rows = sql_ctrl.fetchall()
    sql_conn.commit();
    closeSqlController();    
    username_flags =  [ True for (u,p) in (rows) if u == name ] 
    password_flags =  [ True for (u,p) in (rows) if p == password_hash ] 
    if True not in username_flags:
        return -1;#username not found
    else:
        if True not in password_flags:
            return 0;#wrong password
        else:
            return 1;#username and password match


