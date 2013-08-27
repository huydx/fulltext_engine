# -*- coding: UTF-8 -*-

import sys
import codecs
from index import Index

NGRAM = 2

def main(filepath, column):
  indexer = Index(NGRAM)
  f = codecs.open(filepath, "r", "utf-8")
  lines = f.readlines()

  for line in lines:
    elems = line.split("\t")
    print elems[column-1]
    indexer.append(''.join(elems[column-1]))

  f.close()
  indexer.dump("data/")
  return

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "usage: ./indexer.py INPUT_TSV_FILE_PATH TARGET_COLUMN_NUM"
    sys.exit(1)
  filepath = sys.argv[1]
  column = int(sys.argv[2])
  main(filepath, column)
