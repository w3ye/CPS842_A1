import sys,os,math,time
import invert


#--------------------------------
#->asking for user input
st = ""
while st.lower() != "n" and st.lower() != "y":
	st = input("Would you like to use stopwords?(N/Y)")

ps = ""
while ps.lower() != "n" and ps.lower() != "y":
	ps = input("Would you like to use Porter Stemming Algorithm?(N/Y)")


required = input("What are you searching for?")
while required != "ZZEND":
	tester = invert.main(ps,st)
	#----------------------------------------
	if required != "" and required.lower() != "default":
		queryWeight = tester.generateQuery(required)
		if queryWeight == []:
			print("Invalid Query")
		elif len(queryWeight) == 1:
			print("Retrieving Term")
			if required in tester.postingHash.keys():
				print("TF = " + str(tester.tokenHash[key]) +".")
				for doc in content:
					print("DocID: " + str(doc[0]) + ". DF = " + str(doc[1]))				
		else:
			tester.topKSimilarity(queryWeight)
	else:
		tester.retrieveQuery()
	
	#----------------------------------------
	required = input("What are you searching for?")

print("Program ends.")
