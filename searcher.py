# -*- coding: UTF-8 -*-

import sys
from search import Search
from content import Content

NGRAM = 2

class Searcher:
  def __init__(self):
    self.engine = Search(NGRAM, "./")
  
  def execute(self, statement, numOfResult):
    return self.engine.zenhan_ngram_search(unicode(statement, "UTF-8"), numOfResult)

  def execute_with_print(self, statement, numOfResult):
    search_result = self.execute(statement, numOfResult)
    for elem in search_result:
      doc = self.engine.content.get(elem[0])
      print doc


if __name__ == "__main__":
  if (sys.argv) < 3:
    print "usage: ./searcher.py statement numOfResult"
    sys.exit(1)
  statement = sys.argv[1]
  numOfResult = int(sys.argv[2])
  
  searcher = Searcher()
  searcher.execute_with_print(statement, numOfResult)
