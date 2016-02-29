# umesh_client.py

import os
import sys
import socket

max_packet_length = 1024
FileDownload = 0
FileDownloadName = ''

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def open_my_socket(ip_addr, port_no):
	try:
		my_socket.connect((ip_addr, port_no))
		my_socket.send("Hello from client!")
	except socket.error:
		print "couldn't connect: Connection Refused"
		sys.exit(1)


def main():
	
	if len(sys.argv) < 3:
		print 'Usage: python client.py <IP> <PORT>\nIP PORT: ip address you want to connect to.'
		sys.exit(1)

	# open a socket for connection
	ip_addr = sys.argv[1]
	port_no = sys.argv[2]

	open_my_socket(ip_addr, int(port_no))
	print my_socket.recv(max_packet_length)

	while True:
		print "Enter Command:", 
		input_string = raw_input()
		FileDownload = 0
		if input_string == "quit":
			sys.exit(0)
		if input_string:
			if "FileDownload" in input_string:
				FileDownload = 1
				if len(input_string.split()) == 3:
					FileDownloadName = input_string.split()[2]
				else:
					FileDownload = 0
			my_socket.send(input_string)
			
			#	receiving part 
			if FileDownload:
				f = open(FileDownloadName, 'w')
			else:
				f = open('received_file', 'w')

			flag = 0	
			while True:
				data = my_socket.recv(max_packet_length)
				if 'xumeshx' in data:
					print data.replace('xumeshx', '')
					break
				if 'endoffile' in data or flag == 1:
					if flag:
						print data
					flag = 1
				else:
					if not flag:
						f.write(data)
			f.close()

			if FileDownload:
				print 'File Downloaded:' + FileDownloadName
				FileDownload = 0
			else:
				f = open('received_file', 'r')
				print f.read()
				f.close()
				os.system("rm received_file")

	my_socket.close()	

if __name__ == '__main__':
	main()
