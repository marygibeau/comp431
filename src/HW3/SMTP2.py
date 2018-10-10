import sys
import os

rcpt = 0
dataTime = False
mailed = False

# whitespace checks how many spaces
# returns number of first index without


def whitespace(str):
    i = 0
    while True:
        if (str[i] != " "):
            return i
        i = i + 1


def fromCmd(s):
    if s[0] == "F" and s[1] == "r" and s[2] == "o" and s[3] == "m" and s[4] == ":" and s[5] == " ":
        return True
    return False


def toCmd(s):
    if s[0] == "T" and s[1] == "o" and s[2] == ":" and s[3] == " ":
        return True
    return False


def resetGlobals():
    global rcpt
    global dataTime
    global mailed
    rcpt = 0
    dataTime = False
    mailed = False


def error(s):
    return s[0:3]


def quit():
    sys.stdout.write("QUIT")
    f.close()


# file is read in from command line argument that is file name
f = open(sys.argv[1], "r")

info = f.readlines()

for line in info:
    # echo what was read to stderr
    # sys.stderr.write(line)
    response = ""
    if fromCmd(line) == True and mailed != True:
        resetGlobals()
        sys.stdout.write("MAIL FROM: " + line[6:])
        # read in from stdin
        response = sys.stdin.readline()
        sys.stderr.write( response)
        if error(response) != "250":
            quit()
            break
        else:
            mailed = True
    elif toCmd(line) == True and mailed == True:
        sys.stdout.write("RCPT TO: " + line[4:])
        rcpt = rcpt + 1
        response = sys.stdin.readline()
        sys.stderr.write( response)
        if error(response) != "250":
            quit()
            break
        else:
            rcpt = rcpt + 1
    elif toCmd(line) != True and mailed == True and rcpt > 0:
        if dataTime == False:
            sys.stdout.write("DATA\n")
            response = sys.stdin.readline()
            sys.stderr.write( response)
            if error(response) != "354":
                quit()
                break
            else:
                sys.stdout.write(line)
            dataTime = True
        elif fromCmd(line) == True:
            sys.stdout.write(".\n")
            response = sys.stdin.readline()
            sys.stderr.write( response)
            if error(response) != "250":
                quit()
                break
            resetGlobals()
            sys.stdout.write("MAIL FROM: " + line[6:])
            # read in from stdin
            response = sys.stdin.readline()
            sys.stderr.write( response)
            if error(response) != "250":
                quit()
                break
            else:
                mailed = True
        else:
            sys.stdout.write(line)
    elif line[0] == "Q" and line[1] == "U" and line[2] == "I" and line[3] == "T":
        quit()
        break
else:
    if dataTime == True:
        sys.stdout.write("\n.\n")
        response = sys.stdin.readline()
        sys.stderr.write( response)
        if error(response) != "250":
            quit()
    elif mailed == True and rcpt > 0:
        sys.stdout.write("DATA\n")
        response = sys.stdin.readline()
        sys.stderr.write( response)
        if error(response) != "354":
            quit()
        else:
            sys.stdout.write(".\n")
            response = sys.stdin.readline()
            sys.stderr.write( response)
            if error(response) != "250":
                quit()
            resetGlobals()
