from __future__ import print_function
import nltk
from nltk.tag import UnigramTagger,BigramTagger,TrigramTagger
from nltk.tokenize import word_tokenize
from multipleTagging import tagging
from nltk.stem import WordNetLemmatizer
from nltk.corpus import treebank,stopwords,wordnet
import re
from nltk.metrics import *
import pyperclip
import time
import ctypes
from pymsgbox import *

class ExtractNewSentences:

    #Paper referred - #http://www.aclweb.org/anthology/W09-1608

    nounDict={} #for storing nouns of a paticular sentence. To be used in Rule - 3 of findAffinity and Rule - 1 of findCloseness.
    closeScoreDict={} #for storing the average of both rules in findCloseness.
           
    def removeStopwords(self,sents):
        st=stopwords.words('english')
        newSents=[]
        for sent in sents:
            wordSent=word_tokenize(sent)
            newWordSent=[w for w in wordSent if w not in st]
            newSents.append(' '.join(newWordSent))
     
        return newSents
    
    def tagMap(self,treebank_tag):
        if treebank_tag==None:
            return wordnet.NOUN
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
 

    def lemmatizationOfText(self,sents):

        tagger=tagging(treebank.tagged_sents(),[UnigramTagger,BigramTagger,TrigramTagger],backoff=None)
        newSents=[]
        index=0
        for sent in sents:
            
            noun=[]
            taggedSent=tagger.tag(word_tokenize(sent))
            words=[]
            for (wd,tg) in taggedSent:
                newTag=self.tagMap(tg)
                if tg!=None and tg.startswith('N'):
                    noun.append(wd)
                
                wd=WordNetLemmatizer().lemmatize(wd,newTag)
                words=words+[wd]
            
            self.nounDict.setdefault(index,noun)
            index=index+1
            
            newSent=' '.join(words)
            newSents.append(newSent)
        return newSents

    def synonyms(self,nlist):
        synonymsList=[]
        for noun in nlist:
            define=wordnet.synsets(noun)
            for i in define:
                if i.pos()=='n':
                    for j in i.lemmas():
                        synonymsList=synonymsList+[j.name()]
        #synonyms=set(synonyms)
        #print(synonymsList)
        return synonymsList
       
    
    def findAffinity(self,sent1,sent2,index1,index2):

        rulesScore=[0] #for storing 1 if rule is satisfied.
        corpusPossesive=['he','she','their','yours']
        corpusConnective=['accordingly','again', 'also', 'besides', 'hence', 'henceforth', 'however','incidentally', 'meanwhile', 'moreover', 'namely', 'nevertheless','otherwise', 'that', 'then', 'therefore', 'thus','and', 'but', 'or', 'yet', 'so', 'once', 'than', 'that', 'till','whenever', 'whereas','wherever']
        words1=nltk.tokenize.word_tokenize(sent1)
        words2=nltk.tokenize.word_tokenize(sent2)

        #Rule 1 - Connective words
        if words2[0].lower() in corpusConnective:
            rulesScore.append(1)

        
        #Rule 2 - Same words
        for word in words1:
            if word in words2:
                rulesScore.append(1)
                break

        
        #Rule 3 - Thesaurus using Wordnet. Will append 1 if atleast 1 noun matches.
        if set(self.synonyms(self.nounDict[index1])).intersection(set(self.synonyms(self.nounDict[index2])))!=None:
            rulesScore.append(1)

            
        #Rule 4 - Starting with He/She
        if words2[0].lower() in corpusPossesive:
            rulesScore.append(1)

        tscore=0
        for sc in rulesScore:
            tscore=tscore+sc
            
        return float(tscore)/4

    def findCloseness(self,sents):
    
        index=0
        for i in range(len(sents)):
            tScore=[]
            for j in range(len(sents)):
          
                if i!=j:

                    nouns=set(self.synonyms(self.nounDict[i])).intersection(set(self.synonyms(self.nounDict[j])))
                    countNouns=float(len(nouns)) #Rule - 1 count number of nouns
                    distance=float(edit_distance(sents[i],sents[j]))/len(sents[i]) #Rule - 2 Find distance between 2 sentences. Used library nltk.metrics 
                    totalScore=float(countNouns+distance)/2
                    tScore.append(totalScore)    
            self.closeScoreDict.setdefault(index,tScore)  #Dictionary of Sentence index and total score of that sentence with other sentences.
            index=index+1

        
        
    def sortOrig(self,c1,c2):
        newSents=[None]*len(c1)
        newFinalSents=[]
        for s in c2:
            for i in range(len(c1)):
                if s==c1[i]:
                    newSents[i]=s
                    break
            
        for s in newSents:
            if s!=None:
                newFinalSents.append(s)
        try:
            ctypes.windll.user32.MessageBoxW(0, ' '.join(newFinalSents), "Article - ", 0)
        except:
            alert(text=' '.join(newFinalSents), title='Article - ', button='OK')
        #print(newFinalSents)

    def run(self,loop='NoValue',timer=2,reducepercent=0.75):
        timeInSec=timer*3600
        startTime=time.time()
        while True and time.time()-startTime<timeInSec:
            content=nltk.tokenize.sent_tokenize(pyperclip.paste())
            if content!=loop:
                print('Running..')
                nounDict={}
                closeScoreDict={}
                loop=content
                self.main(sents=content,reducepercent=reducepercent)
            

                
    def main(self,sents,reducepercent=0.75):

         
        sentsorig=sents[:]
        sents=self.removeStopwords(sents)
        sents=self.lemmatizationOfText(sents)

        affinityScores=[] #to store affinity scores. Taken 2 sentences at a time.
        #For example for sentence 2, add 1-2 and 2-3 score and take average. For first and last score = 1 is added additionally. 

        i=0
        affinityScores.append(1+self.findAffinity(sents[i],sents[i+1],i,i+1)) #first sentence score calculated.
        i=i+1
    
        for i in range(1,len(sents)-1):
            
            sc1=self.findAffinity(sents[i],sents[i-1],i,i-1) #previous relation sentence
            sc2=self.findAffinity(sents[i],sents[i+1],i,i+1) #next relation sentence 
            affinityScores.append(sc1+sc2)

        affinityScores.append(1+self.findAffinity(sents[i],sents[i-1],i,i-1)) #last sentence score calculated.


        self.findCloseness(sents) #call to generate closeScoreDict
        closeListFinal=[]
        for i in range(len(sents)):
            closeScore=self.closeScoreDict[i]
            s=0
            for j in range(len(closeScore)):
                s=s+closeScore[j]
            s=float(s)/len(sents)
            closeListFinal.append(s)
            
        totalScoreFinal=[]
        for i in range(len(sents)):
            totalScoreFinal.append(float(0.35*affinityScores[i]+0.65*closeListFinal[i]))
            
        nSent=int(reducepercent*len(sents))

        compList=totalScoreFinal[:] #to not copy by reference instead do it by value.
        totalScoreFinal.sort(reverse=True)
        print(compList)
        finalSents=[] #for storing new reduced sentence list
        for i in range((int(nSent))):
            
            #finalSents.append(sents[(compList.index(totalScoreFinal[i]))])
            finalSents.append(sentsorig[(compList.index(totalScoreFinal[i]))])
        #self.sortOrig(sents,finalSents)
        self.sortOrig(sentsorig,finalSents)
