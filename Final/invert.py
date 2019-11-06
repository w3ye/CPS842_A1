import sys,os,re,time,math
import nltk
from nltk.stem import PorterStemmer

'''
New data strcture for dictionary and postings
dictionary postings
term -> docid | frequency | positions
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
	docToken = {}
	doc = {}
	tokenHash = {}
	queryWeight = {}
	postingHash = {}
	docWeight = {}
	stopwords = []

	stem = ""
	def __init__(self, algorithm, stop):
		if stop.lower() == "y": self.getStop()
		self.stem = algorithm.lower()
		self.initDoc()
		self.initToken()
		self.initPosting()
		self.initWeights()
		self.writeOut()

	def readDoc(self, docName):
		file = open(docName,"r")
		data = file.read()
		file.close()
		return data

	def getStop(self):
		data = self.readDoc("./cacm/common_words")
		for w in data.split():
			self.stopwords.append(w)	

	def initDoc(self):
		'''This functions reads all documents from file
		Each file is separated by \n.I
		File content is only validated and stored if it has both abstract and title
		The content is filtered as a list of tokenized letters
		'''
		data = self.readDoc("./cacm/cacm.all")
		for f in data.split("\n.I"):
			if ".T\n" in f and ".W\n" in f:
				docID = f.split()[0]
				self.docToken[docID] = self.tokenize(f)
				self.doc[docID] = self.filt(f)
	

	def tokenize(self,raw):
		'''Tokenize all the terms in abstract and title
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
		'''Split out each title abstract and author of the book
		'''
		re = {}
		for block in raw.split("\n."):
			if block[0] == 'T': re["title"] = block
			if block[0] == 'W': re["content"] = block
			if block[0] == 'A': re["author"] = block
		return re

	def clean(self,raw):
		'''Removes all non letters and next lines
		'''
		raw = str(raw).replace("\n"," ")
		words = re.sub('[^A-Za-z]+',' ',raw)
		wordList = [x for x in words.lower().split() if x not in self.stopwords]
		ps = PorterStemmer()
		if self.stem.lower() == "y":
			for w in wordList:
				w = ps.stem(w)		
		return sorted(wordList)


	def initToken(self):
		'''Initializes all unique terms and store in hashmap alphabetically
		'''
		tokens = {}
		for docVal in self.docToken.values():
				for term in docVal:
					if term in tokens: tokens[term]+=1
					else: tokens[term]=1
		for token in sorted(tokens.keys()):
			self.tokenHash[token] = tokens[token]

	def initPosting(self):
		for terms in self.tokenHash:
			self.postingHash[terms] = self.getPost(terms)
			

	def getPost(self,target):
		'''Search over all valid documents for a certain term
		returns a list of docs for each term:
		[
			[doc1,2,pos1,pos2]
			[doc2,3,pos1,pos2,pos3]
		]
		'''
		temp = []
		for docID,docVal in self.docToken.items():
			if target in docVal:
				positions = [str(index+1) for index,value in enumerate(docVal) if target == value]
				temp.append([docID,len(positions)] + positions)
		return temp
		
	
	def writeOut(self):
		#write dictionary to file in order of terms
		dictionary = open("./dictionary","w")
		for t in self.tokenHash:
			dictionary.write(t+"&"+str(self.tokenHash[t])+"\n")
		#write postings to file in order of terms
		posting = open("./posting","w")
		for term in self.postingHash:
			posting.write(str(term) + " : " + str(self.postingHash[term]) + "\n")
		#write raw docs
		f = open("./tokenizedDocs","w")
		for i,l in self.docToken.items():
			f.write(i + " :\n"+ str(l) + "\n")
		#
		tf = open("./tfs","w")
		for d,w in self.docWeight.items():
			tf.write(str(d) + ": " + str(w))

		dictionary.close()
		posting.close()
		f.close()
		tf.close()

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
		n = len(self.docToken.keys())
		#
		idfs = []
		for f in self.postingHash.values():
			if len(f)==0: idfs.append(0)
			else: idfs.append(math.log(n/len(f)))
		#
		for docID, docVal in self.docToken.items():
			tfs = []
			for t,f in self.postingHash.items():
				if t not in docVal: tfs.append(0)
				else:
					for docs in f:
						if docs[0] == str(docID): tfs.append(1 + math.log(docs[1]))
			self.docWeight[docID] = self.getWeight(tfs,idfs)

	def generateQuery(self, required):
		'''tokenize query to list of terms
		'''
		self.queryList = self.clean(required)
		print(str(self.queryList))
		queryWeight = {}
		for t in self.queryList:
			if t in self.tokenHash and t not in queryWeight.keys():
				queryWeight[t]=1
			elif t in self.tokenHash and t in queryWeight.keys():
				queryWeight[t]+=1
		return list(queryWeight.values())

	def retrieveQuery(self):
		'''Read given queries
		'''
		defaultQuery = self.readDoc("./cacm/query.text")
		for part in defaultQuery.split(".I "):
			for q in part.split("\n."):
				if "W\n" in q:
					self.topKSimilarity(self.generateQuery(q.split()[1:]))

	def topKSimilarity(self, queryWeight):
		'''Assume retrieve top 5 results
		'''
		print(str(queryWeight))
		queryLength = 0.0
		for x in queryWeight:
			queryLength += x**2
		similarity = []
		for doc,val in self.docToken.items():
			'''
			if [x for x in self.queryList if x in val] == []:
				similarity.append("x")
			else:
			'''
			if [x for x in self.queryList if x in val] != []:
				docLength = 0.0
				dot = 0.0
				for y in self.docWeight[doc]:
					if y != 0.0:
						docLength += y**2
						for z in queryWeight:
							dot += z * y
				similarity.append(dot / (math.sqrt(docLength) * math.sqrt(queryLength)))
			else:
				similarity.append(0.0)
		print(list(self.docToken.keys())[similarity.index(max(similarity))])
		#top 5 retrieval
		'''
		for i in range(1):
			similarity = list(set(similarity) - set([0.0]))
			top = similarity.index(sorted(similarity)[i])
			print(sorted(similarity)[i])
			print(top)
			#print(str(self.rawdocHash.keys()))
			print(str(i+1) + ": " + self.docHash.keys()[top])
			print("Title: " + self.rawdocHash.values()[top]["title"][2:])
			print("Author: " + self.rawdocHash.values()[top]["author"][2:])
		'''

