import sys

datar = ""
message = ""
datar = raw_input("354 Start mail input; end with <CRLF>.<CRLF>\n")
while datar != ".":
        print(datar)
        message += datar
        datar = raw_input()
print(message)