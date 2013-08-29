# -*- coding: UTF-8 -*-
import sys
import codecs
from index import Index

NGRAM = 2

def main(filepath, column):
  indexer = Index(NGRAM)
  f = codecs.open(filepath, "r", "utf-8")
  lines = f.readlines()
  
  indexer.load("./")
  
  for line in lines:
    print line
    elems = line.split("\t")
    indexer.append(''.join(elems[column-1]))
  
  f.close()
  indexer.dump("./")
  return

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: ./indexer_update.py UPDATE_TSV_FILE_PATH TARGET_COLUMN_NUM"
    sys.exit(1)

  new_filepath = sys.argv[1]
  column = int(sys.argv[2])

  main(new_filepath, column)
