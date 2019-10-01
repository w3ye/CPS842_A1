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
	temp = raw.replace("\n"," ")
	temp = re.sub('[^A-Za-z]+',' ',temp)
	temp = temp.split()
	for t in stopwords:
		if t in temp: temp.remove(t)
	return temp
	
'''
search over all valid documents for a certain term
returns a list of maps for each term

"term":[
	{doc1:[pos1,pos2,pos3]}
	{doc2:[pos2]}
]
'''
def post(target):
	temp = []
	for docID,docVal in docs.items():
		if target in clean(docVal[0]+docVal[1]):
			temp.append({docID:getPos(target,clean(docVal[0]+docVal[1]))})
	return temp

def getPos(term,val):
	pos = []
	count = 0
	for t in val:
		count+=1
		if term == t: pos.append(count)
	return pos

#->
stopwordFile = open("./cacm/common_words","r")
s = stopwordFile.read()
stopwords = []#list to store all the obmitting words

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
for docID,docVal in docs.items():
	for term in clean(docVal[0]+docVal[1]):
		if term.lower() not in stopwords:
			if term in tokens: tokens[term]+=1
			else: tokens[term]=1

#->
postings = {}
for t in sorted(tokens):
	postings[t]=post(t)#

#->print dictionary document
dictionary = open("./dictionary","w")
for t in sorted(tokens):
	dictionary.write(t+"&"+str(tokens[t])+"\n")
dictionary.close()

#->print postings document
posting = open("./posting","w")
for t,v in posting.items():
	posting.write("\n?"+t)
	for d in v:
		posting.write("!"+d)
		for p in v[d]:
			posting.write("-"+p)

#->
print(docs["2919"][1])
