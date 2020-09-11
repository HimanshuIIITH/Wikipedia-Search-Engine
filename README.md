## Wikipedia-Search-Engine
A wikipedia content search engine on ~40 GB of wikipedia dump. In order to fecilitate faster search results indexing technique is used and top k results are fetched using ranking algorithem.

### Parsing:
Parsing is done using SAX parser, which efficiently reads the xml corpus line by line so that we don't run out of memory while parsing.
Parsing a page includes following operations:
```
   - Case Folding
   - Tokenization
   - Stop words removel
   - Stemming
   ```
### Inverted Index:
Inverted index of a token contains posting list having information of documents in which word is occouring. Along with doc information it also stores fields info as well.
Following fields have been used in posting list:

```
t:title
c:category
i:infobox
r:reference
e:external link
b:body
tfidf
```
tfidf is made of two factors:
- tf: How frequent a word is in a particular document or field
- idf: How relevent that word is considering all documents 

typical line of inverted index looks like-
```
token#doc_id123t12c12i5r34@1234
```
#### Chalenges:
- Since we can not store and process all pages of wikidump(~40gb) in main memory,pages are processed in batch(30000 pages) and severeal intermediatory index files will  be generated.
- Sorting these index files requires external sorting 
- After sorting and merging we do have multiple final inverted index files, which needs to be accessed using secondary index.
<<<<<<< Updated upstream

=======
   
>>>>>>> Stashed changes

### Technologies:
Language:Python3

Modules:
```
NLTK
Pystemmer
```
### Directory structure:

- base directory=/
- title directory=/title
- inverted index directory=/inverted_index/merged_path
- query's text file=/
- wiki dump directory(in zip formate)=/wiki_dump


### How to run
#### 1.Index creation:
1. run phase2.ipynb file to create index
2. run fetchtitle.ipynb to create title and title_id map files
#### 2.Search:
1. Put queries in quires.txt
<<<<<<< Updated upstream
2. Run search_refined.py to fetch search result

### Search output:
Search output will be dumped into queries_op.txt file
=======
2. Run search.py to fetch search result

### Search output:
Search output will be dumped into queries_op.txt file

>>>>>>> Stashed changes
