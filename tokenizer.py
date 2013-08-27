# -*- coding: utf-8 -*-

class Tokenizer:
  def __init__(self):
    pass

  def split(self, statement, ngram):
    result = []
    if(len(statement) >= ngram):
      for i in xrange(len(statement) - ngram + 1):
        result.append(statement[i:i+ngram])
    return result
  
  def test(self):
    test_str = "aab"
    test_tokenized = ["aa", "ab"]
    ret = self.split(test_str, 2)
    assert test_tokenized[0] == ret[0]
    assert test_tokenized[1] == ret[1]
    
