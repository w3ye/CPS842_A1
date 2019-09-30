import sys,os,re,time,math

class Invert:

    docHash = {} 
    docNum = 0
    token = {}
    stop = []
    tokenNum = 0
    
    def __init__(self):
        self.initDocHash()
        self.initToken()
    
    #read all the content in cacm.all
    def readDoc(self):
        file = open("./cacm/cacm.all")
        data = file.read()
        file.close()
        return data
    
    def initDocHash(self):
        data = self.readDoc()
        for i in data.split(".I"):
            if ".T\n" in i and ".W\n" in i:
                docID = i.split()[0]
                self.docHash[docID] = self.appendAbstractTitle(i)
                self.docNum += 1
        return

    def appendAbstractTitle(self,data):
        line = data.split("\n.")
        temp = ""
        for l in line:
            l = "\n"+ l
            if "\nW\n" in l or "\nT\n" in l:
                temp += l
        return temp

    #takes in the data from initDocHash and take out all words individually
    def initFrequency(self, data):
        temp = ""
        temp = data.replace('\n',' ')
        temp = re.sub('[^A-Za-z]+',' ',temp)
        temp = temp.split()
        for i in self.stop:
            if i in temp:
                temp.remove(i)
        return temp
    
    def initToken(self):
        file = open("./test","w")
        for key,value in self.docHash.items():
            file.write(value+"\n")
        file.close()
        return

Invert()