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
        data = self.readDoc()
        file = open("./test","a")
        for i in data.split(".I"):
            if ".T\n" in i and ".W\n" in i:
                docID = i.split()[0]
                print(docID)
        
        file.close()
        return

Invert().initDocHash()