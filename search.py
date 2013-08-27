# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer
from collections import Counter
import zenhan

class Search:
  def __init__(self, ngram, dir):
    self.docID = DocID()
    self.tokenizer = Tokenizer()
    self.content = Content()
    self.ngram = ngram
    self.docID.load(dir + "docid.pickle")
    self.content.load(dir + "content.pickle")
  
  def zenhan_ngram_search(self, statement, numOfResult):
    han_statement = zenhan.z2h(statement)
    zen_statement = zenhan.h2z(statement)

    han_list = self.tokenizer.split(han_statement, self.ngram)
    zen_list = self.tokenizer.split(zen_statement, self.ngram)
    
    to_search = han_list + zen_list

    return self.ngram_search(to_search, numOfResult)

  def ngram_search(self, tokenList, numOfResult):
    frequency_hash = Counter() # {document_id : frequencey}
    for token in tokenList:
      content_id_list = self.docID.get(token)

      for content_id in content_id_list:
        if frequency_hash.has_key(content_id):
          frequency_hash[content_id] += 1
        else:
          frequency_hash[content_id] = 1
    
    max_num = len(frequency_hash) if numOfResult > len(frequency_hash) else numOfResult
    return frequency_hash.most_common(max_num)

  def normal_ngram_search(self, statement, numOfResult):
    tokenized_list = self.tokenizer.split(statement, self.ngram)
    return self.ngram_search(tokenized_list, numOfResult)
    
