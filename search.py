# -*- coding: UTF-8 -*-
from docid import DocID
from content import Content
from tokenizer import Tokenizer
from collections import Counter
import zenhan

STOPWORDS_FILE = "stopwords.dat"
NEWWORD_FACTOR = 10
ORDER_FACTOR = 5.0 #float
DEBUG = True 

class Search:
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
    
    han_list = self.tokenizer.split_query(han_statement)
    zen_list = self.tokenizer.split_query(zen_statement)
    
    if han_statement != zen_statement:
      to_search = han_list + zen_list
    else:
      to_search = self.tokenizer.split_query(statement) 

    return self._search(to_search, numOfResult)

  def normal_search(self, statement, numOfResult):
    tokenized_list = self.tokenizer.split_query(statement)
    return self._search(tokenized_list, numOfResult)

  def _search(self, tokenList, numOfResult):
    frequency_hash = Counter()  #return value {document_id : frequency}
    frequency_memoize = dict()  #memoize offset of query and offset of document to cal score 
    doc_tok_map = []            #memoize index of word in query to prevent search same word

    token_search_index = 0 
    
    #<<<search loop
    for token in tokenList:
      token_content = token[0] #token content
      token_id = token[1] #real index in query statement

      content_list = self.docID.get(token_content)

      for content_data in content_list:
        already_searched = False 

        content_id = content_data[0]
        token_doc_index = content_data[1]
        
        #if same token, same index in document than skip
        map = (content_id, token_id)
        if map in doc_tok_map:
          already_searched = True
        else:
          doc_tok_map.append(map)

        #calculate score --> customize here
        #format of frequency_memoize : (token, token_doc_index, token_search_index)
        if frequency_hash.has_key(content_id):
          if token_content in self.stopwords: continue; #if stop word continue
          
          #else increase score
          if not self._exist_freq_memoize(token_id, frequency_memoize[content_id]): #if token already in memoize
            frequency_memoize[content_id].append((token_content, token_id, token_doc_index, token_search_index))
          
          #if this word already searched, increase with smaller score
          if already_searched:
            frequency_hash[content_id] += 1
          else:
            frequency_hash[content_id] += NEWWORD_FACTOR

        else:
          frequency_memoize[content_id] = [(token_content, token_id, token_doc_index, token_search_index)]
          frequency_hash[content_id] = 1
      token_search_index += 1
    #>>>endloop

    #increase score by confirming offset from frequency_memoize
    if False:
      #self._print_freq_memoize(frequency_memoize)
      self._cal_score_by_freq_memoize(frequency_memoize, frequency_hash)
    
    if DEBUG:
      print frequency_hash.most_common(20)

    #get numOfResult from result
    frequency_hash_len = len(frequency_hash)
    
    if (numOfResult == "all"):
      max_num = frequency_hash_len
    else :
      max_num = frequency_hash_len if numOfResult > frequency_hash_len  else numOfResult
    
    return frequency_hash.most_common(max_num)
  
  def _exist_freq_memoize(self, token_id, frequency_memoize_item):
    for token_item in frequency_memoize_item:
      if (token_id == token_item[1]): return True;
    return False
    

  def _cal_score_by_freq_memoize(self, frequency_memoize, frequency_hash):
    for key, val in frequency_memoize.iteritems(): #key is content_id
      # for each key calculate score for this key
      point = 0 #score for that key
      
      prev_token = None
      if len(val) >= 2: #if > 2 item so we need to care about order
        loop_time = 0
        for item in val:
          if (loop_time == 0):
            prev_token = item
            loop_time += 1
            continue
          else:
            current_token = item
            doc_order = float(prev_token[2] - current_token[2])
            found_order = float(prev_token[3] - current_token[3])
            
            if abs(doc_order) > abs(found_order):
              diff = doc_order / found_order
            else:
              diff = found_order / doc_order

            plus_point = ORDER_FACTOR / (diff)
            point += int(plus_point)

            if DEBUG:
              print "({0}, {1}) : {2} : {3}\n".format(prev_token[0], prev_token[1], prev_token[2], prev_token[3])
              print "({0}, {1}) : {2} : {3}\n".format(current_token[0], current_token[1], current_token[2], current_token[3])
              print point
          loop_time += 1
      
      frequency_hash[key] += point

  def _print_freq_memoize(self, frequency_memoize):
    MAX_PRINT = 20
    loop_idx = 0
    for key, val in frequency_memoize.iteritems():
      #print doclist
      if len(val) >= 2:
        print "*******"
        for item in val:
          print "({0}, {1}) : {2} : {3}\n".format(item[0], item[1], item[2], item[3])
        print "*******"
      loop_idx += 1
      #if (loop_idx >= MAX_PRINT): return;

  def _load_stopwords(self, file):
    f = open(file)
    ret = f.read()
    f.close()
    return ret
