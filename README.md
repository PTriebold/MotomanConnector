# MotomanConnector
Connection to the Motoman Ethernet Server, available on some Yaskawa Motoman Controllers. Tested on DX200 and YRC1000.


# Code

    MotomanConnector(IP = "192.168.255.1", PORT=80, S_pulse = 1341.4, L_pulse = 1341.4, U_pulse = 1341.4, R_pulse = 1000, B_pulse = 1000, T_pulse = 622)

Initalize the Library

| Parameter | type   | Default         | Description                       |
|-----------|--------|-----------------|-----------------------------------|
| IP        | string | "192.168.255.1" | Controller IP                     |
| Port      | int    | 80              | Controller Port                   |
| S_pulse   | float  | 1341.1          | No. Encoder Pulse per ° on Axis S |
| L_pulse   | float  | 1341.1          | No. Encoder Pulse per ° on Axis L |
| U_pulse   | float  | 1341.1          | No. Encoder Pulse per ° on Axis U |
| R_pulse   | float  | 1000            | No. Encoder Pulse per ° on Axis R |
| B_pulse   | float  | 1000            | No. Encoder Pulse per ° on Axis B |
| T_pulse   | float  | 622             | No. Encoder Pulse per ° on Axis T |

    MotomanConnector.connectMH()

Establish a connection to the Robot Controller.
Raises an Exception on an unexpected or no Answer.

    MotomanConnector.disconnectMH()

Drop the connection to the Robot Controller.

    MotomanConnector.getJointAnglesMH()

Read the Joint Angles.

Returns a list of six Joint Angles

    MotomanConnector.getCoordinatesMH(coordinateSystem = 0)

Read the current Position in reference to a selectable coordinate system, **currently Broken on DX Controllers!**

| Parameter        | type | Default | Description                                                        |
|------------------|------|---------|--------------------------------------------------------------------|
| coordinateSystem | int  | 0       | The referenced coordinate System. 0 = Base, 1 = Robot, 2-64 = User |

Returns a list with the current Positional Values

    MotomanConnector.servoMH(state = True)

Turn the Servo motors on/off. Keyswitch needs to be in "REMOTE" Position.

| Parameter | type | Default | Description                                 |
|-----------|------|---------|---------------------------------------------|
| state     | bool | True    | Enable (True) or disable (False) the Servos |

    MotomanConnector.moveAngleMH(speed,S,L,U,R,B,T)

Move the Robot in joint coordinates.  
**CAREFUL** The Robot can get quite Fast, be careful with the speed Values.

| Parameter | type  | Default | Description   |
|-----------|-------|---------|---------------|
| speed     | float | -       | Speed in %    |
| S         | float | -       | S Joint Angle |
| L         | float | -       | L Joint Angle |
| U         | float | -       | U Joint Angle |
| R         | float | -       | R Joint Angle |
| B         | float | -       | B Joint Angle |
| T         | float | -       | T Joint Angle |

    MotomanConnector.WriteVariableMH(type,number,value)

Write a Variable on the controller.

| Parameter | type                  | Default | Description                                                                                                      |
|-----------|-----------------------|---------|------------------------------------------------------------------------------------------------------------------|
| type      | int                   | -       | Type of the Variable \| 0 = Byte, 1 = Integer, 2 = Double, 3 = Real, 7 = String. Other Values raise an exception |
| number    | int                   | -       | Variable Number                                                                                                  |
| value     | byte/int/float/string | -       | Value to be set                                                                                                  |

    MotomanConnector.ReadVariableMH(type,number)

Read a variable from the controller  
Returns the read Value

| Parameter | type | Default | Description                                                                                                      |
|-----------|------|---------|------------------------------------------------------------------------------------------------------------------|
| type      | int  | -       | Type of the Variable \| 0 = Byte, 1 = Integer, 2 = Double, 3 = Real, 7 = String. Other Values raise an exception |
| number    | int  | -       | Variable Number                                                                                                  |

    MotomanConnector.statusMH()

Read the Status bytes from the Robot.  
Returns a list containing the two status Bytes.

    MotomanConnector.readCurrJobMH()

Read the current Job name.  
Returns job name

    MotomanConnector.startJobMH(job)

Start a Job by its name
Returns (d1,d2) ->  
string d1: return of command transaction  
string d2: return of the Payload Transaction


| Parameter | type   | Default | Description             |
|-----------|--------|---------|-------------------------|
| job       | string | -       | Job name which to start |