import pickle

class DocID:
  def __init__(self):
    self.docIDTable = dict()

  def get_doc_num(self):
    return len(self.docIDTable)

  def set(self, term, docID, termPos):
    value = self.docIDTable.get(term, [])
    value.append((docID, termPos))
    self.docIDTable[term] = value

  def get(self, term):
    return self.docIDTable.get(term, [])

  def dump(self, file):
    f = open(file, "w")
    pickle.dump(self.docIDTable, f)
    f.close()

  def load(self, file):
    f = open(file)
    self.docIDTable = pickle.load(f)
    f.close()
  
  def pretty_print(self):
    for key, value in self.docIDTable.iteritems():
      print key
      print "*****"
      print value
  

