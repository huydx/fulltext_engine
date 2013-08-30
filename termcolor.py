#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import re

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

reload(sys)
sys.setdefaultencoding( 'utf-8' )

#following from Python cookbook, #475186
def has_colours(stream):
  if not hasattr(stream, "isatty"):
    return False
  if not stream.isatty():
    return False # auto color only on TTYs
  try:
    import curses
    curses.setupterm()
    return curses.tigetnum("colors") > 2
  except:
    # guess false in case of error
    return False

has_colours = has_colours(sys.stdout)

def printout(text, colour=WHITE):
  if has_colours:
    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    sys.stdout.write(seq)
  else:
    sys.stdout.write(text)

def printcolor(instring, query):
  #unicode convert
  instring = instring.decode("UTF-8") 
  #reorder query
  #for i in query: print i;
  list_q = []
  for q in query:
    q2 = unicode(q, "UTF-8", "ignore")
    indices = [m.start() for m in re.finditer(q2, instring)]
    for i in indices: list_q.append((q2, i)) 

  list_q = sorted(list_q, key=lambda x: x[1])    
 
  start_idx = 0
  q_list_len = len(query)
  loop_idx = 0

  for q in list_q:
    i = q[1]  
    q_len = len(q[0])
    s = instring[start_idx:i]
    if s: sys.stdout.write(s);
    printout(q[0], YELLOW)
    start_idx = i + q_len
    loop_idx += 1

  s = instring[start_idx:len(instring)] 
  if s: print s

def test():
  statement = unicode("@nioka23_tom 今日はうまく意見まとめられなくてごめんね(/_;)うん!がんばる!ありがとね(T^T)", "UTF-8")
  query = [unicode("私", "UTF-8"), unicode("は", "UTF-8"), unicode("まとめ", "UTF-8")]

  printcolor(statement, query)

#test()
