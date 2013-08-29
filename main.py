#-*- coding: utf-8 -*-
import sys
import codecs
from tokenizer import Tokenizer
from content import Content

#test_tokenizer = Tokenizer()
#test_tokenizer.test()

content = Content()
content.load("content.pickle")
content.pretty_print()
