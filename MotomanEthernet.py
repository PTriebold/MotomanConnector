import socket, time

#######################
# Communication Interface to Motoman Controllers
# Tested on MH24 with DX200
# Tested on 6VX7 with YRC1000
# 
# Philipp Triebold
######################


#MH24 Conversion Values
#S 1341,4 Pulse pro °
#L 1341,4 Pulse pro °
#U 1341,4 Pulse pro °
#R 90° 90000 -> 1000 Pulse pro °
#B 90° 90000 -> 1000 Pulse pro °
#T 90° 56462 -> 622 Pulse pro °

class MotomanConnector:
    def __init__(self,IP = "192.168.255.1", PORT=80, S_pulse = 1341.4, L_pulse = 1341.4, U_pulse = 1341.4, R_pulse = 1000, B_pulse = 1000, T_pulse = 622):
        """Interface for the Ethernet Server Function of various Yaskawa Motoman Controllers

        Args:
            IP (str, optional): IP of the Controller. Defaults to "192.168.255.1".
            PORT (int, optional): Port of the Controller. Defaults to 80.
            S_pulse (float, optional): S-Axis encoder pulses per degree. Defaults to 1341.4.
            L_pulse (float, optional): L-Axis encoder pulses per degree. Defaults to 1341.4.
            U_pulse (float, optional): U-Axis encoder pulses per degree. Defaults to 1341.4.
            R_pulse (float, optional): R-Axis encoder pulses per degree. Defaults to 1000.
            B_pulse (float, optional): B-Axis encoder pulses per degree. Defaults to 1000.
            T_pulse (float, optional): T-Axis encoder pulses per degree. Defaults to 622.
        """

        self.s = socket.socket()
        self.IP = IP
        self.PORT = PORT
        self.S_pulse = S_pulse
        self.L_pulse = L_pulse
        self.U_pulse = U_pulse
        self.R_pulse = R_pulse
        self.B_pulse = B_pulse
        self.T_pulse = T_pulse

    def __sendCMD(self,command,payload):
        """INTERNAL - Internal send Function.

        Args:
            command (string): Command - See Yaskawa documentation
            payload (string): Command payload - empty string if no data should be send. If not empty, remember the <CR> at the end!

        Raises:
            Exception: If the Command does not return an ok, an error is raised

        Returns:
            string data: returned data from command transaction
            string data2: returned data from command payload transaction
        """

        print(command,payload)

        self.s.send(bytes(f"HOSTCTRL_REQUEST {command} {len(payload)}\r\n","utf-8"))
        data = self.s.recv(1024)
        print(f'Received: {repr(data)}')

        if data[:2] != b"OK":
            print(f"COMMAND ({command}) ERROR")
            raise Exception("Yaskawa Error!")

        elif len(payload) > 0:
            self.s.send(bytes(f"{payload}","utf-8"))
        
        data2 = self.s.recv(1024)
        print(f'Received: {repr(data2)}')
        
        return data, data2


    def connectMH(self):
        """Connect to the Motoman controller

        Raises:
            Exception: If the connection does not return OK
        """
        self.s.connect((self.IP,self.PORT))
        self.s.send(b"CONNECT Robot_access Keep-Alive:-1\r\n")
        data = self.s.recv(1024)
        print(f'Received: {repr(data)}')
        if data[:2] != b"OK":
            print("Connection Faulty!")
            raise Exception("Yaskawa Connection Error!")

    def disconnectMH(self): #Verbindung Trennen
        """Disconnect from the Controller
        """
        self.s.close()

    def getJointAnglesMH(self): #Encoderpulse ausrechnen und als Winkel umgerechnet ausgeben
        """Read the Joint Angles

        Returns:
            list: list of the six joint angles
        """
        d1, d2 = self.__sendCMD("RPOSJ","")

        data2_str = d2.decode("utf-8").replace("\r","").split(",")

        data2_arr = [int(data2_str[0])/self.S_pulse,int(data2_str[1])/self.L_pulse,int(data2_str[2])/self.U_pulse,int(data2_str[3])/self.R_pulse,int(data2_str[4])/self.B_pulse,int(data2_str[5])/self.T_pulse]
        return data2_arr

    def getCoordinatesMH(self,coordinateSystem = 0): #Der Controller ist irgendwie nicht in der lage die koordinaten zu
        """Read the current Position in reference to a selectable coordinate system, currently Broken on DX Controllers!

        Args:
            coordinateSystem (int, optional): The refereced coordinate System. 0 = Base, 1 = Robot, 2-64 = User. Defaults to 0.

        Returns:
            list: List with the current Positional Values
        """
        d1, d2 = self.__sendCMD("RPOSC","0,0\r")
        return d2.decode("utf-8").replace("\r","").split(",")

    def servoMH(self, state = True): #Servo an/aus-schalten
        """Turn on/off the Servo motors

        Args:
            state (bool, optional): Powerstate to set the servos to. Defaults to True.
        """
        time.sleep(0.1)
        self.__sendCMD("SVON",f"{1 if state else 0}\r")


    def moveAngleMH(self, speed,S,L,U,R,B,T):
        """Move the Robot in joint coordinates

        Args:
            speed (float): Speed value - 0% - 100% - It's not recomended to use more than 50%!
            S (float): S angle
            L (float): L angle
            U (float): U angle
            R (float): R angle
            B (float): B angle
            T (float): T angle
        """
        cmd = f"{speed},{int(S*1341.4)},{int(L*1341.4)},{int(U*1341.4)},{int(R*1000)},{int(B*1000)},{int(T*622)},0,0,0,0,0,0,0\r" #die gegebenen Winkel in Encoderpulse umrechnen
        self.__sendCMD("PMOVJ",cmd)


    def WriteVariableMH(self,type,number,value):
        """Write a Variable on the controller

        Args:
            type (int): Type of the Variable | 0 = Byte, 1 = Integer, 2 = Double, 3 = Real, 7 = String. Other Values raise an exception
            number (int): variable numer
            value (byte/int/float/string): Variable Value

        Raises:
            Exception: Exception if the type is not allowed
        """
        cmd = f"{type},{number},{value}\r"
        if type in [0,1,2,3,7]: self.__sendCMD("LOADV",cmd) #Überprüfen ob der variablentyp in den "einfach"-schreibbaren ist
        else: raise Exception("Variable Type not supported!")

    def ReadVariableMH(self,type,number):
        """Read a variable from the controller

        Args:
            type (int): Type of the Variable
            number (int): Variable Number

        Returns:
            string: Variable Value
        """
        d1,d2 = self.__sendCMD("SAVEV",f"{type},{number}\r")
        return d2.decode("utf-8").replace("\r","")

    def statusMH(self):
        """Read the Status bytes from the Robot

        Returns:
            list: list containing the two status bytes
        """
        d1,d2 = self.__sendCMD("RSTATS","")
        status = d2.decode("utf-8").replace("\r","").split(",")
        return status

    def readCurrJobMH(self):
        """Read the current Job Name

        Returns:
            string: Current Job Name
        """
        d1,d2 = self.__sendCMD("RJSEQ","")
        return d2
    
    def startJobMH(self,job):
        """Start a Job by its name

        Args:
            job (string): Job Name which to start

        Returns:
            string d1: return of command transaction
            string d2: return of the Payload Transaction
        """
        d1,d2 = self.__sendCMD("START",f"{job}\r")
        return d1, d2

if __name__ == "__main__":
    mh = MotomanConnector(IP="192.168.178.10")
    mh.connectMH()

    # # # #MH24 Commandos hier

    mh.disconnectMH()