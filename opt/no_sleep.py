import requests
import os
from time import sleep
from datetime import datetime

HEROKU_URL = os.environ.get("HEROKU_URL", "http://localhost")
REST_API_PORT = int(os.environ.get("REST_API_PORT", 7878))
SERVER_STATUS_URL = "http://localhost:{}/v2/server/status"
ANTI_IDLE_MODE = int(os.environ.get("ANTI_IDLE", 0)) #0 = off, 1 = always-on, 2 = terraria mode

def wakeUp():
    try:
        requests.get(HEROKU_URL)
    except:
        return 0
        
def getNow():
    return datetime.now().time().replace(microsecond=0)
    
def getActivePlayers():
    try: 
        r = requests.get(SERVER_STATUS_URL.format(REST_API_PORT))
    except:
        return 0
        
    if r.status_code == 200: #Successful Call
        return r.json()["playercount"]
    else:   #REST API not running
        return 0
        
def check():
    sleepTime = 60 * 20 # 20 minutes
    # Off
    if ANTI_IDLE_MODE == 0:
        print("[{}] Going to sleep soon".format(getNow()))
    
    # Always On
    if ANTI_IDLE_MODE == 1:
        print("[{}] Wake up call!".format(getNow()))
        wakeUp()
        
    # Terraria Mode
    if ANTI_IDLE_MODE == 2:
        if getActivePlayers() != 0:
            print("[{}] Wake up call!".format(getNow()))
            wakeUp()
        else:
            print("[{}] No players Online, checking in 3 mins".format(getNow()))
            sleepTime = 60 * 3 # 3 Minutes
        
    sleep(sleepTime) 

#every 20 mins
while True:
    check()
