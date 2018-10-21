from socket import *
import sys
import os
serverName = sys.argv[1]  # snapper.cs.unc.edu
serverPort = int(sys.argv[2])  # 10877
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
greeting = clientSocket.recv(1024).decode()
print(greeting)
heloMessage = "HELO " + gethostbyname(gethostname())
print(heloMessage)
clientSocket.send(heloMessage.encode())
goahead = clientSocket.recv(1024).decode()
print(goahead)

rcptSuccess = False
mailed = False
endMessage = False

# stores message, from mail address, and array of recipient addresses
mailFromAddress = ""
message = ""
recipients = []

# state for error messages
error = 0

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
        print("reversepath is false")
        return False
    return True

# runs through path
# returns true if < if at beginning
# and if there is null or space between < and mailbox
# Throws 501 error if issue within and no other issues with command


def path(s):
    global error
    # make sure next thing is mailbox and not null space
    print("checking path of : " + str(s) )
    if s[0] == "<" and nullspace(s[1:]) == 0:
        box = ''.join(s).split(">", 1)
        print(box)
        if len(box) < 2:
            if error != 500 and error != 503:
                error = 501
            print("path is false1")
            return False
        skip2 = nullspace(box[1])
        if crlf(box[1][skip2]) != True:
            if error != 500 and error != 503:
                error = 501

            print("path is false2")
            return False
        skip = mailbox(box[0][1:])
        if s[skip + 1] == ">":
            return True
    if nullspace(s[1:]) != 0 or s[0] != "<":
        if error != 500 and error != 503:
            error = 501

        print("path is false3")
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

            print("string is false")
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

        print("name1 is false")
        return False
    if letDigStr(s[1:]) != True:
        if error != 500 and error != 503:
            error = 501

        print("name2 is false")
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

            print("lds is false")
            return False
    return True


# check if character is a letter or a digit
# return true if letter or digit test true, otherwise false
def letDig(s):
    if digit(s) or letter(s):
        return True

    print("ld is false")
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

    print("crlf is false")
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
    dataTime = 0
    message = ""
    mailFromAddress = ""
    recipients = []

# returns false if encounter an error and print out error message
# returns true if valid mail command


def handleErrors():
    global error
    if error == 500:
        clientSocket.send("500 Syntax error: command unrecognized".encode())
        return False
    elif error == 503:
        clientSocket.send("503 Bad sequence of commands".encode())
        return False
    elif error == 501:
        clientSocket.send(
            "501 Syntax error in parameters or arguments".encode())
        return False
    else:
        clientSocket.send("250 OK".encode())
        return True

# check rcpt whitespace to:
# returns true if 500 or 501 level error wasn't written
# puts recipients in message if successful command sequence


def rcptToCmd(s, index):
    global message
    j = nullspace(s)
    # store after null space in path
    pathe = s[j:]
    # error if path test fails
    if path(pathe) != True:

        print("rcpt1 is false")
        return False
    # if no errors return sender ok
    if mailed == True:
        message += "To: " + pathe.split(">", 1)[0] + ">\n"
        recipients[index] = pathe.split(">", 1)[0][1:]
    return True

# check mail, whitespace, from:
# returns true if 500 or 501 level error wasn't written
# appends mail from address to message if successful command


def mailFromCmd(s):
    global message
    # error if path test fails
    if path(s) != True:

        print("mail1 is false")
        return False
    # if no errors return sender ok
    if mailed == False:
        mailFromAddress = s.split(">", 1)[0]
        message += "From: " + mailFromAddress + ">\n"
    return True


def quitCmd(s):
    if s[0] == "Q" and s[1] == "U" and s[2] == "I" and s[3] == "T" and s[4] == "\n":
        return True

    print("quit is false")
    return False


def errorNum(s):
    return s[0:3]


def quitter():
    clientSocket.send("QUIT".encode())
    if errorNum(clientSocket.recv(1024).decode()) == 221:
        clientSocket.close()


# get from
while mailed != True:
    fromm = raw_input("From: \n")
    print(fromm)
    # check from
    if mailFromCmd("<" + fromm + ">\n") == True:
        mailed = True
    # if from is bad loop
    # if from is good change mailed
newFromm = "MAIL FROM: <" + fromm + ">\n"
clientSocket.send(newFromm.encode())
print("sent mailfromcmd, awaiting response")
# get response
response = clientSocket.recv(1024).decode()
print(response)
# if response is good change state
while rcptSuccess != True:
    too = raw_input("To: \n")
    recipients = too.split(",")
    print(recipients)
    # check if toos are good
    successes = 0
    rcpts = 0
    while rcpts < len(recipients):
        ignore = nullspace(recipients[rcpts])
        recipients[rcpts] = "<" + recipients[rcpts][ignore:] + ">\n"
        if rcptToCmd(recipients[rcpts], rcpts) == True:
            successes += 1
        rcpts += 1
    if successes == len(recipients):
        rcptSuccess = True
        print("good senders")
    # trim off whitespace before <'s and restore also
    # if bad one reprompt
# if good send
for line in recipients:
    print(line)
    rcptBoi = "RCPT TO: <" + line + ">\n"
    print(rcptBoi)
    clientSocket.send(rcptBoi.encode())
    print("sent address, waiting on response")
    response = clientSocket.recv(1024).decode()
    print("response received")
    # check if response good
subjectt = raw_input("Subject: \n")
subjectt = "Subject: " + subjectt + "\n"
clientSocket.send(subjectt.encode())
print("subject sent waiting on response...")
response = clientSocket.recv(1024).decode()
print(response + " received")
# send data command
clientSocket.send("DATA\n".encode())
print("sent data command, waiting on response...")
response = clientSocket.recv(1024).decode()
print(response + " received")
# check response starts with 354
if errorNum(response) == "354":
        message = "From: " + fromm + '\n'
        for line in recipients:
            message += "To: " + line + "\n"
        message += subjectt + "\n"
        datar = ""
        datar = raw_input("Message:\n")
        while datar != ".":
            print(datar)
            message += datar + '\n'
            datar = raw_input()
        message += ".\n"
        # message is done so send message to server
        print("sending: \n" + message)
        clientSocket.send(message.encode())
        # get back server response
        print("message sent, waiting on response...")
        clientSocket.recv(1024).decode()
        print(response + " received, quitting now")
        quitter()

# put in print errors like hw1
# take out print debugging
# fix hostname to not display ip address
# double check helo syntax in server
# fix quit command
# figure out how to print error messages when encounter socket errors and what not
# put angle brackets on from and to in message
# put to's on one line



# change user input to be good commands
# send user input

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
