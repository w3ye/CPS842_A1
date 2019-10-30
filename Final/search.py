import sys,os,math,time
import invert


#--------------------------------
#->asking for user input
st = ""
while st.lower() != "n" and st.lower() != "y":
	st = raw_input("Would you like to use stopwords?(N/Y)")

ps = ""
while ps.lower() != "n" and ps.lower() != "y":
	ps = raw_input("Would you like to use Porter Stemming Algorithm?(N/Y)")



required = raw_input("What are you searching?")
while required != "ZZEND":
	#the loop will keep running untill the user say ZZEND
	start = time.time()
	print("preparing...")
	tester = invert.main(ps,st)
	#----------------------------------------
	query = tester.generateQuery(required)
	if len(query) == 1:
		#searching term
		found = False
		for key,content in tester.postingHash.items():
			if required == key:
				found = True
				print("TF = " + str(tester.tokenHash[key]) +".")
				for doc in content:
					print("DocID: " + str(doc[0]) + ". DF = " + str(doc[1]))
		if not found: print("Term: "+ required +"NOT FOUND!\n")
	else:
		#searching sentence
		tester.retrieveQuery()
	#----------------------------------------
	end = time.time()
	print("The program used: "+ str(end-start)+"seconds.")
	required = raw_input("What term are you searching for?")

print("Program ends.")
