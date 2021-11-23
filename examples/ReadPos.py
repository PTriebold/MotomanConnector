from ..MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one

mh = MotomanConnector() #Create Connector
mh.connectMH() #Connect
print(mh.getJointAnglesMH()) #Get the Joint angles and print them
mh.disconnectMH()