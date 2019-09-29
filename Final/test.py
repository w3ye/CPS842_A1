import sys,os,re

def test(term)
  return "searching for term related content"

#->
dictionary = open("./dictionary","r")
termNfrequency = dictionary.read()


#->
postingT = open("./postingTerm.txt","r")
termNposting = postingT.read()


#->
postingD = open("./postingDoc.txt","r")
docNtermposition = postingD.read()

required = input("What term are you searching for?")
while required != "ZZEND"
  required = input("What term are you searching for?")
