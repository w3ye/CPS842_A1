import sys,os,re,time
#if without class you can just def a main function which triggers other functions such as initDoc or initPosting
from invert import main
#if you have set up main class, then just simply import the whole document
import invert

def test(term)
  return "searching for term related content"

#->
dictionary = open("./dictionary","r")
termNfrequency = dictionary.read()


#->
posting = open("./posting","r")
termNposting = posting.read()

posting.close()
dictionary.close()


#->
stop = ""
while stop.lower() != "n" and stop.lower() != "y":
  stop = input("Would you like to use stopwords?(N/Y)")
  
ps = ""
while ps.lower() != "n" and ps.lower() != "y":
  ps = input("Would you like to use Porter Stemming Algorithm?(N/Y)")

required = ""
while required != "ZZEND"：
  required = input("What term are you searching for?")
  print("Searhing for: "+required)
  start = time.time()




  '''
  Put the body of excutional code here
  '''

  end = time.time()
  print("The program used: "+ str(end-start)+"seconds.")

print("Program ends.")
