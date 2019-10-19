import sys,os,math,time
import invert

'''
#->dictionary file as input
dictionary = open("./dictionary","r")
termNfrequency = dictionary.read()

#->posting file as input
posting = open("./posting","r")
termNposting = posting.read()

posting.close()
dictionary.close()
'''


#--------------------------------
#->asking for user input
st = ""
while st.lower() != "n" and st.lower() != "y":
	st = raw_input("Would you like to use stopwords?(N/Y)")

ps = ""
while ps.lower() != "n" and ps.lower() != "y":
	ps = raw_input("Would you like to use Porter Stemming Algorithm?(N/Y)")
print("preparing...")

tester = invert.main(ps,st)

required = raw_input("What term are you searching for?")
while required != "ZZEND":
	#the loop will keep running untill the user say ZZEND
	print("Searhing for: "+required)
	start = time.time()

	#----------------------------------------
	found = False
	for key,content in tester.postingHash.items():
		if required == key.split()[0]:
			found = True
			print("The term shows up: " + key.split()[1] +"times.\n")
			print("Sample article: \n" + tester.docHash[content[0][0]][0] + tester.docHash[content[0][0]][1] + "\n")
			print("All positions: ")
			for doc in content:
				print(str(doc) + "\n")
	if not found: print("Term: "+ required +"NOT FOUND!\n")
	#----------------------------------------

	end = time.time()
	print("The program used: "+ str(end-start)+"seconds.")
	required = raw_input("What term are you searching for?")

print("Program ends.")
