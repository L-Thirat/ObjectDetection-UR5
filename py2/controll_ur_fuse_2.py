'''
###### CREATE :: TERUS LIMSURUT ######

## manual ##
HOST = "192.168.1.8" = Left
HOST = "192.168.1.9" = Right

digital_port 1 = pick

## code ##
pick = control(pick)
move = control(move,x,y,z,ro,pi,ya,a,v)
'''

import socket
import time

class controll():
    def __init__(self,Hand):
        if Hand=="L":
            self.HOST = "192.168.1.8"  # Left = L
        else: self.HOST = "192.168.1.9" # Right = R
        self.PORT = 30002  # The same port as used by the server
        self.PORT_502 = 502
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def pick(self):
        self.s.connect((self.HOST, self.PORT))
        cmd = "set_digital_out(1,True)" + "\n"
        self.s.send(cmd.encode('utf-8'))

    def drop(self):
        self.s.connect((self.HOST, self.PORT))
        cmd = "set_digital_out(1,False)" + "\n"
        self.s.send(cmd.encode('utf-8'))

    def move(self,x,y,z,ro,pi,ya):
        self.s.connect((self.HOST, self.PORT))
        x_old = x
        y_old = y
        z_old = z
        x=str(x/1000.0)
        y=str(y/1000.0)
        z=str(z/1000.0)
        ro=str(ro)
        pi=str(pi)
        ya=str(ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        while self.read_pos() == (x_old,y_old,z_old,ro,pi,ya):
            break
        time.sleep(5)

    def read_pos(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((self.HOST, self.PORT_502))
            time.sleep(0.05)
            print ""
            reg_400 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x90\x00\x01") #request data from register 128-133 (cartisian data)
            reg_400 = s.recv(1024)
            reg_400 = reg_400.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_400 = reg_400.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_400 == "":
                reg_400 = "0000"
            reg_400_i = int(reg_400,16)
            if reg_400_i < 32768:
                reg_400_f = float(reg_400_i)/10
            elif reg_400_i > 32767:
                reg_400_i = 65535 - reg_400_i
                reg_400_f = float(reg_400_i)/10*-1
            print "X = ",reg_400_f
            x = reg_400_f

            reg_401 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x91\x00\x01") #request data from register 128-133 (cartisian data)
            reg_401 = s.recv(1024)
            reg_401 = reg_401.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_401 = reg_401.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_401 == "":
                reg_401 = "0000"
            reg_401_i = int(reg_401,16)
            if reg_401_i < 32768:
                reg_401_f = float(reg_401_i)/10
            elif reg_401_i > 32767:
                reg_401_i = 65535 - reg_401_i
                reg_401_f = float(reg_401_i)/10*-1
            print "Y = ",reg_401_f
            y = reg_401_f

            reg_402 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x92\x00\x01") #request data from register 128-133 (cartisian data)
            reg_402 = s.recv(1024)
            reg_402 = reg_402.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_402 = reg_402.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_402 == "":
                reg_402 = "0000"
            reg_402_i = int(reg_402,16)
            if reg_402_i < 32768:
                reg_402_f = float(reg_402_i)/10
            if reg_402_i > 32767:
                reg_402_i = 65535 - reg_402_i
                reg_402_f = float(reg_402_i)/10*-1
            print "Z = ",reg_402_f
            z = reg_402_f

            reg_403 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x93\x00\x01") #request data from register 128-133 (cartisian data)
            reg_403 = s.recv(1024)
            reg_403 = reg_403.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_403 = reg_403.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_403 == "":
                reg_403 = "0000"
            reg_403_i = int(reg_403,16)
            if reg_403_i < 32768:
                reg_403_f = float(reg_403_i)/1000
            if reg_403_i > 32767:
                reg_403_i = 65535 - reg_403_i
                reg_403_f = float(reg_403_i)/1000*-1
            print "Rx = ",reg_403_f
            ro = reg_403_f

            reg_404 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x94\x00\x01") #request data from register 128-133 (cartisian data)
            reg_404 = s.recv(1024)
            reg_404 = reg_404.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_404 = reg_404.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_404 == "":
                reg_404 = "0000"
            reg_404_i = int(reg_404,16)
            if reg_404_i < 32768:
                reg_404_f = float(reg_404_i)/1000
            if reg_404_i > 32767:
                reg_404_i = 65535 - reg_404_i
                reg_404_f = float(reg_404_i)/1000*-1
            print "Ry = ",reg_404_f
            pi = reg_404_f

            reg_405 = ""
            s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x95\x00\x01") #request data from register 128-133 (cartisian data)
            reg_405 = s.recv(1024)
            reg_405 = reg_405.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
            reg_405 = reg_405.encode("hex") #convert the data from \x hex notation to plain hex
            if reg_405 == "":
                reg_405 = "0000"
            reg_405_i = int(reg_405,16)
            if reg_405_i < 32768:
                reg_405_f = float(reg_405_i)/1000
            if reg_405_i > 32767:
                reg_405_i = 65535 - reg_405_i
                reg_405_f = float(reg_405_i)/1000*-1
            print "Rz = ",reg_405_f
            ya = reg_405_f

            time.sleep(5.00)
            home_status = 1
            program_run = 0
            s.close()
        except socket.error as socketerror:
            print("Error: ", socketerror)
        return (x,y,z,ro,pi,ya)

    def close_sv(self):
        self.s.close()

class path_action(controll):
    def pick2jig(self,x,y):
        ##step 1
        x = str(x / 1000.0)
        y = str(y / 1000.0)
        z = str(114.2 / 1000.0)
        ro = str(1.58)
        pi = str(0.56)
        ya = str(-0.54)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        #step2
        self.pick()
        time.sleep(1)

        #step3
        z = str(336 / 1000.0)
        print(x, y, z, ro, pi, ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(3)

        #step4
        x = str(-275 / 1000.0)
        y = str(-455 / 1000.0)
        z = str(294 / 1000.0)
        ro = str(1.9)
        pi = str(0.8)
        ya = str(-1.15)
        print(x, y, z, ro, pi, ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(5)

        #step5
        x = str(-380 / 1000.0)
        y = str(-341 / 1000.0)
        z = str(188 / 1000.0)
        ro = str(2.53)
        pi = str(0.7)
        ya = str(-1)
        print(x, y, z, ro, pi, ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(3)

        #step6
        x = str(-396 / 1000.0)
        y = str(-326 / 1000.0)
        z = str(104 / 1000.0)
        ro = str(2.58)
        pi = str(0.6)
        ya = str(-1.21)
        print(x, y, z, ro, pi, ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(5)

        #step7
        self.drop()
        time.sleep(1)

        #step8
        x = str(40 / 1000.0)
        y = str(-499 / 1000.0)
        z = str(331 / 1000.0)
        ro = str(1.64)
        pi = str(0.7)
        ya = str(-1)
        print(x, y, z, ro, pi, ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))

        #step9 :finish
        self.close_sv()
        #####################finish#############

    def jig2drop(self,x_in,y_in):
        ##step 1 : init jig pos
        x = str(-100 / 1000.0)
        y = str(-367 / 1000.0)
        z = str(159.7 / 1000.0)
        ro = str(1.6)
        pi = str(0.36)
        ya = str(-0.835)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        ##step 2
        x = str(-230.8 / 1000.0)
        y = str(-363.85 / 1000.0)
        z = str(163 / 1000.0)
        ro = str(1.877)
        pi = str(1.046)
        ya = str(0.52)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        ##step 3 :case regtangular
        x = str(-229.75 / 1000.0)
        y = str(-327 / 1000.0)
        z = str(108.2 / 1000.0)
        ro = str(1.8)
        pi = str(1.17)
        ya = str(0.556)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        #step4
        self.pick()
        time.sleep(1)

        ##step 5
        x = str(232.79/ 1000.0)
        y = str(-343 / 1000.0)
        z = str(268.1 / 1000.0)
        ro = str(1.395)
        pi = str(1.084)
        ya = str(0.354)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        ##step 6
        x = str(x_in/ 1000.0)
        y = str(y_in / 1000.0)
        z = str(268.1 / 1000.0)
        ro = str(1.395)
        pi = str(1.084)
        ya = str(0.354)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        ##step 7
        x = str(232.79/ 1000.0)
        y = str(-343 / 1000.0)
        z = str(268.1 / 1000.0)
        ro = str(1.395)
        pi = str(1.084)
        ya = str(0.354)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        #step8
        self.drop()
        time.sleep(1)

        #step9
        x = str(-100/ 1000.0)
        y = str(-367 / 1000.0)
        z = str(159.7 / 1000.0)
        ro = str(1.6)
        pi = str(0.36)
        ya = str(-0.835)
        print(x, y, z, ro, pi, ya)
        # move = "movej(p[-0.30, -0.30, 0.40, 1.30, 0.80, -0.08],a=1.10, v=0.54)" + "\n"
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=1,v=0.5)" + "\n"
        self.s.send(mm.encode('utf-8'))
        time.sleep(10)

        #step10 :finish
        self.close_sv()


'''test jig2drop'''


'''test pick2jik'''
# controll("R").move(-285,-601,264,1.5,0.69,-0.61) #capture top view
# time.sleep(4)
# controll("R").move(-377,-458,267.3,1.73,-1.3,-2.2) #move for safety
# time.sleep(2)
# controll("R").move(-280,-517,96.6,1.16,-2.9,-0.124) #capture front view
# time.sleep(2)
# controll("R").move(-377,-458,267.3,1.73,-1.3,-2.2) #move for safety
# time.sleep(2)
# controll("R").move(-42,-340,534,1.52,0.656,-0.63) #capture material
# path_action("R").pick2jig(-50,-720)

'''test controll'''
# controll("R").move(-75,-540,200,1.5,0.58,-0.66)
# controll("R").move(168,-521,129,1.5,0.58,-0.66)
# controll("R").pick()
# controll("R").move(170,-519,109,1.5,0.58,-0.66)
# controll("R").move(-170,-549,109,1.5,0.58,-0.66)
# # controll("R").move(582,-45,-294,1.5,0.58,-0.66)
# time.sleep(10)
# controll("R").drop()
controll("R").move(-174,-549,149,1.5,0.58,-0.66)
