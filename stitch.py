#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, getopt
from scipy import misc
import numpy as np

starter = """
<html>
<head>
<style>
div.row {
  position: relative;
  }
td, div.square {
    border-right: 1px solid #999;
    border-top: 1px solid #999;
    width: 9px;
    height: 9px;
    font-size: 8px;
    text-align: center;
    padding: 0px;
    -webkit-print-color-adjust: exact;
  }
div.square {
  display: block;
  position: absolute;
}
div.square.contsq {
  border-right: 1px solid #DDD;
}
div.square.dark {
  color: white;
  -webkit-print-color-adjust: exact;
}
div.square.light {
  color: black;
  -webkit-print-color-adjust: exact;
}
</style>
</head>
<body>
<div class="grid">
<!-- table cellpadding="0" cellspacing="0" border="0" -->
"""

ender = """
<!-- /table -->
</grid>
</body>
</html>
"""

def main(argv):
  inputfile = ''
  outputfile = 'output.html'
  interval = 9
  try:
    opts, args = getopt.getopt(argv,"hi:o:v:",["ifile=","ofile=","interval="])
  except getopt.GetoptError:
    print 'usage: -i <inputfile> -o <outputfile>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'usage: -i <inputfile> -o <outputfile>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      if not os.path.isfile(arg):
        print "couldn't find that file"
        sys.exit()
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
    elif opt in ("-v", "--interval"):
      if not arg.isdigit():
        print "interval must be an integer"
        sys.exit()
      interval = int(arg)
  print "Input file is '{0}', output file is '{1}', interval is {2}".format(inputfile, outputfile, interval)

  try:
    image = misc.imread(inputfile)
  except:
    print 'usage: -i <inputfile> -o <outputfile>'
    sys.exit(2)
  
  # TODO: go through once, count distinct colors, create css class for each color
  # TODO: figure out if there's a better way to do this than absolute positioning
  
  htmllines = [starter]
  squaresize = 10
  sqcount = 0
  debug = False
  
  for rowindex, row in enumerate(image):
    htmlline = []
    
    for colindex, column in enumerate(row):
      extraclass = ""
      text = ""
      
      # if the next box is the same color as this box, increase the count and make their border lighter
      mysum = sum([column[0], column[1], column[2]])
      if (colindex % interval > 0 and len(row) > colindex + 1 and abs(mysum - sum([row[colindex + 1][0], row[colindex + 1][1], row[colindex + 1][2]])) < 27):
        sqcount = sqcount + 1
        extraclass = "contsq"
        
      # otherwise, display the count and reset it
      else:
        text = "{0}".format(sqcount + 1)
        sqcount = 0
        
      if sum([column[0], column[1], column[2]]) > 128 * 3:
        extraclass += " light"
      else:
        extraclass += " dark"
        
      htmlline.append("<div class=\"square {0}\" style=\"left: {1}; top: {2}; background-color: rgb({3},{4},{5})\">{6}</div>".format(extraclass, colindex * squaresize, rowindex * squaresize, column[0], column[1], column[2], text))
          
    htmllines.append("".join(htmlline))
  
  htmllines.append(ender)
  
  output = "\n".join(htmllines)
  
  if debug:
    print output
  
  with open(outputfile, "w") as outfilestream:
      outfilestream.write(output)

if __name__ == "__main__":
   main(sys.argv[1:])
