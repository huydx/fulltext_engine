#-*- coding: utf-8 -*-
import pickle

class Content:
  def __init__(self):
    self.contentTable = dict()

  def get_content_num(self):
    return len(self.contentTable)

  def set(self, content):
    #[TODO] get_content_num called too much 
    self.contentTable[self.get_content_num()] = content
    current_index = self.get_content_num() - 1
    return current_index
  
  def get(self, id):
    return self.contentTable.get(id)

  def dump(self, file):
    f = open(file, 'w')
    pickle.dump(self.contentTable, f)
    f.close()

  def load(self, file):
    f = open(file)
    self.contentTable = pickle.load(f)
    f.close()

  def pretty_print(self):
    for key, value in self.contentTable.iteritems():
      print key
      print "*****"
      print value
