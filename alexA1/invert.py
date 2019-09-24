import sys,os,re,time,math

docNum = 0 #number of documents
tokNum = 0 #number of tokens
termNum = 0#number of terms
tiNum = 0 #number of term index
diNum = 0 #number of document index


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

.I
123 (document ID)
.T
apple.2.34-46 (term.tf.firstpos-secondpos-thirdpos-...)
bad.1.1

postings structure
{
	"docID":[
			{"term1":["pos1","pos2"]},
			{"term2":["pos1"]}
		]
}


NOT DONE YET

'''
def form(content):
	ct=content.replace('\nT\n',' ').replace('\nW\n',' ')
	terms = {}
	counter = 0
	for t in ct.split():
		counter +=1
		if t in terms and t not in stop:
			terms[t].append(counter)
		else:
			terms[t] = [str(counter)]
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
for f in data.split("\n.I"):
	#we only need document ID, title and abstract from the document
	if ".T\n" in f and ".W\n" in f:
		docID = f.split()[0]#First line after .I is the docID
		docs[docID]=fil(f)#filter only title and abstract
		docNum+=1
files.close()

#->
tokens = {} #all tokens/terms in all valid documents
for key,value in docs.items():
	for t in clean(value):
		if t in tokens:
			tokens[t]+=1
		else:
			tokens[t]=1
		tokNum+=1

#->NOT DONE YET
postings = {}
for doc in docs:
	postings[doc]=form(docs[doc])


#->
#print dctionary document
dictionary = open("./dictionary","w")
for key in sorted(tokens):
	dictionary.write("TERM:"+key+"FREQUENCY:"+str(tokens[key])+"\n")
dictionary.close()

#print the posting document
#NOT DONE YET only prints every valid info from each document right now
#waiting for form method to be done
postings = open("./postings","w")
for key,value in docs.items():
	postings.write(key + docs[key])
