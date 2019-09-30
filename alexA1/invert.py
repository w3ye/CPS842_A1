import sys,os,re,time,math


'''
input the content of each book
and returns only title and abstract of the book like the following:

.W
blahblah blha
.T
blah

'''
def fil(content):
	lines=content.split("\n.")
	re = ""
	for line in lines:
		line = "\n"+line
		if "\nW\n" in line or "\nT\n" in line:
			re+=line#only append the abstract and the title part
	return re

'''
clean the given content and return a string with only letters
'''
def clean(content):
	temp = ""	
	temp = content.replace('\n',' ')
	temp = re.sub('[^A-Za-z]+', ' ', temp)
	temp = temp.split()
	for t in stop:
		if t in temp:
			temp.remove(t)
	return temp
	

'''
formatting things in document to list format

postings structure
{
	"docID":[
			{"term1":["pos1","pos2"]},
			{"term2":["pos1"]}
		]
}

'''
def form(content):
	ct=content.replace('\nT\n',' ').replace('\nW\n',' ')
	terms = {}
	occurrence = 0
	for t in clean(ct):
		occurrence +=1
		if t not in stop:
			if t in terms:
				terms[t].append(occurrence)
			else:
				terms[t] = [occurrence]
	return terms

#->
stopwords = open("./stopwords.txt","r")
s = stopwords.read()
stop = []#all the stop words to ignore

for w in s.split():
	stop.append(w)
stopwords.close()

#->
files = open("./cacmoriginal/cacm.all","r")# open the file
data = files.read()

docs = {} #the dictionary hashmap for data storage
docNum = 0 #number of documents

for f in data.split("\n.I"):
	#we only need document ID, title and abstract from the document
	if ".T\n" in f and ".W\n" in f:
		docID = f.split()[0]#First line after .I is the docID
		docs[docID]=fil(f)#filter only title and abstract
		docNum+=1
files.close()

#->
tokens = {} #all tokens/terms in all valid documents
tokNum = 0 #number of tokens

for key,value in docs.items():
	for t in clean(value):
		if t.lower() not in stop:
			if t in tokens:
				tokens[t]+=1
			else:
				tokens[t]=1
		tokNum+=1

#->postings ordered by documentID
postingDoc = {}
for doc in docs.keys():
	postingDoc[doc]=form(docs[doc])

#->
#print dctionary document
dictionary = open("./dictionary","w")
for key in sorted(tokens):
	dictionary.write(key+"&"+str(tokens[key])+"\n")
dictionary.close()


#->
#NEED MODIFICATION
postD = open("./postingDoc.txt","w")

for postDkey,postDvalue in postingDoc.items():
	postD.write("Document ID:"+postDkey+" \n")
	for k,v in postDvalue.items():
		postD.write("Term:"+k)
		postD.write(" Frequency:"+str(len(v)))
		postD.write(" Postings:"+''.join(str(e)+"-" for e in v)+"\n")
postD.close()

'''
postings in the order of terms
{
	"term":[
		{doc1:[pos1,pos2]},
		{doc2:[pos2,pos2,pos3]}
	],
	"term2":[...]
}
'''
postingTerm = {}
for key in tokens.keys():
	postingTerm[key]=[]#initializing the postings in order of terms

for keyID,termList in postingDoc.items():
	for t in termList:
		if t in postingTerm.keys():
			tempMap = {keyID:termList[t]}
			postingTerm[t].append(tempMap)

#->
postT = open("./postingTerm.txt","w")

print(type(postingTerm))
