import re
import bisect
import xml.sax
import timeit
import subprocess
import mwparserfromhell
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import Stemmer
import re
import math
import timeit
stop_words = set(stopwords.words('english'))
stemmer = Stemmer.Stemmer('english')

reg1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
reg2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
reg3 = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)
refreg=r'{{v?cite(.*?)}}'
reg4 = re.compile(r'[-.,:;_?()"/\']',re.DOTALL)
reg5 = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
# reg6 = re.compile(r'[\'~` \n\"_!=@#$%-^*+{\[}\]\|\\<>/?]',re.DOTALL)
reg6 = re.compile(r'[\'~`\"_!=@#$%\-^*+{\[}\]\|\\<>/?]',re.DOTALL)

catRegExp = r'\[\[category:(.*?)\]\]'
infoRegExp = r'{{infobox(.*?)}}'
refRegExp = r'== ?references ?==(.*?)=='
reg7 = re.compile(infoRegExp,re.DOTALL)
reg8 = re.compile(refRegExp,re.DOTALL)
reg9 = re.compile(r'{{(.*?)}}',re.DOTALL)
reg10 = re.compile(r'<(.*?)>',re.DOTALL)
reg11=re.compile(r'\[\[(.*?)\]\]')
reg12=re.compile(catRegExp,re.DOTALL)

index_path="inverted_index/merged_path/"

def gettitles(toplist):
    top_titles=[]
    for docid in toplist:
        title_file_no=math.floor(docid/30000)
        title_index=docid%30000
        fp=open("title/"+str(title_file_no),'r')
        
        i=0
        for line in fp.readlines():
            if(i==title_index):
                top_titles.append(line[:-1])
            i+=1
    return top_titles
        
        
        
        
    

 
def convert(titledict):
    resdict={}
    for key,val in titledict.items():
        val=val.strip()
        token=val.split()
        token=stemmer.stemWords(token)
        for t in token:
           
            resdict[t]=key
    return resdict

def getposting(index_path,word):
#     print(word)
    secondaryindex_fp=open(index_path+"secondary_index.txt",'r')
    secondary_list=[]
    for line in secondaryindex_fp.readlines():
        secondary_list.append(line[:-1])
        
    index_no=bisect.bisect(secondary_list, word)-1 #index number fetched from secondary index
    if index_no==-1:                  #invalid index number
        return ""
    index_path=index_path+str(index_no)+".txt"   # path to index file to be searched
    index_fp=open(index_path,'r')
    
    for entry in index_fp.readlines():
        idx=entry.index('#')
        w=entry[:idx]
        if(w==word):
            return entry[idx:]
    return ""                                   # if posting doesn't exist return empty string

def gettopten(docid_freq_tfidf):
    rank_list=[]
    top_ten=[]
    
    for docid in docid_freq_tfidf:
#         print(docid)
        rank_list.append([[docid_freq_tfidf[docid][0],docid_freq_tfidf[docid][1]],docid])
        
    rank_list.sort(reverse=True)
    
    i=0
    for item in rank_list:
        top_ten.append(item[1])
        i+=1
        if i == 10:
            break
            
    return top_ten
        
        
        
        
        
        
    
    
   
    
        
        
    


# index_path="inverted_index/merged_path/"

# index_path="inverted_index/merged_path/"



def top_search1(st):

    st=st.lower()
    index=st.find(':')
    docid_freq_tfidf={}  # dict keys are doc_id and value is list of frequescy and tfidf weight
    if(index>=0):
        titledict={}

        field='#' 
        buffer=""
        for i in range(len(st)):
            if st[i]==':':
                if field!='#':
                    titledict[field]=buffer[0:len(buffer)-1]
                    buffer=""
                field=st[i-1]
                buffer=""

            else:
                buffer=buffer+st[i]

        if field!='#':
            titledict[field]=buffer
        resdict=convert(titledict)     #dict of word and their field type
#         print(resdict)


        for word,field in resdict.items():
#             print(word,field,"#####################################################################################################################################################################################################################################################3")
            postings=getposting(index_path,word)
    #         print(postings)

            if postings=="":
                continue


            postings=postings[:-1]  #remove new line

            postings=postings.split('#')
            postings=postings[1:]   #first ele in postings is always "" so remove it
    #         print(postings)

            for posting in postings:
                if field=='c':
                    postinglist=re.findall(r'c[0-9]*',posting,re.DOTALL)
                if field=='i':
                    postinglist=re.findall(r'i[0-9]+',posting,re.DOTALL)
                if field=='t':
                    postinglist=re.findall(r't[0-9]*',posting,re.DOTALL)
                if field=='e':
                    postinglist=re.findall(r'e[0-9]*',posting,re.DOTALL)
                if field=='b':
                    postinglist=re.findall(r'b[0-9]*',posting,re.DOTALL)
                if field=='r':
                    postinglist=re.findall(r'r[0-9]*',posting,re.DOTALL)
                if(len(postinglist)): 
                    poslist=posting.split('@')
                    tfidf=int(poslist[1])+10
                    prepost=poslist[0]

                    docid=re.findall(r'id[0-9]*',posting,re.DOTALL)

                    docid=int(re.findall(r'[0-9]+',docid[0],re.DOTALL)[0])

                    if docid not in docid_freq_tfidf:
                        fre_tfidfsum=[1,tfidf]
                        docid_freq_tfidf[docid]=fre_tfidfsum
                    else:
                        fre_tfidfsum=docid_freq_tfidf[docid]
                        fre_tfidfsum[0]+=1
                        fre_tfidfsum[1]+=tfidf
                        docid_freq_tfidf[docid]=fre_tfidfsum
    #             else:
    #                 poslist=posting.split('@')
    #                 tfidf=int(poslist[1])
    #                 prepost=poslist[0]

    #                 docid=re.findall(r'id[0-9]*',posting,re.DOTALL)

    #                 docid=int(re.findall(r'[0-9]+',docid[0],re.DOTALL)[0])

    #                 if docid not in docid_freq_tfidf:
    #                     fre_tfidfsum=[1,tfidf]
    #                     docid_freq_tfidf[docid]=fre_tfidfsum
    #                 else:
    #                     fre_tfidfsum=docid_freq_tfidf[docid]
    #                     fre_tfidfsum[0]+=1
    #                     fre_tfidfsum[1]+=tfidf
    #                     docid_freq_tfidf[docid]=fre_tfidfsum




        top_ten=gettopten(docid_freq_tfidf)
        top_titles=gettitles(top_ten)
#         print(top_ten)
#         print(top_titles)

    else:
        st=reg1.sub(' ',st)
        st=reg2.sub(' ',st)
        st=reg3.sub(' ',st)
        st=reg4.sub(' ',st)
        st=reg5.sub(' ',st)
        st=reg6.sub(' ',st)
        st=st.strip()
        st=st.split()

        st=[word for word in st if word not in stop_words]
        st=stemmer.stemWords(st)

        for word in st:
#             print(word)
            postings=getposting(index_path,word)
    #         if word.isnumeric():
    #             print(postings)
            if postings=="":
                continue


            postings=postings[:-1]  #remove new line

            postings=postings.split('#')
            postings=postings[1:] 

            for posting in postings:
    #             if field=='c':
    #                 postinglist=re.findall(r'c[0-9]*',posting,re.DOTALL)
    #             if field=='i':
    #                 postinglist=re.findall(r'i[0-9]+',posting,re.DOTALL)
    #             if field=='t':
    #                 postinglist=re.findall(r't[0-9]*',posting,re.DOTALL)
    #             if field=='e':
    #                 postinglist=re.findall(r'e[0-9]*',posting,re.DOTALL)
    #             if field=='b':
    #                 postinglist=re.findall(r'b[0-9]*',posting,re.DOTALL)
    #             if field=='r':
    #                 postinglist=re.findall(r'r[0-9]*',posting,re.DOTALL)

                poslist=posting.split('@')
                tfidf=int(poslist[1])-10
                prepost=poslist[0]


                docid=re.findall(r'id[0-9]*',posting,re.DOTALL)
                docid=int(re.findall(r'[0-9]+',docid[0],re.DOTALL)[0])

                if docid not in docid_freq_tfidf:
                    fre_tfidfsum=[1,tfidf]
                    docid_freq_tfidf[docid]=fre_tfidfsum
                else:
                    fre_tfidfsum=docid_freq_tfidf[docid]
                    fre_tfidfsum[0]+=1
                    fre_tfidfsum[1]+=tfidf
                    docid_freq_tfidf[docid]=fre_tfidfsum

        top_ten=gettopten(docid_freq_tfidf)

        top_titles=gettitles(top_ten)
        
        
        
    return (top_ten,top_titles)
            
            
def main():

    query_in=open("queries.txt",'r')
    query_out=open("queries_op.txt",'w')

    for line in query_in.readlines():
    #     print(line)
        line=line.split(',')
        top_k=int(line[0])
        query=line[1][:-1]

        start = timeit.default_timer()
        ids_titles=top_search1(query)         #main search logic
        end = timeit.default_timer()

        for n in range(top_k):
            write_line=str(ids_titles[0][n])+","+str(ids_titles[1][n])+"\n"
            query_out.write(write_line)

        t=end-start
        query_out.write(str(round(t,3))+","+str(round(t/top_k,3))+"\n")
        query_out.write("\n")

    query_out.close()
    print("End of processing")

if __name__ == "__main__": 
	main() 
        
