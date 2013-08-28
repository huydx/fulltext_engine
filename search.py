# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer
from collections import Counter
import zenhan

class SearchNgram:
  def __init__(self, ngram, dir):
    self.docID = DocID()
    self.tokenizer = Tokenizer("ngram")
    self.content = Content()
    self.ngram = ngram
    self.docID.load(dir + "docid.pickle")
    self.content.load(dir + "content.pickle")
  
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
    frequency_hash = Counter() # {document_id : frequencey}
    for token in tokenList:
      content_list = self.docID.get(token)

      for content_data in content_list:
        content_id = content_data[0]
        token_index = content_data[1]

        if frequency_hash.has_key(content_id):
          frequency_hash[content_id] += 1
        else:
          frequency_hash[content_id] = 1
    frequency_hash_len = len(frequency_hash)

    if (numOfResult == "all"):
      max_num = frequency_hash_len
    else :
      max_num = frequency_hash_len if numOfResult > frequency_hash_len  else numOfResult
    
    return frequency_hash.most_common(max_num)
