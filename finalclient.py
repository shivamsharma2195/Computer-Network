#Group Members:
#  Name                 ID
# SHIVAM SHARMA     2019H1240160
# CHINMAY ROJINDAR  2019H1240132
# AYUSH CHOWDHURY   2019H1240603
# MOHIT KULKARNI    2019H1240134
# ASHIRWAD RAY      2019H1240129
#


import socket
import sys
import hashlib
import select 
import sys 
import time
r=16
strt=0
host     = "127.0.0.1"
port     = 20009
serverAddressPort   = ("127.0.0.1", 20009)
buf=16
buff=1024
chat=1
fltrnsfr=2
msgFromClient1       = "let's do chatting  1"
msgFromClient2       = "file transfer mode 2"
bytesToSend1         = str.encode(msgFromClient1)
bytesToSend2         = str.encode(msgFromClient2)


def cksum(data):
     cksm=reduce(lambda x,y:x+y, map(ord, data))
     return cksm

def packt(dat):
	z=len(dat)
	if len(dat)>15:
		return dat
    	else:
        	while (len(dat)<16):
        	    dat=dat+" "
		return dat

def unpack(rxdata):
	p=0
	l=len(rxdata)
	
	a=int(rxdata[0])
#	print "a =",a
	p=p+1
	b=int(rxdata[p:p+a])
#	print "b =",b
	p=p+a
	c=int(rxdata[p:p+1])
#	print "c =",c
	p=p+1
	e=int(rxdata[p:p+c])
#	print "e =",e
	p=p+c
	code=rxdata[p:p+e]
#	print "code = ",code
	p=p+e
	d=int(rxdata[p:p+1])
	p=p+1
	checks=int(rxdata[p:p+d])
	p=p+d
	packetno=int(rxdata[p:l])
	print "packet no is = ",packetno
	check=cksum(code)
	if check==checks:
		print"checksum verified"
		return code
	else:
		return "error"



a= int(input("enter 1 for chat and 2 for file transfer"))

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s=UDPClientSocket
if a==chat:
	UDPClientSocket.sendto(bytesToSend1, serverAddressPort)
	[data,ip]= UDPClientSocket.recvfrom(buff)
	print data
	while(data):
		print("type your msg")
		messg = sys.stdin.readline()
		message=packt(messg) 
		flen=1
		a=1
		j=1
		check=str(cksum(message))
		data=str(a)+str(flen)+str(len(str(len(message))))+str(len(message))+message+str(len(check))+check+str(j)
		UDPClientSocket.sendto(data,ip)

		print "waiting for server msg"
		[msg,ip]= UDPClientSocket.recvfrom(buff)
		data=unpack(msg)
		print "server msg is = ",data		


elif a==fltrnsfr:
	UDPClientSocket.sendto(bytesToSend2, serverAddressPort)
#	msg=s.recvfrom(buf)
#	print msg
	addr = (host,port)
	file_name="readme.txt"
	f1=open(file_name,"r")
	fl=len(f1.read())
	if fl/buf==strt:
		flen=fl/buf
	else:
		flen=(fl/buf)+1
 
	b=len(str(flen))
	f1.close()
	f=open(file_name,"rb")

#data = f.read(buf)
	print file_name

#s.sendto(data,addr)
	print "file name sent"
	j=1
	print "packet sent ", j
	data = f.read(buf)
	while (j<flen+1):
	    if(s.sendto(data,addr)):
	     print "packet sent ", j
	     ack,ip=UDPClientSocket.recvfrom(buf)
	     print"ack received for ",ack
	     j=j+1
	     rcdata = f.read(buf)
	     message=packt(rcdata)
	     check=str(cksum(message))
	     data=str(len(str(flen)))+str(flen)+str(len(str(len(message))))+str(len(message))+message+str(len(check))+check+str(j)
	     
	print "file sent"
	f.close()
s.close()






