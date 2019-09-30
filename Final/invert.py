import sys,os,re,time,math

class Invert:

    docHash = {} 
    docNum = 0
    token = {}
    stop = []
    tokenNum = 0
    file = open("./test","w")
    
    def __init__(self):
        self.initDocHash()
        self.initToken()
        #self.dictionary()
    
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
                self.file.write(self.appendAbstractTitle(i))
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
        for key,value in self.docHash.items():
            for i in self.initFrequency(value):
                if i in self.token:
                    self.token[i] += 1
                else:
                    self.token[i] = 1
                self.tokenNum += 1
        return
    
    def dictionary(self):
        file = open("./dictionary","w")
        for i in sorted(self.token):
            file.write("Word: "+i+"\tFrequency: "+str(self.token[i])+"\n")
        file.close()
        return

Invert()