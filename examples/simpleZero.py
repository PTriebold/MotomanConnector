import time
from ..MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one

mh = MotomanConnector() #Create connector
mh.connectMH() #Connect to Controller
mh.servoMH() #Turn Servo on
mh.moveAngleMH(10,0,0,0,0,0,0) # Move to all Zero

time.sleep(5) #Wait for the move to finish

mh.servoMH(False) #Turn the Servos of
mh.disconnectMH() #Disconnect the Controller