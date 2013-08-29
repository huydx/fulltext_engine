# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer
from collections import Counter
import zenhan

STOPWORDS_FILE = "stopwords.dat"

class SearchNgram:
  def __init__(self, ngram, dir):
    self.docID = DocID()
    self.tokenizer = Tokenizer("ma")
    self.content = Content()
    self.ngram = ngram
    self.docID.load(dir + "docid.pickle")
    self.content.load(dir + "content.pickle")
    self.stopwords = self._load_stopwords(STOPWORDS_FILE)
  
  def zenhan_search(self, statement, numOfResult):
    han_statement = zenhan.z2h(statement)
    zen_statement = zenhan.h2z(statement)

    han_list = self.tokenizer.split(han_statement)
    zen_list = self.tokenizer.split(zen_statement)
    
    to_search = han_list + zen_list
    return self._search(to_search, numOfResult)

  def normal_search(self, statement, numOfResult):
    tokenized_list = self.tokenizer.split(statement)
    return self._search(tokenized_list, numOfResult)

  def _search(self, tokenList, numOfResult):
    frequency_hash = Counter() # {document_id : frequency}
    frequency_memoize = dict()
    token_search_index = 0 
    
    #<<<loop
    for token in tokenList:
      content_list = self.docID.get(token)

      for content_data in content_list:
        content_id = content_data[0]
        token_doc_index = content_data[1]
        
        #calculate score --> customize here
        #format of frequency_memoize : (token, token_doc_index, token_search_index)
        if frequency_hash.has_key(content_id):
          #if token is stopwords, not increase score (less important)
          if token in self.stopwords: continue;
          
          #else increase score
          frequency_memoize[content_id].append((token, token_doc_index, token_search_index))
          frequency_hash[content_id] += 1
        else:
          frequency_memoize[content_id] = [(token, token_doc_index, token_search_index)]
          frequency_hash[content_id] = 1
      token_search_index += 1
    #>>>endloop

    #increase score by confirming offset frmo frequency_memoize
    #self._print_freq_memoize(frequency_memoize) 
    
    #get numOfResult from result
    frequency_hash_len = len(frequency_hash)
    
    if (numOfResult == "all"):
      max_num = frequency_hash_len
    else :
      max_num = frequency_hash_len if numOfResult > frequency_hash_len  else numOfResult
    
    return frequency_hash.most_common(max_num)

  def _print_freq_memoize(self, frequency_memoize):
    for key, val in frequency_memoize.iteritems():
      print "*****"
      #print doclist
      for item in val:
        print "{0} : {1} : {2}\n".format(item[0], item[1], item[2])

  def _load_stopwords(self, file):
    f = open(file)
    ret = f.read()
    f.close()
    return ret
