# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer
from collections import Counter

class Search:
  def __init__(self, ngram, dir):
    self.docID = DocID()
    self.tokenizer = Tokenizer()
    self.content = Content()
    self.ngram = ngram
    self.docID.load(dir + "docid.pickle")
    self.content.load(dir + "content.pickle")

  def ngram_search(self, statement, numOfResult):
    frequency_hash = Counter() # {document_id : frequencey}
    
    tokenized_str = self.tokenizer.split(statement, self.ngram)

    for token in tokenized_str:
      content_id_list = self.docID.get(token)

      for content_id in content_id_list:
        if frequency_hash.has_key(content_id):
          frequency_hash[content_id] += 1
        else:
          frequency_hash[content_id] = 1
    
    max_num = len(frequency_hash) if numOfResult > len(frequency_hash) else numOfResult
    return frequency_hash.most_common(max_num)
