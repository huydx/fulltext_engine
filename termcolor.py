# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import re

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

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

def test():
  statement = unicode("私はははフイフイです,私は", "UTF-8")
  query = [unicode("私", "UTF-8"), unicode("フイ", "UTF-8"), unicode("へ", "UTF-8")]
  
  #reorder query
  list_q = []
  for q in query:
    indices = [m.start() for m in re.finditer(q, statement)]
    for i in indices: list_q.append((q, i)) 
  
  list_q = sorted(list_q, key=lambda x: x[1])    
 
  start_idx = 0
  q_list_len = len(query)
  loop_idx = 0

  for q in list_q:
    i = q[1]  
    q_len = len(q[0])
    s = statement[start_idx:i]
    if s: sys.stdout.write(s);
    printout(q[0], YELLOW)
    start_idx = i + q_len
    loop_idx += 1

  s = statement[start_idx:len(statement)] 
  if s: print s
 
test()
