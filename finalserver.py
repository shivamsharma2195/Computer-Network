#Group Members:
#  Name                 ID
# SHIVAM SHARMA     2019H1240160
# CHINMAY ROJINDAR  2019H1240132
# AYUSH CHOWDHURY   2019H1240603
# MOHIT KULKARNI    2019H1240134
# ASHIRWAD RAY      2019H1240129
#


from socket import *
import socket
import sys
import select 
import time
import timeit

localIP     = "127.0.0.1"
localPort   = 20009
#address     = ("127.0.0.1", 20009)
chat=1
strt=0
r=16
fltrnsfr=2
buff=1024
msgFromServer1       = "we are ready to chat Hello"
bytesToSend1         = str.encode(msgFromServer1)
msgFromServer2       = "send file"
bytesToSend2         = str.encode(msgFromServer2)


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
	print "packet no is =",packetno
	check=cksum(code)
	if check==checks:
		print"checksum verified"
		return code
	else:
		return "error"


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s=UDPServerSocket
UDPServerSocket.bind((localIP, localPort))
[data,ip]= UDPServerSocket.recvfrom(buff)
print data[0:19]," with ",ip
slct=data[19]
print data[19]
if int(slct)==chat:
	print "chat mode"
	UDPServerSocket.sendto(bytesToSend1, ip)
	while(data):
		print("type your msg")
		messg = sys.stdin.readline()
		message=packt(messg)
		flen=1
		a=1
		j=1
		check=str(cksum(message))
		data=str(a)+str(flen)+str(len(str(len(message))))+str(len(message))+message+str(len(check))+check+str(j)
		UDPServerSocket.sendto(data,ip)

		print "waiting for Client msg"
		rxcdata,ip = UDPServerSocket.recvfrom(buff)
		data=unpack(rxcdata)
		print "Client Msg is =",data		



elif int(slct)==fltrnsfr:
	print "file mode"
	UDPServerSocket.sendto(bytesToSend2, ip)
	data,addr = s.recvfrom(buff)
	start=timeit.default_timer()
	fname="rx.txt"
	fil = open(fname,'wb+')
	fil.write(data)
	j=2
	rcdata,addr = s.recvfrom(buff)
	data=unpack(rcdata)
	try:
		while(data):
			fil.write(data)
			print "packet recieved and ack sent for packet ", j
			UDPServerSocket.sendto(str(j),ip)
			s.settimeout(2)
			rcdata,addr = s.recvfrom(buff)
			j=j+1
			data=unpack(rcdata)
	except timeout:
		stop=timeit.default_timer()
		print "total time taken to download the file is :",(stop-start)
		fil.close()
		s.close()
	print "File Donwloaded"
