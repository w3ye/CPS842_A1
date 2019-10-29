import sys,os,re,time,math
import nltk
from nltk.stem import PorterStemmer

'''
New data strcture for dictionary and postings
dictionary postings
term | frequency -> docid | frequency | positions
		 -> docid | frequency | positions

{
[t1]:[
		[doc1,n1,pos1,pos2,pos....],
		[],
		[]
	]
}
'''

class main:
	docHash = {}
	tokenHash = {}
	stopwords = []
	postingHash = {}
	weightHash = {}
	def __init__(self,algorithm,stop):
		if stop.lower() == "y": self.getStop()
		self.initDoc()
		self.initToken(algorithm.lower())
		self.initPosting()
		self.initWeights()
		self.writeOut()

	def readDoc(self,docName):
		#helper function for reading document data to avoid duplicte
		file = open(docName,"r")
		data = file.read()
		file.close()
		return data

	def initDoc(self):
		'''
		This functions reads all documents from file
		Each file is separated by \n.I
		File content is only validated and stored if it has both abstract and title
		The content is filtered as a list of tokenized letters
		'''
		data = self.readDoc("./cacm/cacm.all")
		for f in data.split("\n.I"):
			if ".T\n" in f and ".W\n" in f:
				docID = f.split()[0]
				self.docHash[docID] = self.filt(f)
	

	def filt(self,raw):
		'''
		//input the raw content of each book
		.W
		blah blahblha
		.T
		bla bbb
		//and return as a list of letters combining both
		'''
		parts = raw.split("\n.")#split categories like abstracts, titles etc.
		temp = ""
		for part in parts:
			part = "\n" + part
			if "\nW\n" in part:
				temp = temp + part.replace("\nW\n"," ")
			if "\nT\n" in part:
				temp = temp + part.replace("\nT\n"," ")
		return self.clean(temp)


	def clean(self,raw):
		#the cleaning function that removes all non letters or nextlines
		raw = raw.replace("\n"," ")#put everything in the same line
		words = re.sub('[^A-Za-z]+',' ',raw)#change all the non-letters to space
		wordList = [x for x in words.lower().split() if x not in self.stopwords]
		return wordList


	def initToken(self,use):
		'''
		This function initilizes tokens
		storing all unique tokens in a hashmap
		and storing all raw(valid terms only) docs in a hashmap
		'''
		ps = PorterStemmer()
		for docVal in self.docHash.values():
				for term in docVal:
					if use == "y": term = ps.stem(term)
					if term in self.tokenHash: self.tokenHash[term]+=1
					else: self.tokenHash[term]=1

	def initPosting(self):
		print("initializing postings")
		for terms in self.tokenHash:
			self.postingHash[terms]=self.getPost(terms)
			

	def getPost(self,target):
		'''
		search over all valid documents for a certain term
		returns a list of maps for each term

		return a list of docs
		[
			[doc1,2,pos1,pos2]
			[doc2,3,pos1,pos2,pos3]
		]
		'''
		temp = []
		for docID,docVal in self.docHash.items():
			if target in docVal:
				positions = [str(index+1) for index,value in enumerate(docVal) if target == value]
				temp.append([docID,len(positions)] + positions)
		return temp
		
	
	def writeOut(self):
		#write dictionary to file in order of terms
		dictionary = open("./dictionary","w")
		for t in sorted(self.tokenHash):
			dictionary.write(t+"&"+str(self.tokenHash[t])+"\n")
		dictionary.close()
		#write postings to file in order of terms
		posting = open("./posting","w")
		for term in sorted(self.postingHash):
			posting.write(str(term) + " : " + str(self.postingHash[term]) + "\n")
		#write tfs
		termfrequency = open("./tfs","w")
		for d,f in self.weightHash.items():
			termfrequency.write("docID: " + str(d) + " tfs: " + str(f) + "\n")
		#write raw docs
		f = open("./rawdocs","w")
		for i,l in self.docHash.items():
			f.write(i + " :\n"+ str(l) + "\n")

		dictionary.close()
		posting.close()
		termfrequency.close()
		f.close()

	def getStop(self):
		#read common words into stopwords list when necessary
		data = self.readDoc("./cacm/common_words")
		for w in data.split():
			self.stopwords.append(w)

	def getWeight(self,ls1,ls2):
		'''calculate similarity between two lists: tfs and idfs
		
		dot = 0.0
		len1 = 0.0
		for x in ls1:
			len1 += x**2
			for y in ls2:
				dot += x*y
		len2 = 0.0
		for y in ls2:
			len2 += y**2
		return dot / (math.sqrt(len1)*math.sqrt(len2))
		'''
		weights = []
		for i in range(len(ls1)):
			weights.append(ls1[i]*ls2[i])
		return weights

	def initWeights(self):
		'''calculated terms frequencies for all docs and terms
		{docID: [f1,f2,f3 ..... fn]}
		for each term shown in doc
		'''
		print("initializing document weights")
		n = len(self.tokenHash.keys())
		print(n)
		#
		idfs = []
		for t,f in self.postingHash.items():
			idfs.append(math.log(n/len(f)))
		#
		for docID, docVal in self.docHash.items():
			tfs = []
			for t,f in self.postingHash.items():
				if t not in docVal: tfs.append(0)
				else:
					for docs in f:
						if docs[0] == docID: tfs.append(1 + math.log(docs[1]))
			self.weightHash[docID] = self.getWeight(tfs,idfs)

