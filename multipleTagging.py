## Running multiple Taggers for improving effeciency
## Not running correctly

from nltk.tag import UnigramTagger,BigramTagger,TrigramTagger,NgramTagger

def tagging(train,taggers,backoff=None):

    for t in taggers:

        backoff=t(train,backoff=backoff)

    return backoff

## To use -

## patterns=[(r'.*ing','VB'),(r'.*ful','JJ')]
## tagger=tagging(train,[UT,BT,TT],backoff=RegexpTagger(patterns))
