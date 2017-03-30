# Echo client program
import socket
import time

HOST = "192.168.0.9" # The remote host
PORT_502 = 502

print "Starting Program"

count = 0
home_status = 0
program_run = 0

while (True):
 if program_run == 0:
   try:
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.settimeout(10)
     s.connect((HOST, PORT_502))
     time.sleep(0.05)

     print ""
     print "Request reg 400"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x90 x00 x01"
     reg_400 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x90\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 400"
     print "Received"
     reg_400 = s.recv(1024)
     print repr(reg_400) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_400 = reg_400.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_400 = reg_400.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_400 == "":
       reg_400 = "0000"
     print reg_400
     print ""
     reg_400_i = int(reg_400,16)
     print reg_400_i
     if reg_400_i < 32768:
       reg_400_f = float(reg_400_i)/10
     if reg_400_i > 32767:
       reg_400_i = 65535 - reg_400_i
       reg_400_f = float(reg_400_i)/10*-1
     print "X = ",reg_400_f

     print ""
     print "Request reg 401"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x91 x00 x01"
     reg_401 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x91\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 401"
     print "Received"
     reg_401 = s.recv(1024)
     print repr(reg_401) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_401 = reg_401.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_401 = reg_401.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_401 == "":
       reg_401 = "0000"
     print reg_401
     print ""
     reg_401_i = int(reg_401,16)
     print reg_401_i
     if reg_401_i < 32768:
       reg_401_f = float(reg_401_i)/10
     if reg_401_i > 32767:
       reg_401_i = 65535 - reg_401_i
       reg_401_f = float(reg_401_i)/10*-1
     print "Y = ",reg_401_f

     print ""
     print "Request reg 402"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x92 x00 x01"
     reg_402 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x92\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 402"

     print "Received"
     reg_402 = s.recv(1024)
     print repr(reg_402) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_402 = reg_402.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_402 = reg_402.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_402 == "":
       reg_402 = "0000"
     print reg_402
     print ""
     reg_402_i = int(reg_402,16)
     print reg_402_i
     if reg_402_i < 32768:
       reg_402_f = float(reg_402_i)/10
     if reg_402_i > 32767:
       reg_402_i = 65535 - reg_402_i
       reg_402_f = float(reg_402_i)/10*-1
     print "Z = ",reg_402_f

     print ""
     print "Request reg 403"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x93 x00 x01"
     reg_403 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x93\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 403"
     print "Received"
     reg_403 = s.recv(1024)
     print repr(reg_403) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_403 = reg_403.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_403 = reg_403.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_403 == "":
       reg_403 = "0000"
     print reg_403
     print ""
     reg_403_i = int(reg_403,16)
     print reg_403_i
     if reg_403_i < 32768:
       reg_403_f = float(reg_403_i)/1000
     if reg_403_i > 32767:
       reg_403_i = 65535 - reg_403_i
       reg_403_f = float(reg_403_i)/1000*-1
     print "Rx = ",reg_403_f

     print ""
     print "Request reg 404"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x94 x00 x01"
     reg_404 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x94\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 404"
     print "Received"
     reg_404 = s.recv(1024)
     print repr(reg_404) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_404 = reg_404.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_404 = reg_404.strip("\x00\x04\x00\x00\x00\x05\x00\x03\x02")
     reg_404 = reg_404.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_404 == "":
       reg_404 = "0000"
     print reg_404
     print ""
     reg_404_i = int(reg_404,16)
     print reg_404_i
     if reg_404_i < 32768:
       reg_404_f = float(reg_404_i)/1000
     if reg_404_i > 32767:
       reg_404_i = 65535 - reg_404_i
       reg_404_f = float(reg_404_i)/1000*-1
     print "Ry = ",reg_404_f

     print ""
     print "Request reg 405"
     print "Sending: x00 x04 x00 x00 x00 x06 x00 x03 x01 x95 x00 x01"
     reg_405 = ""
     s.send ("\x00\x04\x00\x00\x00\x06\x00\x03\x01\x95\x00\x01") #request data from register 128-133 (cartisian data)
     print "Modbus command send to read reg 405"
     print "Received"
     reg_405 = s.recv(1024)
     print repr(reg_405) #Print the receive data in \x hex notation (notice that data above 32 hex will berepresented at the ascii code e.g. 50 will show P
     print ""
     reg_405 = reg_405.replace ("\x00\x04\x00\x00\x00\x05\x00\x03\x02", "")
     reg_405 = reg_405.strip("\x00\x04\x00\x00\x00\x05\x00\x03\x02")
     reg_405 = reg_405.encode("hex") #convert the data from \x hex notation to plain hex
     if reg_405 == "":
       reg_405 = "0000"
     print reg_405
     print ""
     reg_405_i = int(reg_405,16)
     print reg_405_i
     if reg_405_i < 32768:
       reg_405_f = float(reg_405_i)/1000
     if reg_405_i > 32767:
       reg_405_i = 65535 - reg_405_i
       reg_405_f = float(reg_405_i)/1000*-1
     print "Rz = ",reg_405_f

     time.sleep(5.00)
     home_status = 1
     program_run = 0
     s.close()
   except socket.error as socketerror:
     print("Error: ", socketerror)
print "Program finish"
