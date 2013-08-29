# -*- encoding: utf-8 -*-
from subprocess import Popen, PIPE
 
p = Popen(['php','./webma2.php'], stdin=PIPE, stdout=PIPE)
 
text= "きょう"
p.stdin.write(text + "\n")
ret = p.wait()
 
if ret == 0:
    dat = p.stdout.read()
    lines = dat.split("\n")
    for line in lines:
      print line
      if (len(line) > 0):
        ma_line = line.split()[1]
        ma_tokens = ma_line.split(",")
