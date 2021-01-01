from signal import signal, SIGINT, SIGTERM
from _sql_functions_ import closeSqlConnection
from _cv_ import closeCV
def interrupt(signal, frame) -> None:
    try:
        closeSqlConnection();
        closeCV();
        exit();
    except:
        print("\n")
        exit();
def terminate(signal, frame) -> None:
    try:
        closeSqlConnection();
        closeCV();
        exit();
    except:
        print("\n")
        exit();
def initSignals():
    signal(SIGINT, interrupt)
    signal(SIGTERM, terminate)

