from socket import *
serverName = 'snapper.cs.unc.edu'
serverPort = 10877
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
heloMessage = "HELO " + clientSocket.gethostname()
clientSocket.send(heloMessage.encode())

# take in user input
# change user input to be good commands
# send user input

clientSocket.close()
# prompt user to type in email message
# send message to server
# take two command line args
    # name of the server - name of computer server is executing on
    # port number that server is expecting connection on
        # should use 8000+0877
        # should be prepared to handle port conflicts

# listen for 220 message
# smtp helo command
# after 250 send mail from cmd

# prints From: and then allows user to enter email address
# print error and ask user to enter correct email
# prints To: and then a list of recipients separated by commas - no angle brackets
# print error and prompt user to type better address
# Subject:
# arbitrary text
# Message: <message body terminated on an empty line
# arbitrary text

# establish socket
# send message
# terminate after success or any socket or protocol errors

# send message with 
    # From: <>
    # To: <>
    # Subject:
    # blank line
    # body
    # do not include period