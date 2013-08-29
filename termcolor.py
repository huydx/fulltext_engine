# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys

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

def breakRNA(sequence, *breakPoint):
  sequenceList = []
  noOfBreakPoints = len(breakPoint)
  for breakPt in range(noOfBreakPoints):
    for index in breakPoint:
      sequenceList.append(sequence[:index])
      sequence = sequence[index:]
    break
  return sequenceList

def test():
  statement = unicode("私はははフイです", "UTF-8")
  query = [unicode("私ははは", "UTF-8"), unicode("フイ", "UTF-8")]
  
  start_idx = 0
  q_list_len = len(query)
  loop_idx = 0

  for q in query:
    i = statement.index(q)  
    q_len = len(q)
    s = statement[start_idx:i]
    if s: print s
    printout(q, YELLOW)
    start_idx = i + q_len
    loop_idx += 1

  s = statement[start_idx:len(statement)] 
  if s: print s
  
test()
