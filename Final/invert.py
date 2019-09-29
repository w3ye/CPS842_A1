import sys,os,re,time,math

class Invert:

    docHash = {}

    #read all the content in cacm.all
    def readDoc(self):
        file = open("./cacm/cacm.all")
        data = file.read()
        file.close()
        return data

    def initDocHash(self):
        return

Invert().readDoc()