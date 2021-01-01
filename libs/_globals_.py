
sql_conn = sql_ctrl = None;
sql_record = {"record":""};
ignore_titles = [ "", "Task Switching" ];
active_window_title = active_pid = record = "";
key_listener = mouse_listener = None;

def helpMessage():
    print( "-h -H --help :: show this help message" )
    print( "-t -T --train :: retrain the facial recognition model from libs/user_images/*" )
    print( "-c -C --camera :: run the application with the camera feed shown" )
    print( "-s -S --server :: run the application with the dashboard webserver running on localhost:3000" )
    print( "-au -AU --add-user :: add a user a new user to the system or add new images to an existing user" )



