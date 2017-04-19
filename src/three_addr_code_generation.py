import sys
import cparser

temp, symbol_table = cparser.main()
count_label = 0

print symbol_table	


class label(object):
  def __init__(self, code='',id = 0):
  	self.code = code
  	self.id = count_label;
  	count_label = count_label + 1;
  def print_label(self):
  	print "L",self.id,":"
  	print "\t",self.code


