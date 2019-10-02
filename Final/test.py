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
print("got it")

required = ""
while required != "ZZEND":
	#the loop will keep running untill the user say ZZEND
	required = raw_input("What term are you searching for?")
	print("Searhing for: "+required)
	start = time.time()

	#----------------------------------------
	tester = invert.main(ps,st)
	tester.initDoc()
	#----------------------------------------

	end = time.time()
	print("The program used: "+ str(end-start)+"seconds.")


print("Program ends.")
