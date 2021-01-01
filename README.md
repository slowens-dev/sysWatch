ERRORS or BUGS:
	https://github.com/slowens-dev/sysWatch/issues
	or
	samuel@slowens.com

SysWatch aims to provide a tool for monitoring the activity on a particular machine
it creates an sqlite database of all activity on the machine
each record represents a change in the current "focused" window
each record contains information on the start and end time of the window session
as well as  a full log of key presses, mouse clicks, and mouse scrolls
this activity record is paired with a facial recognition system 
the face of the active user is compared against a facial recognition model
authorized users will take pictures of themselves using the machines designated camera
these images are used to train the recognition model
it is recommended not to upload face images not taken with the camera the app will use
using a different camera may cause recognition errors
if the face is not one of the authorized users the record will show UNKNOWN
if the face is one of the authorized user that user's name will be added to the sql record

the sqlite database resides in the file usage.db
it contains a single table titled:	
	usage
this table contains the following columns:
	year	month	day	date	start_hour	start_minutes	start_seconds	start_time
	window_pid	window_title	mouse_record	key_record	combined_record	
	end_hour	end_minutes	end_seconds	end_time	active_users

INSTALLATION
SysWatch makes use of the following python3 stdlib modules
they should be included in the standard python3 installation

	time
	sqlite3

SysWatch requires the following modules to be installed by the user

>> All Platforms <<
	pip3 install pynput opencv-python opencv-contrib-python

>> Windows-specific <<
	pip3 install pywin32

>> Linux-specific <<
the linux solution does not use a python module
instead it runs the linux tool xdotool from within the python script and works with the output
the python-libxdo module is incomplete and does not have documentation,
it may be incorporated if/when it is a functional and complete module

	apt install xdotool

