from ..MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one

mh = MotomanConnector() #Create connector
mh.connectMH()  #Connect
mh.WriteVariableMH(1,4,200) #Write integer 200 to I004 on the controller
mh.disconnectMH() #Disconnect