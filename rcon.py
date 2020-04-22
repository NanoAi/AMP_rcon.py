#!/usr/bin/python3
import json, sys, requests, getpass

# This script is made by NanoAi from Mirai.Red
# With motevation, and support from Xoren.io
# ----
# If you decide to use/modify any of my work please give us some credit! <3

# Set this variable to your port number if you don't want to define the port all the time!
PORT = ""
# Set this variable to define the file your SessionID will be written to.
# This is so you don't have to define it all the time.
WritePath = "/tmp/amp_sessionid"

# API-EndPoints
# You can change this if your not making calls to localhost.
Login = "http://localhost:%port%/API/Core/Login"
SendMessage = "http://localhost:%port%/API/Core/SendConsoleMessage"

# Headers
Headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# Data
Data = {}

if len(sys.argv) <= 0:
	print("Type in `-l` to start, then enter the commands you'd like to run.")

if sys.argv[1].lower()[:2] == "-l":
	Username = len(sys.argv) > 2 and sys.argv[2] or input("Username: ")
	Password = len(sys.argv) > 3 and sys.argv[3] or getpass.getpass("Password: ")

	RememberMe = len(sys.argv) > 4 and sys.argv[4] or str(
		input("Remember Me [ Y / [N] ]: ") ).lower()[:0] == "y"

	Port = PORT or input("Port: ")
	Login = Login.replace( "%port%", Port, 1 )

	# Define the data we want to send.
	Data = { "username": Username, "password": Password,
			"token": "", "rememberMe": str(RememberMe).lower() }

	# Send the post request, and output the response to a variable.
	r = requests.post(url=Login, data=json.dumps( Data ), headers=Headers)

	f = open(WritePath, "w")
	f.write(r.json()['sessionID'])
	f.close()
elif sys.argv[1].lower()[:2] == "-d":
  # Overwite the file, thus removing its contents.
	f = open(WritePath, "w")
	f.write("")
	f.close()
	print("RCON Disconnected.")
else:
	with open(WritePath, 'r') as file:
		key = file.read().replace('\n', '')

	Port = PORT or input("Port: ")
	SendMessage = SendMessage.replace("%port%", Port, 1)

	Data = {'SESSIONID': key, 'message': ' '.join(sys.argv[1:])}
	r = requests.post(url=SendMessage, data=json.dumps(Data), headers=Headers)
