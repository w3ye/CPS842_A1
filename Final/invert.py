import sys,os,re,time,math
import nltk
from nltk.stem import PorterStemmer

'''
New data strcture for dictionary and postings
dictionary postings
term | frequency -> docid | frequency | positions
		 -> docid | frequency | positions

{
[t1_totalN]:[
		[doc1,n1,pos1,pos2,pos....],
		[],
		[]
	]
}
'''

class main:
	docHash = {}
	rawdocHash = {}
	tokenHash = {}
	stopwords = []
	postingHash = {}
	tfHash = {}
	def __init__(self,algorithm,stop):
		if stop.lower() == "y": self.getStop()
		self.initDoc()
		self.initToken(algorithm.lower())
		self.initPosting()
		self.initTfs()
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
		The content is filtered as a list
		value[0] is abstract and value[1] is title
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
		//and return as a list of size 2
		[abstract,title]
		'''
		parts = raw.split("\n.")#split categories like abstracts, titles etc.
		temp = []
		for part in parts:
			part = "\n"+part
			if "\nW\n" in part:
				temp.append(part.replace("\nW\n",""))
			elif "\nT\n" in part:
				temp.append(part.replace("\nT\n",""))
		if len(temp)==1:temp.append(" ")#in case one of the title or abstract is empty but .T/.W is still there
		return temp


	def clean(self,raw):
		#the cleaning function that removes all non letters or nextlines
		temp = " ".join(raw)#raw is a list of two string elements
		temp.replace("\n"," ")#put everything in the same line
		words = re.sub('[^A-Za-z]+',' ',temp)#change all the non-letters to space
		wordList = set(words.lower().split()) - set(self.stopwords)#--->removes stopwords from list<---
		return wordList


	def initToken(self,use):
		'''
		This function initilizes tokens
		storing all unique tokens in a hashmap
		and storing all raw(valid terms only) docs in a hashmap
		'''
		ps = PorterStemmer()
		for docID, docVal in self.docHash.items():
				self.rawdocHash[docID] = list(self.clean(docVal))
				for term in self.clean(docVal):
					if use == "y": term = ps.stem(term)
					if term in self.tokenHash: self.tokenHash[term]+=1
					else: self.tokenHash[term]=1

	def initPosting(self):
		for terms in self.tokenHash.keys():
			dic = terms + " " + str(self.tokenHash[terms])
			self.postingHash[dic]=self.getPost(terms)
			

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
		for docID,docVal in self.rawdocHash.items():
			#positions = [str(index+1) for index,value in enumerate(docVal) if target in value]
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
		for term in self.postingHash:
			posting.write(str(term) + " : " + str(self.postingHash[term]) + "\n")
		#write tfs
		termfrequency = open("./tfs","w")
		for d,f in self.tfHash.items():
			termfrequency.write("docID: " + str(d) + "frequency: " + str(f) + "\n")

	def getStop(self):
		#read common words into stopwords list when necessary
		data = self.readDoc("./cacm/common_words")
		for w in data.split():
			self.stopwords.append(w)
	def initTfs(self):
		"""calculated terms frequencies for all docs and terms
		{docID: [f1,f2,f3 ..... fn]}
		n same size as tokenHash for corresponding tokens
		"""
		for docID, docVal in self.rawdocHash.items():
			dfs = []
			for t,f in self.tokenHash.items():
				#if t not in docVal: dfs.append(0)
				#else:
				if t in docVal:
					for docs in self.postingHash[str(t) + " " + str(f)]:
						if docs[0] == docID: dfs.append(1 + math.log(docs[1]))
			self.tfHash[docID] = dfs
