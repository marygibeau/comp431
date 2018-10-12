from socket import *
import sys
import os

# state for command order variables
dataTime = False
mailed = False
rcpt = 0

# stores message, from mail address, and array of recipient addresses
mailFromAddress = ""
message = ""
recipients = []

# state for error messages
error = 0

# whitespace checks how many spaces 
# returns number of first index without
def whitespace ( str ):
    i = 0
    while True:
        if (str[i] != " "):
            return i
        i = i + 1

# nullspace checks if null or space
# returns 0 if no space
# returns number of spaces
def nullspace ( str ):
    i = 0
    while True:
        if str[i] == " ":
            i = i + 1
        else:
            return i

# checks that there is a character index 0 and 1
# returns true if null
def null ( str ):
    if letDig(str[0]) and letDig(str[1]):
        return True
    return False

# runs through path backwards
# returns true if > is at the end of the path
# and if there is nothing  between > and mailbox
def reversePath ( str ): # run backwards through the path
    global error
    if str [0] != ">":
        if error != 500 and error != 503:
            error = 501
        return False
    return True

# runs through path
# returns true if < if at beginning
# and if there is null or space between < and mailbox
# Throws 501 error if issue within and no other issues with command
def path ( str ):
    global error
    if str[0] == "<" and nullspace(str[1:]) == 0: # make sure next thing is mailbox and not null space
        box = ''.join(str).split(">", 1)
        if len(box) < 2:
            if error != 500 and error != 503:
                error = 501
            return False
        skip2 = nullspace(box[1])
        if crlf(box[1][skip2]) != True:
            if error != 500 and error != 503:
                error = 501
            return False 
        skip = mailbox(box[0][1:])
        if str[skip + 1] == ">":
            return True
    if nullspace(str[1:]) != 0 or str[0] != "<":
        if error != 500 and error != 503:
            error = 501
        return False


# check for local part, @, and domain
# return true if local part is followed by @ and domain
def mailbox ( str ): # make sure string without <> being passed in
    global error
    if "@" not in str:
        if error != 500 and error != 503:
            error = 501
        return 0
    box = ''.join(str).split("@")
    if len(box) != 2:
        if error != 500 and error != 503:
            error = 501
        return 0
    if localPart(box[0]) <= 0 or domain(box[1]) <= 0:
        return 0
    return localPart(box[0]) + domain(box[1])



# checks string
# returns false if all digits or null
# returns string test otherwise
def localPart ( str ):
    global error
    if string(str) != True:
        if error != 500 and error != 503:
            error = 501
        return 0
    return len(str)

# checks if each index if a character
# return false if any char test is false
# return true if pass all tests
def string ( str ):
    for c in str:
        if char(c) != True:
            return False
    return True

# checks if char is ascii and not special or space
# return false if special or space
# return true if printable ascii, otherwise false
def char ( str ):
    if str == " " or special(str) == True:
        return False
    if ord(str) > 32 and ord(str) <= 128:
        return True
    return False 


# deliniate by . and check that each member of the array is an element
# return 0 if element test fails
# otherwise return length of domain
def domain ( str ):
    sarray = str.split(".")
    length = len(sarray)
    for s in sarray:
        if element(s) <= 0:
            return 0
        length = length + element(s)
    return length

# check if a letter or a name
# return 0 if letter or name test fails
# otherwise length of str
def element ( str ):
    global error
    if len(str) <= 0:
        if error != 500 and error != 503:
            error = 501
        return 0
    if letter(str[0]) != True or name(str) != True:
        if letter(str[0]) != True:
            if error != 500 and error != 503:
                error = 501
        return 0
    return len(str)


# make sure string starts with a letter
# returns false if letter test on first character fails
# or if letDigString test fails, otherwise true
# throws 501 error if no other issues with command
def name ( str ):
    global error
    if letter(str[0]) != True:
        if error != 500 and error != 503:
            error = 501
        return False
    if letDigStr(str[1:]) != True:
        if error != 500 and error != 503:
            error = 501
        return False
    return True


# check if character is an uppercase or lowercase letter
# if within ascii range return true, otherwise false
def letter ( str ):
    if (ord(str) >= 65 and ord(str) <= 90) or (ord(str) >= 97 and ord(str) <= 122):
        return True
    return False


# check each character to see if letDig test pass
# return false if any character fails, otherwise true
def letDigStr ( str ):
    for char in str:
        if letDig(char) != True:
            return False
    return True
            

# check if character is a letter or a digit
# return true if letter or digit test true, otherwise false
def letDig ( str ):
    if digit(str) or letter(str):
        return True
    return False
    

# check if character is a number
# return true if number is found, otherwise false
def digit ( str ):
    if ord(str) >= 48 and ord(str) <= 57:
        return True
    return False 


# check for new line character
# return true if newline found, otherwise false
def  crlf ( str ):
    if ( str[0] == '\n'):
        return True
    return False


# check to see if character is special
# return true if special character
def special ( str ):
    if ( str == '<' or str == '>' or str == '(' or str == ')' or str == '[' or str == ']' or str == '.' or str == ',' or str == ';' or str == ':' or str == '@' or str == '"' or str == "\\"):
        return True
    return False 

# reset global variables after successful mail message is constructed
def resetGlobals():
    global mailed
    global rcpt
    global dataTime
    global message
    global recipients
    global mailFromAddress
    mailed = False
    rcpt = 0
    dataTime = 0
    message = ""
    mailFromAddress = ""
    recipients = []

# returns false if encounter an error and print out error message
# returns true if valid mail command
def handleErrors():
    global error
    if error == 500:
        connectionSocket.send("500 Syntax error: command unrecognized".encode())
        return False
    elif error == 503:
        connectionSocket.send("503 Bad sequence of commands".encode())
        return False
    elif error == 501:
        connectionSocket.send("501 Syntax error in parameters or arguments".encode())
        return False
    else:
        connectionSocket.send("250 OK".encode())
        return True

# returns true if still processing
# false if done processing
# when done, write message to file bc mail maessage is a success
def processData( str ):
    global message
    global recipients
    global error
    global mailed
    global rcpt
    if str == ".\n":
        i = 0
        # print(recipients)
        while i < len(recipients):
            # print("here's what's being written...")
            # print(message)
            prename = recipients[i].split(">", 1)
            name = "forward/" + prename[0][1:] # + ".txt"
            i += 1
            f = open(name, "a+")
            f.write(message)
            f.close()
        resetGlobals()
        return False
    message += str
    return True

# checks for data command
# returns false if bad command
# returns true if need to process data
# don't throw error here bc use this check several places
def data( str ):
    global error
    global dataTime
    if str[0] != "D" or str[1] != "A" or str[2] != "T" or str[3] != "A":
        return False
    i = nullspace(str[4:])
    if i == 0 and crlf(str[4:]) != True:
        return False
    if crlf(str[4 + i:]) != True:
        error = 501
        return False
    return True

# check rcpt whitespace to:
# returns true if 500 or 501 level error wasn't written
# puts recipients in message if successful command sequence
def rcptToCmd ( str ):
    global error
    global message
    if str[0] != "R" or str[1] != "C" or str[2] != "P" or str[3] != "T":
        error = 500
        return False
    i = whitespace( str[4:] )
    if i == 0:
        error = 500
        return False
    to = str[4 + i:]
    if to[0] != "T" or to[1] != "O" or to[2] != ":":
        error = 500
        return False
    j = nullspace( to[3:] )
    # store after null space in path
    pathe = to[3 + j:]
    # error if path test fails
    if path(pathe) != True:
        return False
    # if no errors return sender ok
    if mailed == True:
        message += "To: " + pathe.split(">", 1)[0] + ">\n"
        recipients.append(pathe)
    return True

# check mail, whitespace, from:
# returns true if 500 or 501 level error wasn't written
# appends mail from address to message if successful command
def mailFromCmd ( str ):
    global error
    global mailFromAddress
    global mailed
    global message
    # store first 4 letters in mail array
    mail = str[0:4]
    # error if not "MAIL"
    if mail[0] != "M" or mail[1] != "A" or mail[2] != "I" or mail[3] != "L":
        return False
    # check for how much white space comes after mail and store in i
    i = whitespace( str[4:] )
    # error if no whitespace
    if i == 0:
        return False
    # store characters after whitespace and mail in frome array
    frome = str[4 + i:]
    # error if not "FROM:"
    if frome[0] != "F" or frome[1] != "R" or frome[2] != "O" or frome[3] != "M" or frome[4] != ":":
        return False
    # check for amount of null space after from:
    j = nullspace( frome[5:] )
    # store after null space in path
    pathe = frome[5 + j:]
    # error if path test fails
    if path(pathe) != True:
        return False
    # if no errors return sender ok
    if mailed == False:
        mailFromAddress = pathe.split(">", 1)[0]
        message += "From: " + mailFromAddress + ">\n"
    return True
    

# state machine
# checks first letter of command and siphon of to correct helper function
# issues 503 error if commands out of order
def grammar ( str ):
    global mailed
    global rcpt
    global dataTime
    global error
    global recipients
    # only one mail from cmd
    # print(mailed)
    # print(rcpt)
    if dataTime == True:
        dataTime = processData ( str )
    elif str[0] == "M" and mailed != True:
        mailed = mailFromCmd( str )
        if mailed == False and error == 0:
            error = 500
    elif str[0] == "M" and mailed == True:
        if mailFromCmd( str ) == True:
            error = 503
        else:
            error = 500
    # count number of rcpt commands
    elif str[0] == "R" and mailed == True:
        if rcptToCmd( str ) == True:
            rcpt = rcpt + 1
    elif str[0] == "R" and mailed != True:
        if rcptToCmd( str ) == True:
            if error != 500:
                error = 503
                recipients = recipients [:-1]
                
    # receive data
    elif str[0] == "D" and mailed == True and rcpt > 0:
        dataTime = data( str )
        if dataTime == True and error == 0:
            connectionSocket.send("354 Start mail input; end with <CRLF>.<CRLF>\n".encode())
        if dataTime == False and error != 501:
            error = 500

            
    elif str[0] == "D" and (mailbox != True or rcpt == 0):
        if data(str) == True:
            error = 503
        else:
            error = 500
    else:
        if error != 503:
            error = 500


def checkHelo(s):
    if s[0] != "H" or s[1] != "E" or s[2] != "L" or s[3] != "O":
        return False
    return True

# read from socket
# store messages received in file like HW2
# file name after destination domain (jeffay@unc.edu -> unc.edu)
# one cmd line arg
# port number want to listen on

serverPort = 877
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is now ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    hostname = connectionSocket.gethostname()
    # send initial greeting
    greeting = "220 " + hostname
    connectionSocket.send(greeting.encode())
    # receive helo response
    helo = connectionSocket.recv(1024).decode()
    # if valid helo then send valid helo response to kick of message
    if checkHelo(helo) == True:
        heloResponse = "250 " + hostname + " pleased to meet you"
        connectionSocket.send(heloResponse.encode())
    # process message here
    endOfMessage = False
    while endOfMessage != True:
        # reset error after each line is read
        error = 0
        
        address = connectionSocket.recv(1024).decode()
        # find out domain names from recipients
        # no repeat of domains
        # assign appropriate errors
        grammar(address)
        # if not processing data check for errors and start new line
        if dataTime == False:
            handleErrors()
            sys.stdout.write('\n')
        # condition to close connection
        if connectionSocket.recv(1024).decode() == "QUIT":
            closingMessage = "221 " + hostname + " closing connection"
            connectionSocket.send(closingMessage.encode())
            connectionSocket.close()
# speak first
    # 220 <client-name>
# receive helo
# gives 250 and echos name of computer", pleased to meet you"
# receive mail from and send 250 <receipient name>... Sender ok
