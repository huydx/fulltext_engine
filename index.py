# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer

class Index:
  def __init__(self, ngram):
    self.tokenizer = Tokenizer()
    self.docID = DocID()
    self.content = Content()
    self.ngram = ngram

  def tokenize(self, statement):
    return self.tokenizer.split(statement, self.ngram)
    
  def append_doc(self, token, id):
    return self.docID.set(token, id)

  def set_content(self, statement):
    return self.content.set(statement)

  def append(self, statement):
    tokenized_str = self.tokenize(statement)
    content_id = self.set_content(statement)
    for token in tokenized_str:
      self.append_doc(token, content_id) 

  def dump(self, dir):
    f_content_name = "content.pickle"
    f_docid_name = "docid.pickle"
    self.content.dump(f_content_name)
    self.docID.dump(f_docid_name)
