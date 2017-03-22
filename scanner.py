#!/usr/bin/python
#
# Finds docx/txt files in a folder, then parses them for search strings defined in dict.txt in current directory.
#
import os
import re
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
sys.path.append("/home/sysuser/projects/tools/python-docx-master/")
import docx
if (len(sys.argv) != 3):
   sys.stderr.write("usage: scanner.py searchroot dictfile\n")
   sys.exit(0)
if (not os.path.isdir(sys.argv[1])):
   sys.stderr.write("error: searchroot directory not found: \"%s\"\n" % sys.argv[1])
   sys.exit(1)
if (not os.path.isfile(sys.argv[2])):
   sys.stderr.write("error: dictfile file not found: \"%s\"\n" % sys.argv[2])
   sys.exit(1)
search_strings = []
for i in open(sys.argv[2], "r").readlines():
   search_strings.append(i.strip())
docx_files = []
os.chdir(sys.argv[1])
def convert_pdf_to_txt(path):
   rsrcmgr = PDFResourceManager()
   retstr = StringIO()
   codec = 'utf-8'
   laparams = LAParams()
   device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams) 
   fp = file(path, 'rb') 
   interpreter = PDFPageInterpreter(rsrcmgr, device) 
   password = ""
   maxpages = 0
   caching = True
   pagenos=set()

   for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
      interpreter.process_page(page) 
   text = retstr.getvalue()
   fp.close()
   device.close()
   retstr.close()
   return text
for root, subdirs, files in os.walk(sys.argv[1]): 
   for f in files: 
      # This part does DOCX
      if re.search("\.docx$", f, re.IGNORECASE):
         try:
            current_docx = docx.Document(root + "/" + f) 
            for w in search_strings: 
               for p in current_docx.paragraphs: 
                  match = re.findall("(.{0,10}" + w + ".{0,10})", p.text, re.IGNORECASE) 
                  for m in match: 
                     print "\"%s/%s\", \"%s\"" % (root, f, m) 
         except: 
            sys.stderr.write("Error: cannot open \"%s/%s\"\n" % (root, f)) 
      # This part does TXT
      if re.search("\.txt$", f, re.IGNORECASE):
         try:
            lines = open("%s/%s" % (root, f), "r").readlines()
            for w in search_strings: 
               for line in lines: 
                  match = re.findall("(.{0,10}" + w + ".{0,10})", line, re.IGNORECASE) 
                  for m in match: 
                     print "\"%s/%s\", \"%s\"" % (root, f, m)
         except:
            sys.stderr.write("Error: cannot open \"%s/%s\"\n" % (root, f))
      # This part does PDF
      if re.search("\.pdf$", f, re.IGNORECASE):
         try:
            lines = convert_pdf_to_txt("%s/%s" % (root, f)).split("\n")
            for w in search_strings: 
               for line in lines: 
                  match = re.findall("(.{0,10}" + w + ".{0,10})", line, re.IGNORECASE) 
   	              for m in match: 
                     print "\"%s/%s\", \"%s\"" % (root, f, m)
         except:
            sys.stderr.write("Error: cannot open \"%s/%s\"\n" % (root, f))
     # This part does not yet do EML
