#-*- coding: utf-8 -*-
import pickle

class Content:
  def __init__(self):
    self.contentTable = dict()

  def get_content_num(self):
    return len(self.contentTable)

  def set(self, content):
    #[TODO] –ˆ‰ñget_content_num‚ğŒÄ‚Ño‚·‚Ì‚ª”ñŒø—¦H
    self.contentTable[self.get_content_num()] = content
    return self.get_content_num()

  def dump(self, file):
    f = open(file, 'w')
    pickle.dump(self.contentTable, f)
    f.close()

  def load(self, file):
    f = open(file)
    pickle.load(self.contentTable, f)
    f.close()
