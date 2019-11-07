# CPS842_A2
* Yuanbo Shi & William Ye
* 500745024  & 500780613

# Report
*How to run the program?
Simply execute search.py or input python search.py in terminal will run
This programs join the search and eval together depending on the input
If user input 'default' or '' (not entering anything), will read all query.text input queries
If user input a sentence, it will tokenize it and calculate similarity or the tokenized list
If after tokenization, tokenized list has one term, it will retrieve tf values of corresponding term

*top-K retrieval?
No theories used, but used simplification methods.
Similarities eliminates all non-relevant files (non of the terms in the query exist in file), then get top 5 in the list.

*Weight scheme?
tf = 1 + log(f)
idf = log(n / df)
For both document and queries

*Posting lists are ordered alphabetically, then docID
