# Provides an interface which communicates between Twitch and AI

import re
import socket
import string
from settings import HOST, PORT, OAUTH, IDENT, CHANNEL

class TwitchBot:
    def __init__(self):
        # workaround the be able to access streamer's name inside chatbot.py
        self.nickname = CHANNEL

    def openSocket(self):
        s = socket.socket()
        s.connect((HOST, PORT))
        msg = "PASS " + OAUTH + "\r\n" + "NICK " + IDENT + "\r\n" + "JOIN #" + CHANNEL + "\r\n"
        s.send(msg.encode(encoding='utf_8'))
        return s
    
    def joinRoom(self, s):
        buffer = ""
        loading = True
        while loading:
            buffer = buffer + s.recv(1024).decode(encoding='utf_8')
            temp = buffer.split("\n")
            readbuffer = temp.pop() 
            for line in temp:
                print(line)
                loading = self.loadingComplete(line)       
        self.sendMessage(s, "Succesfully joined the chat!")
            
    def loadingComplete(self, line):
        if("End of /NAMES list" in line):
            return False
        else:
            return True
    
    def sendMessage(self, s, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
        s.send(messageTemp.encode(encoding='utf_8'))
        print("Sent: " + messageTemp)

    def getMessage(self, line):
        ret = re.search(":.*:(.*)", line)
        return ret.group(1)
    
    def getUser(self, line):
        ret = re.search(":.*#(.*) :", line)
        return ret.group(1)