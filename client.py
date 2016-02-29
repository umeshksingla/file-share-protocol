# umesh_client.py

import os, re
import sys
import socket

max_packet_length = 1024
FileDownload = 0
TCP = 1
UDP = 0
FileDownloadName = ''
udp_port = 5678

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def open_my_socket(ip_addr, port_no):
	try:
		my_socket.connect((ip_addr, port_no))
		my_socket.send("Hello from client!")
	except socket.error:
		print "couldn't connect: Connection Refused"
		sys.exit(1)


def main():
	TCP = 1
	UDP = 0
	if len(sys.argv) < 3:
		print 'Usage: python client.py <IP> <PORT>\nIP PORT: ip address you want to connect to.'
		sys.exit(1)

	# open a socket for connection
	ip_addr = sys.argv[1]
	port_no = sys.argv[2]

	open_my_socket(ip_addr, int(port_no))
	print my_socket.recv(max_packet_length)

	while True:
		TCP = 1
		UDP = 0
		print "Enter Command:", 
		input_string = raw_input()
		FileDownload = 0
		if input_string == "quit":
			sys.exit(0)
		if input_string:
			if "FileDownload" in input_string:
				FileDownload = 1
				TCP = 1
				if len(input_string.split()) == 3:
					FileDownloadName = input_string.split()[2]	# name of file
					FileDownloadType = input_string.split()[1]	# method to use
					if FileDownloadType == 'UDP':
						TCP = 0
						UDP = 1
				else:
					FileDownload = 0
			my_socket.send(input_string)
			
			#	receiving part 
			if FileDownload:
				f = open(FileDownloadName, 'w')
			else:
				f = open('received_file', 'w')

			flag = 0
			
			if TCP:	
				while True:
					data = my_socket.recv(max_packet_length)
					if 'xumeshx' in data:
						print data.replace('xumeshx', '')
						break
					if 'endoffile' in data or flag == 1:
						if flag:
							print data
						else:
							flag = 1
							f.write(re.sub('endoffile', '', data))
					else:
						if not flag:
							f.write(data)
				f.close()
			
			elif UDP:
				
				# make a DGRAM socket
				udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
				udp_host = ip_addr
				udp_socket.bind((udp_host, udp_port))
				addr = (udp_host, udp_port)
				data, addr = udp_socket.recvfrom(max_packet_length*100000)
				#print data
				f.write(data)
				"""data, addr = udp_socket.recvfrom(max_packet_length)
				print data
				while data:
					print data
			    	f.write(data)
			    	data, addr = udp_socket.recvfrom(max_packet_length)"""
				udp_socket.close()
				f.close()

			if FileDownload:
				print 'File Downloaded: ' + FileDownloadName
				FileDownload = 0
			else:
				f = open('received_file', 'r')
				print f.read()
				f.close()
				os.system("rm received_file")

	my_socket.close()	

if __name__ == '__main__':
	main()
