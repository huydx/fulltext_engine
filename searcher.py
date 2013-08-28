# -*- coding: UTF-8 -*-
import sys
from search import SearchNgram
from content import Content

NGRAM = 2

class Searcher:
  def __init__(self):
    self.engine = SearchNgram(NGRAM, "./")
  
  """private execute function 
  just a  wrapper for search engine search function
  """
  def _execute(self, statement, numOfResult):
    return self.engine.normal_ngram_search(unicode(statement, "UTF-8"), numOfResult)
  
  
  """search with single word
  single word is statement without operator (without space as AND or OR keyword)
  """
  def execute_with_singleword(self, statement, numOfResult):
    search_result = self._execute(statement, numOfResult)
    print_result(search_result)
  

  """common print result function
  input as a list of tubles: [(id1, score1), (id2, score2)... ]
  search content for each id
  print content
  """
  def print_result(search_result):
    for elem in search_result:
      doc = self.engine.content.get(elem[0])
      print doc
  
  """search with list word
  list word is statement with operator (with space as AND and OR operator)
  """
  def execute_with_listword(self, statementList, numOfResult):
    normalized_list = []

    if ("OR" in statementList): #--> or routine
      #because can not contain AND and OR in one query
      #so we normalize all strings which have space
      prev_or = -1
      list_length = len(statementList) - 1
      for i in range(0, list_length):
        if i == statementList-1:
          normalized_list.append("".join(statementList[(prev_or+1):i]))
        if (statementList[i] == "OR"):
          if (prev_or + 1) >= (i - 1):
            return None #[TODO] should raise error
          else:
            normalized_list.append("".join(statementList[(prev_or+1):(i-1)]))
            prev_or = i

      return self._or_operator(normalized_list, numOfResult)
    else:                     #--> and routine
      normalized_list = statementList.split()
      return self._and_operator(normalized_list, numOfResult)
  
  """private function: or_operator
  take input as statement list (for example "a OR B" will as ["a", "OR", "b"]
  preprocess to concat string with space (for ex: "a b OR c" will as ["ab", "c"]
  take result of each statement and return list of result
  execute OR operator for all results
  """
  def _or_operator(self, statementList, numOfResult):
    result = []
    
    for i in range(0, len(statementList)-1):
      temp_ret = self._execute(statementList[i], "all")
      result.append(temp_ret) #[TODO] move below process to here!!!
    
    #or list of result
    prev_list = []
    cur_list = []
    accumulate_result = Counter()

    for j in range(0, len(result)):
      if (j == 0): 
        prev_list = result[j]
        continue
      
      cur_list = result[j]
      
      #OR operator bw previous list to current list
      max_score = cur_list[0][1] #max score is first element because our list is sorted

      for m in range(0, len(cur_list)-1):
        content_id = cur_list[m][0]
        content_score = cur_list[m][1]

        exist = [i for i,v in enumerate(prev_list) if v[0] == content_id]
        if (len(exist) > 0): # if an elent exist in both list, reduce score
          accumulate_result[content_id] = content_score - max_score
        else :
          accumulate_result[content_id] = content_score
      prev_list = cur_list
    
    print_result(accumulate_result.most_common(numOfResult))

  """private function: and_operator
  take input as statement list (for example "a b" will as ["a", "b"]
  take result of each statement and return list of result
  execute AND operator for all results
  """
  def _and_operator(self, statementList, numOfResult):
    accumulate_result = Counter()
    
    for statement in statementList:
      result = self._execute(statement, "all")
      for content in result:
        id = content[0]
        score = content[1]
        accumulate_result[id] += score 

    print_result(accumulate_result.most_common(numOfResult))

"""
main function to process as a script
"""
if __name__ == "__main__":
  param_len =  sys.argv
  if (param_len) < 3:
    print "usage: ./searcher.py statement numOfResult"
    sys.exit(1)
  
  statement = None
  statement_list = None

  if (param_len == 3):
    statement = sys.argv[1]
    numOfResult = int(sys.argv[2])
  else:
    statement_list = " ".join(sys.argv[1:param_len-1])

  searcher = Searcher()
  
  if statement != None:
    searcher.execute_with_singleword(statement, numOfResult)
  
  if statement_list != None:
    searcher.execute_with_listword(statement_list, numOfResult)
