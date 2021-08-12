# -*- coding: utf-8 -*-
import sys
import struct

from socket import *
from threading import Thread

def download_thread(fileName, clientInfo):
 
	s = socket(AF_INET, SOCK_DGRAM)
 
	fileNum = 0
	fileName = "configXml\\" + str(fileName)[2:-1]
	# str(fileName) :  b'content'
	try:
		f = open(fileName,'rb')
	except:
        # print("file not exist")
        # error code 1: file not found
		errorData = struct.pack('!HHHb', 5, 1, 5, fileNum)
		print(fileName)
		s.sendto(errorData, clientInfo)

		exit()
 
	while True:
		readFileData = f.read(512)
		fileNum += 1
		sendData = struct.pack('!HH', 3, fileNum) + readFileData
		s.sendto(sendData, clientInfo)
		if len(sendData) < 516:
			# print("用户"+str(clientInfo), end='')
			print('download config file finished')
			break
		responseData = s.recvfrom(1024)
		recvData, clientInfo = responseData
		#print(recvData, clientInfo)
		packetOpt = struct.unpack("!H", recvData[:2])
		packetNum = struct.unpack("!H", recvData[2:4])
		#print(packetOpt, packetNum)

		if packetOpt[0] != 4 or packetNum[0] != fileNum:
			print("文件传输错误！")
			break
	f.close()

	s.close()
	exit()


# one instance is engouht
def lauchServer():
	s = socket(AF_INET, SOCK_DGRAM)
	# s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	try:
		s.bind(('', 6699))
	except:
		print("tftp server is running")
		return

	
	print("tftp服务器成功启动!")
	while True:
		recvData,clientInfo = s.recvfrom(1024)
		print(recvData)
		print(recvData[0:2])
		print(recvData[2:-37])
        
        # Read request
		if recvData[0:2] == b'\x00\x01':
			fileName = recvData[2:-37]
			t = Thread(target=download_thread, args=(fileName, clientInfo))
			t.start()
        # if struct.unpack('!b5sb', recvData[-7:]) == (0, b'octet', 0):
        #     opcode = struct.unpack('!H',recvData[:2])
            # fileName = recvData[2:-7].decode('gb2312')
            
            # if opcode[0] == 1:
            #     t = Thread(target=download_thread, args=(fileName, clientInfo))
            #     t.start()

			# elif opcode[0] == 2:
			# 	t = Thread(target=upload_thread, args=(fileName, clientInfo))
			# 	t.start()
	s.close()



if __name__ == "__main__":
    lauchServer()