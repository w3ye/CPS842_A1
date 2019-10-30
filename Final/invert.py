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
	rawdocHash = {}
	docHash = {}
	tokenHash = {}
	stopwords = []
	postingHash = {}
	weightHash = {}
	queryList = []
	queryWeight = {}
	stem = ""
	def __init__(self,algorithm,stop):
		if stop.lower() == "y": self.getStop()
		self.stem = algorithm.lower()
		self.initDoc()
		self.initToken()
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
				self.docHash[docID] = self.tokenize(f)
				self.rawdocHash[docID] = self.filt(f)
	

	def tokenize(self,raw):
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

	def filt(self,raw):
		'''split each part by .^?
		'''
		re = {}
		for block in raw.split("\n."):
			if block[0] == 'T': re["title"] = block
			if block[0] == 'W': re["content"] = block
			if block[0] == 'A': re["author"] = block
		return re

	def clean(self,raw):
		#the cleaning function that removes all non letters or nextlines
		raw = raw.replace("\n"," ")#put everything in the same line
		words = re.sub('[^A-Za-z]+',' ',raw)#change all the non-letters to space
		wordList = [x for x in words.lower().split() if x not in self.stopwords]
		return wordList


	def initToken(self):
		'''
		This function initilizes tokens
		storing all unique tokens in a hashmap
		and storing all raw(valid terms only) docs in a hashmap
		'''
		ps = PorterStemmer()
		for docVal in self.docHash.values():
				for term in docVal:
					if self.stem == "y": term = ps.stem(term)
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
		f = open("./docs","w")
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
		#
		idfs = []
		for f in self.postingHash.values():
			if len(f)==0: idfs.append(0)
			else: idfs.append(math.log(n/len(f)))
		#
		for docID, docVal in self.docHash.items():
			tfs = []
			for t,f in self.postingHash.items():
				if t not in docVal: tfs.append(0)
				else:
					for docs in f:
						if docs[0] == str(docID): tfs.append(1 + math.log(docs[1]))
			self.weightHash[docID] = self.getWeight(tfs,idfs)

	def generateQuery(self,required):
		'''tokenize query to list of terms
		'''
		self.queryList = self.clean(required)
		if self.stem == "y":
			ps = PorterStemmer()
			for q in self.queryList:
				q = ps.stem(q)
		for t in self.queryList:
			if t in self.tokenHash and t not in self.queryWeight.keys():
				self.queryWeight[t]=1
			elif t in self.tokenHash and t in self.queryWeight.keys():
				self.queryWeight[t]+=1
		return self.queryList

	def retrieveQuery(self):
		'''Assume retrieve top 5 results
		'''
		queryLength = 0.0
		for x in self.queryWeight.values():
			queryLength += x**2
		similarity = []
		for doc,val in self.docHash.items():
			if sorted(list(set(self.queryList)-set(val))) == sorted(self.queryList):
				similarity.append(0)
			else:
				docLength = 0.0
				dot = 0.0
				for y in self.weightHash[doc]:
					if y != 0: docLength += y**2
					for z in self.queryWeight.values():
						dot += z * y
				similarity.append(round((dot / (math.sqrt(docLength)*math.sqrt(queryLength))),2))
		#top 5 retrieval
		for i in range(4):
			similarity = list(set(similarity) - set([0.0]))
			top = similarity.index(sorted(similarity)[-i])
			print(sorted(similarity)[-i])
			print(top)
			#print(str(self.rawdocHash.keys()))
			print(str(i+1) + ": " + self.docHash.keys()[top])
			print("Title: " + self.rawdocHash.values()[top]["title"][2:])
			print("Author: " + self.rawdocHash.values()[top]["author"][2:])

