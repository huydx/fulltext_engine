# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer


class Index:
  def __init__(self, ngram):
    self.tokenizer = Tokenizer("ma")
    self.docID = DocID()
    self.content = Content()
    self.ngram = ngram

  def tokenize(self, statement):
    #return self.tokenizer.split(statement, self.ngram)
    return self.tokenizer.split(statement)

  def append_doc(self, token, id, pos):
    return self.docID.set(token, id, pos)

  def set_content(self, statement):
    return self.content.set(statement)

  def append(self, statement):
    tokenized_str = self.tokenize(statement)
    content_id = self.set_content(statement)

    token_index = 0

    for token in tokenized_str:
      self.append_doc(token, content_id, token_index)
      token_index += 1 

  def dump(self, dir):
    f_content_name = "content.pickle"
    f_docid_name = "docid.pickle"
    self.content.dump(f_content_name)
    self.docID.dump(f_docid_name)

  def load(self, dir):
    f_content_name = "content.pickle"
    f_docid_name = "docid.pickle"

    self.content.load(f_content_name)
    self.docID.dump(f_docid_name)
