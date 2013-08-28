# -*- encoding: utf-8 -*-
from subprocess import Popen, PIPE
 
p = Popen(['php','./webma2.php'], stdin=PIPE, stdout=PIPE)
 
text= "今日は晴れ"
p.stdin.write(text + "\n")
ret = p.wait()
 
if ret == 0:
    print p.stdout.read()
