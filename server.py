# umesh_server.py

import os
import sys
import socket

max_packet_length = 1024
port = 1230
udp_port = 5678


def IndexGetLongList(connection):

	to_send_file = open('output.txt', 'w')
	os.system('ls -hl ~ | awk \'{print ($6, $7, "\t", $8, "\t", $5, "\t", $9)}\' > output.txt')
	to_send_file.close()

	to_send_file1 = open('output.txt', 'r+')
	#connection.send(to_send_file.read() + '\nDone!')
	#to_send_file.close()

	aline = to_send_file1.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file1.read(max_packet_length)
	connection.send('xumeshx')
	to_send_file1.close()

	os.system("rm output.txt")		


def IndexGetShortList(starttime, endtime, connection):

	to_send_file = open('output.txt', 'w')
	os.system('find ~ -type f -newermt "'+ starttime +'" ! -newermt "'+ endtime +'" -ls | awk \'{print ($8, $9, "\t", $7, "\t", $10, $11)}\' > output.txt')
	to_send_file.close()

	to_send_file1 = open('output.txt', 'r+')
	#connection.send(to_send_file.read() + '\nDone!')
	#to_send_file.close()

	aline = to_send_file1.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file1.read(max_packet_length)
	connection.send('xumeshx')
	to_send_file1.close()

	os.system("rm output.txt")


def IndexGetRegex(regex, connection):

	to_send_file = open('output.txt', 'w')
	os.system('ls ~ | grep ' + regex + ' > output.txt')
	to_send_file.close()

	to_send_file1 = open('output.txt', 'r+')
	#connection.send(to_send_file.read() + '\nDone!')
	#to_send_file.close()

	aline = to_send_file1.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file1.read(max_packet_length)
	connection.send('xumeshx')
	to_send_file1.close()
	
	os.system("rm output.txt")


def FileHashVerify(input_file, connection):

	to_send_file = open('output.txt', 'w')
	if os.path.isdir(os.path.expanduser('~') + '/' + input_file):
			to_send_file.write(input_file + ' is directory')
	else:
		os.system('md5 ~/' + input_file + ' > output.txt')
		os.system('ls -lh ~/' + input_file + ' >> output.txt')
	to_send_file.close()

	to_send_file1 = open('output.txt', 'r+')
	#connection.send(to_send_file.read() + '\nDone!')
	#to_send_file.close()

	aline = to_send_file1.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file1.read(max_packet_length)
	connection.send('xumeshx')
	to_send_file1.close()
	
	os.system("rm output.txt")


def FileHashCheckAll(connection):

	to_send_file = open('output.txt', 'w')
	
	for input_file in os.listdir(os.path.expanduser('~')):
		if os.path.isdir( os.path.expanduser('~') + '/' + input_file):
			continue
		else:
			os.system('md5 ~/' + input_file + ' >> output.txt')
		# os.system('ls -lh ~/' + input_file + ' >> output.txt')
	to_send_file.close()

	to_send_file1 = open('output.txt', 'r+')
	#connection.send(to_send_file.read() + '\nDone!')
	#to_send_file.close()

	aline = to_send_file1.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file1.read(max_packet_length)
	connection.send('xumeshx')
	to_send_file1.close()
	
	os.system("rm output.txt")


def FileDownloadTCP(input_file, connection):
	
	to_send_file = open(os.path.expanduser('~') + '/' + input_file, 'r')
	
	aline = to_send_file.read(max_packet_length)
	while aline:
	   connection.send(aline)
	   aline = to_send_file.read(max_packet_length)
	connection.send('endoffile')
	to_send_file.close()
	FileHashVerify(input_file, connection)


def FileDownloadUDP(input_file):
	
	content = ''
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
	udp_host = socket.gethostname()
	addr = (udp_host, udp_port)

	f = open(os.path.expanduser('~') + '/' + input_file,"rb")
	data = f.read(max_packet_length)
	#print "data1", data
	while data:
		content += data
		data = f.read(max_packet_length)
	#print "done with data"
	try:
		udp_socket.sendto(content, addr)
	except socket.error:
		udp_socket.close()
	udp_socket.close()
	f.close()


def parse_input(input_string, connection):
	data = input_string.split()
	
	if data[0] == "IndexGet":
		
		if len(data) >= 2:
			if data[1] == "longlist":
				IndexGetLongList(connection)
				return (1, "Done!")
			elif data[1] == "shortlist":
				if len(data) >= 4:
					IndexGetShortList(data[2], data[3], connection)
					return (2, "Done!")
				return (-1, "Need to specify <starttimestamp> and <endtimestamp>")
			elif data[1] == "regex":
				if len(data) >= 3:
					IndexGetRegex(data[2], connection)
					return (3, "Done!")
				return (-1, "Need to specify regular expression")
			return (-1, "Inappropriate flag")
		else:
			return (-1, "No flag provided")
	
	elif data[0] == "FileHash":
		
		if len(data) >= 2:
			if data[1] == "verify":
				if len(data) >= 3:
					if not os.path.exists(os.path.expanduser('~') + '/' + data[2]):
						return (-1, "File Doesn't Exist!")
					FileHashVerify(data[2], connection)
					return (4, "Done!")
				return (-1, "File name missing")
			elif data[1] == "checkall":
				FileHashCheckAll(connection)
				return (5, "Done!")
			return (-1, "Inappropriate flag")
		return (-1, "Flags not specified: verify/checkAll")

	elif data[0] == "FileDownload":
		if len(data) >= 3:
			if data[1] == "TCP":
				if not os.path.exists(os.path.expanduser('~') + '/' + data[2]):
					return (-1, "File Doesn't Exist!")
				FileDownloadTCP(data[2], connection)
				return (6, "Done!")
			elif data[1] == "UDP":
				if not os.path.exists(os.path.expanduser('~') + '/' + data[2]):
					return (-1, "File Doesn't Exist!")
				FileDownloadUDP(data[2])
				return (7, "Done!")
			return (-1, "Inappropriate flag")
		return (-1, "Format: <TCP/UDP> <filename>")		
	return (-1, "Command Not Found")


def main():
	my_socket = socket.socket()
	host = socket.gethostname()		# for server, host will be itself
	my_socket.bind((host, port))	# bind to the host and port
	my_socket.listen(5)				# Now wait for client connection

	print "Server running at %s:%d" % (host, port)
	
	while True:
		connection, client_address = my_socket.accept()		# accept connection from client
		print 'Connected to', client_address
		connection.send('Connection successful')
		print connection.recv(max_packet_length)
		
		while True:
			data = connection.recv(max_packet_length)			# receive data from client and process accordingly
			if data:
				# print "received from client: ", data
				parse_output = parse_input(data, connection)
				if parse_output[0] < 0:
					connection.send(parse_output[1])
					connection.send('xumeshx')
			if not data:
				break
		connection.close()
	my_socket.close()


if __name__ == '__main__':
	main()
