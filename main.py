import serial
import io
import time
ser = serial.Serial('COM3', timeout=None, baudrate=56000, xonxoff=False, rtscts=False, dsrdtr=False) 


print("connected to: " + ser.portstr)

line = []
ClickDelay = 1
DoubleClick = 0
DetectTime = 0
diameter = 0
###
scalePicth = 0.5
scaleRoll = 0.5
scaleYaw = 0.5
mode = 1
cc = 0
AngeleTreshHold = 1
while True:
    for line in ser.readlines(15):
        try: 
            lineArray = line.decode("utf-8").split()
            if(len(lineArray) == 8):
                pedal = float(lineArray[7])
                if(pedal == 0):
                    cc = 0
                    ZeroP = float(lineArray[1])
                    ZeroR = float(lineArray[3])
                    ZeroY = float(lineArray[5])
                    if(DoubleClick == 1):
                        DetectTime = time.time()
                        DoubleClick = 0

                if(pedal == 1):
                    if(time.time() - DetectTime < ClickDelay):
                        pedal = 2
                        cc = 1

                if(pedal == 1 and cc == 0):
                    DoubleClick = 1
                    picth = float(lineArray[1]) - ZeroP
                    row = float(lineArray[3]) - ZeroR
                    yaw = float(lineArray[5]) - ZeroY

                    #### mode 1
                    if(mode == 1):     
                        Vx = picth * scalePicth
                        Vy = row * scaleRoll
                        Vz = yaw * scaleYaw
                        
                        # if(Vx < AngeleTreshHold ):
                        #     Vx = 0
                        # if(Vy < AngeleTreshHold):
                        #     Vy = 0
                        # if(Vz < AngeleTreshHold):
                        #     Vz = 0
                        print("Vx = %.2f | Vy = %.2f | Vz = %.2f" % (Vx, Vy, Vz))
                        
                    #### mode 2
                    if(mode == 2):     
                        Vx = picth * scalePicth
                        Vy = row * scaleRoll
                        Vz = yaw * scaleYaw  
                        if(Vx < AngeleTreshHold ):
                            Vx = 0
                        if(Vy < AngeleTreshHold):
                            Vy = 0
                        if(Vz < AngeleTreshHold):
                            Vz = 0  
                    #### mode 3
                    if(mode == 3):     
                        Vx = picth * scalePicth
                        Vy = row * scaleRoll
                        Vz = yaw * scaleYaw
                        if(Vx < AngeleTreshHold ):
                            Vx = 0
                        if(Vy < AngeleTreshHold):
                            Vy = 0
                        if(Vz < AngeleTreshHold):
                            Vz = 0
                    # print(picth)

                if(pedal == 2 ) :

                    print('icerde')
                    
                    Vx = 0
                    Vy = 0
                    Vz = 0
                    #### mode 1
                    if(mode == 1): 
                        diameter = diameter + (picth * scalePicth)
                    #### mode 2
                    if(mode == 2):
                        diameter = diameter + (picth * scaleYaw)
                    #### mode 3
                    if(mode == 3): 
                        diameter = diameter + (picth * scaleRoll)
        except:
            print("An exception occurred")
        
        
ser.close()