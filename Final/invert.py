import sys,os,re,time,math

class Invert:

    docHash = {}
    docNum = 0

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
                self.docHash[docID] = 1
                file.write(self.appendAbstractTitle(i))
                self.docNum += 1

        file.close()
        return

    def appendAbstractTitle(self,data):
        line = data.split("\n.")
        temp = ""
        for l in line:
            l = "\n"+ l
            if "\nW\n" in l or "\nT\n" in l:
                temp += l
        return temp

Invert().initDocHash()