# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

class Tokenizer:
  def __init__(self, engine):
    self.engine = engine
  
  def split(self, statement, ngram=2):
    if self.engine == "ngram":
      return self.split_ngram(statement, ngram)
    elif self.engine == "ma":
      return self.split_ma(statement)

  def split_ngram(self, statement, ngram):
    result = []
    if(len(statement) >= ngram):
      for i in xrange(len(statement) - ngram + 1):
        result.append(statement[i:i+ngram])
    return result
  
  def split_ma(self, statement):
    result = []
    p = Popen(['php','./webma2.php'], stdin=PIPE, stdout=PIPE)
    p.stdin.write(statement.encode('utf-8') + "\n")
    ret = p.wait()

    if ret == 0:
      tokenized_result = p.stdout.read().split("\n")
      for line in tokenized_result:
        line_elems = line.split()
        if (len(line_elems) > 1):
          ma_line = line.split()[1] #each line get from webma
          ma_tokens = ma_line.split(",")
          if (len(ma_tokens) < 2): continue;

          orig = ma_tokens[0] #original token
          hira = ma_tokens[1] #hiragana token

          result.append(orig)
          if (hira != orig):
            result.append(hira)
    return result

  def test(self):
    test_str = "aab"
    test_tokenized = ["aa", "ab"]
    ret = self.split(test_str, 2)
    assert test_tokenized[0] == ret[0]
    assert test_tokenized[1] == ret[1]

    test_str2 = "今日は晴れ"
    test_tokenized2 = ["今日", "は", "晴れ", "きょう", "はれ"]
    ret2 = self.split_ma(test_str2)
    for token in test_tokenized2:
      assert (token in ret2)
    assert len(ret2) == len(test_tokenized2)
