from socket import *
import sys
import os

serverPort = int(sys.argv[1])  # 10877
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is now ready to receive")

mailed = False
rcpt = 0
dataTime = False
message = ""
recipients = []
mailFromAddress = ""
subject = ""

# whitespace checks how many spaces
# returns number of first index without


def whitespace(s):
    i = 0
    while True:
        if (s[i] != " "):
            return i
        i = i + 1

# nullspace checks if null or space
# returns 0 if no space
# returns number of spaces


def nullspace(s):
    i = 0
    while True:
        if s[i] == " ":
            i = i + 1
        else:
            return i

# checks that there is a character index 0 and 1
# returns true if null


def null(s):
    if letDig(s[0]) and letDig(s[1]):
        return True
    return False

# runs through path backwards
# returns true if > is at the end of the path
# and if there is nothing  between > and mailbox


def reversePath(s):  # run backwards through the path
    global error
    if s[0] != ">":
        if error != 500 and error != 503:
            error = 501
        return False
    return True

# runs through path
# returns true if < if at beginning
# and if there is null or space between < and mailbox
# Throws 501 error if issue within and no other issues with command


def path(s):
    global error
    # make sure next thing is mailbox and not null space
    if s[0] == "<" and nullspace(s[1:]) == 0:
        box = ''.join(s).split(">", 1)
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
        if s[skip + 1] == ">":
            return True
    if nullspace(s[1:]) != 0 or s[0] != "<":
        if error != 500 and error != 503:
            error = 501
        return False


# check for local part, @, and domain
# return true if local part is followed by @ and domain
def mailbox(s):  # make sure string without <> being passed in
    global error
    if "@" not in s:
        if error != 500 and error != 503:
            error = 501
        return 0
    box = ''.join(s).split("@")
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
def localPart(s):
    global error
    if string(s) != True:
        if error != 500 and error != 503:
            error = 501
        return 0
    return len(s)

# checks if each index if a character
# return false if any char test is false
# return true if pass all tests


def string(s):
    for c in s:
        if char(c) != True:
            return False
    return True

# checks if char is ascii and not special or space
# return false if special or space
# return true if printable ascii, otherwise false


def char(s):
    if s == " " or special(s) == True:
        return False
    if ord(s) > 32 and ord(s) <= 128:
        return True
    return False


# deliniate by . and check that each member of the array is an element
# return 0 if element test fails
# otherwise return length of domain
def domain(s):
    sarray = s.split(".")
    length = len(sarray)
    for s in sarray:
        if element(s) <= 0:
            return 0
        length = length + element(s)
    return length

# check if a letter or a name
# return 0 if letter or name test fails
# otherwise length of str


def element(s):
    global error
    if len(s) <= 0:
        if error != 500 and error != 503:
            error = 501
        return 0
    if letter(s[0]) != True or name(s) != True:
        if letter(s[0]) != True:
            if error != 500 and error != 503:
                error = 501
        return 0
    return len(s)


# make sure string starts with a letter
# returns false if letter test on first character fails
# or if letDigString test fails, otherwise true
# throws 501 error if no other issues with command
def name(s):
    global error
    if letter(s[0]) != True:
        if error != 500 and error != 503:
            error = 501
        return False
    if letDigStr(s[1:]) != True:
        if error != 500 and error != 503:
            error = 501
        return False
    return True


# check if character is an uppercase or lowercase letter
# if within ascii range return true, otherwise false
def letter(s):
    if (ord(s) >= 65 and ord(s) <= 90) or (ord(s) >= 97 and ord(s) <= 122):
        return True
    return False


# check each character to see if letDig test pass
# return false if any character fails, otherwise true
def letDigStr(s):
    for char in s:
        if letDig(char) != True:
            return False
    return True


# check if character is a letter or a digit
# return true if letter or digit test true, otherwise false
def letDig(s):
    if digit(s) or letter(s):
        return True
    return False


# check if character is a number
# return true if number is found, otherwise false
def digit(s):
    if ord(s) >= 48 and ord(s) <= 57:
        return True
    return False


# check for new line character
# return true if newline found, otherwise false
def crlf(s):
    if (s[0] == '\n'):
        return True
    return False


# check to see if character is special
# return true if special character
def special(s):
    if (s == '<' or s == '>' or s == '(' or s == ')' or s == '[' or s == ']' or s == '.' or s == ',' or s == ';' or s == ':' or s == '@' or s == '"' or s == "\\"):
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
    dataTime = False
    message = ""
    mailFromAddress = ""
    recipients = []

# returns false if encounter an error and print out error message
# returns true if valid mail command


def handleErrors():
    global error
    if error == 500:
        m = "500 Syntax error: command unrecognized"
        connectionSocket.send(m.encode())
        return False
    elif error == 503:
        m = "503 Bad sequence of commands"
        connectionSocket.send(m.encode())
        return False
    elif error == 501:
        m = "501 Syntax error in parameters or arguments"
        connectionSocket.send(m.encode())
        return False
    else:
        m = "250 OK"
        connectionSocket.send(m.encode())
        return True

# check for duplicate addresses
# once done checking, write message to domain files


def processData(s):
    global message
    global recipients
    global error
    global mailed
    global rcpt
    i = 0
    domains = []
    while i < len(recipients):
        prename = recipients[i].split(">", 1)
        domain = prename[0].split("@", 1)
        if domain[1] not in domains:
            domains.append(domain[1])
            name = "forward/" + domain[1]
            f = open(name, "a+")
            notdot = s.split(".\n")
            f.write(notdot[0])
            f.close()
        i += 1
    resetGlobals()
    return False

# checks for data command
# returns false if bad command
# returns true if need to process data
# don't throw error here bc use this check several places


def data(s):
    global error
    global dataTime
    if s[0] != "D" or s[1] != "A" or s[2] != "T" or s[3] != "A":
        return False
    i = nullspace(s[4:])
    if i == 0 and crlf(s[4:]) != True:
        return False
    if crlf(s[4 + i:]) != True:
        error = 501
        return False
    return True

# check rcpt whitespace to:
# returns true if 500 or 501 level error wasn't written
# puts recipients in message if successful command sequence


def rcptToCmd(s):
    global error
    global message
    if s[0] != "R" or s[1] != "C" or s[2] != "P" or s[3] != "T":
        error = 500
        return False
    i = whitespace(s[4:])
    if i == 0:
        error = 500
        return False
    to = s[4 + i:]
    if to[0] != "T" or to[1] != "O" or to[2] != ":":
        error = 500
        return False
    j = nullspace(to[3:])
    # store after null space in path
    pathe = to[3 + j:]
    # error if path test fails
    if path(pathe) != True:
        return False
    # if no errors return sender ok
    if mailed == True:
        message += "To: " + pathe.split(">", 1)[0] + ">\n"
        # check for duplicates here
        recipients.append(pathe)
    return True

# check mail, whitespace, from:
# returns true if 500 or 501 level error wasn't written
# appends mail from address to message if successful command


def mailFromCmd(s):
    global error
    global mailFromAddress
    global mailed
    global message
    # store first 4 letters in mail array
    mail = s[0:4]
    # error if not "MAIL"
    if mail[0] != "M" or mail[1] != "A" or mail[2] != "I" or mail[3] != "L":
        return False
    # check for how much white space comes after mail and store in i
    i = whitespace(s[4:])
    # error if no whitespace
    if i == 0:
        return False
    # store characters after whitespace and mail in frome array
    frome = s[4 + i:]
    # error if not "FROM:"
    if frome[0] != "F" or frome[1] != "R" or frome[2] != "O" or frome[3] != "M" or frome[4] != ":":
        return False
    # check for amount of null space after from:
    j = nullspace(frome[5:])
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
def grammar(s):
    global mailed
    global rcpt
    global dataTime
    global error
    global recipients
    global subject
    # only one mail from cmd
    if dataTime == True:
        dataTime = processData(s)
    elif s[0] == "M" and mailed != True:
        mailed = mailFromCmd(s)
        if mailed == False and error == 0:
            error = 500
    elif s[0] == "M" and mailed == True:
        if mailFromCmd(s) == True:
            error = 503
        else:
            error = 500
    # count number of rcpt commands
    elif s[0] == "R" and mailed == True:
        if rcptToCmd(s) == True:
            rcpt = rcpt + 1
    elif s[0] == "R" and mailed != True:
        if rcptToCmd(s) == True:
            if error != 500:
                error = 503
                recipients = recipients[:-1]

    # subject line
    elif s[0] == "S" and mailed == True and rcpt > 0:
        subject = s

    # receive data
    elif s[0] == "D" and mailed == True and rcpt > 0:
        dataTime = data(s)
        if dataTime == True and error == 0:
            connectionSocket.send(
                "354 Start mail input; end with <CRLF>.<CRLF>\n".encode())
        if dataTime == False and error != 501:
            error = 500

    #  if data command is bad
    elif s[0] == "D" and (mailbox != True or rcpt == 0):
        if data(s) == True:
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


def quitCmd(s):
    if len(s) != 4:
        return False
    if s[0] == "Q" and s[1] == "U" and s[2] == "I" and s[3] == "T":
        return True
    return False


def quitter():
    closingMessage = "221 " + hostname + " closing connection"
    connectionSocket.send(closingMessage.encode())
    # connectionSocket.close()

# read from socket
# store messages received in file like HW2
# file name after destination domain (jeffay@unc.edu -> unc.edu)
# one cmd line arg
# port number want to listen on


while True:
    connectionSocket, addr = serverSocket.accept()
    hostname = gethostname()
    # send initial greeting
    greeting = "220 " + hostname
    print(greeting)
    connectionSocket.send(greeting.encode())
    # receive helo response
    helo = connectionSocket.recv(1024).decode()
    print(helo)
    # if valid helo then send valid helo response to kick of message
    if checkHelo(helo) == True:
        heloResponse = "250 Hello " + hostname + " pleased to meet you"
        print(heloResponse)
        connectionSocket.send(heloResponse.encode())
    # process message here
    endOfMessage = False
    while endOfMessage != True:
        # reset error after each line is read
        error = 0

        address = connectionSocket.recv(1024).decode()
        if quitCmd(address):
            quitter()
            break

        # find out domain names from recipients
        # no repeat of domains
        # assign appropriate errors
        grammar(address)
        # if not processing data check for errors and start new line
        if dataTime == False:
            handleErrors()
            # sys.stdout.write('\n')
        # condition to close connection

# speak first
    # 220 <client-name>
# receive helo
# gives 250 and echos name of computer", pleased to meet you"
# receive mail from and send 250 <receipient name>... Sender ok
