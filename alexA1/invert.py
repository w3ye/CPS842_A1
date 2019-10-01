import sys,os,re,math

'''
//input the raw content of each book
.W
blah blahblha
.T
bla bbb

//and return as a list of size 2
[abstract,title]
'''
def filt(raw):
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

'''
the clean function removes all non letters and nextlines
'''
def clean(raw):
	temp = " ".join(raw)#raw is a list of two string elements
	temp.replace("\n"," ")#put everything in the same line
	words = re.sub('[^A-Za-z]+',' ',temp)#change all the non-letters to space
	wordList = set(words.lower().split()) - set(stopwords)#--->removes stopwords from list<---
	return wordList

'''
search over all valid documents for a certain term
returns a list of maps for each term

"term":[
	{doc1:[pos1,pos2,pos3]}
	{doc2:[pos2]}
]
'''
def getPost(target):
	temp = []
	#for docID,docVal in rawDocs.items():
		#positions = [str(index+1) for index,value in enumerate(docVal) if target in value]
		#temp.append({docID:positions})
	return temp

#->

stop = "y"
stopwords = []#list to store all the obmitting words

if stop == "y":
	stopwordFile = open("./cacm/common_words","r")
	s = stopwordFile.read()

	for w in s.split():
		stopwords.append(w)
	stopwordFile.close()

#->
files = open("./cacm/cacm.all","r")
data = files.read()

docs = {}#the dictionary hashmap for valid content of each book
for f in data.split("\n.I"):
	#we only need document ID, title and abstract from the document
	if ".T\n" in f and ".W\n" in f:
		docID = f.split()[0]#first thing after .I is document ID
		docs[docID] = filt(f)#filter only title and abstract
files.close()


#->
tokens = {}
rawDocs = {}
for docID,docVal in docs.items():
	rawDocs[docID] = list(clean(docVal))
	for term in clean(docVal):
		if term in tokens: tokens[term]+=1
		else: tokens[term]=1

#->
postings = {}
for t in sorted(tokens):
	postings[t]=getPost(t)

#->print dictionary document
dictionary = open("./dictionary","w")
for t in sorted(tokens):
	dictionary.write(t+"&"+str(tokens[t])+"\n")
dictionary.close()

#->print postings document
print(postings)
'''
posting = open("./posting","w")
for t,v in posting.items():
	posting.write("\n?"+t)
	for d in v:
		posting.write("!"+d)
		for p in v[d]:
			posting.write("-"+p)

'''

#->
#print(docs[docs.keys()[0]])
