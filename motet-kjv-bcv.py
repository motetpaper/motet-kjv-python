#!/usr/bin/env python3

# motet-kjv-bcv.py
# job   : creates book-chapter-verse index files
# job   : this script creates the verse references, one per line
# git   : https://github.com/motetpaper/motet-kjv-python
# lic   : MIT

import re

def motet_kjv_getcv(p):
  return re.findall(rcv, p)

def motet_kjv_getbcv(cv):
  bcv = []
  b=0
  c_tmp = 0
  v_tmp = 0
  c = 0
  v = 0
  for h in cv:
    ## chapter, verse
    c,v = re.split(r':', h)

    ## detects if a new book has started based on chapter-verse increments
    if(int(c_tmp) > 0 and int(v_tmp) > 0):
      if(int(c) < int(c_tmp) or (int(c) == int(c_tmp) and int(v) < int(v_tmp))):
        #print('new book')
        b=b+1

    ## add book-chapter-verse to list
    bcv.append([int(b),int(c),int(v)])

    ## for debugging
    ## the zero-based book index
    ## followed by the current chapter and verse
    ## followed by the chapter and verse from the previous loop
    ## print('book-'+str(b), c, v, c_tmp, v_tmp)

    ## store old values for next loop
    c_tmp, v_tmp = c, v
  return bcv

def motet_kjv_getbcvh(bcv, booksfn):
    books = motet_get_data_aslist(booksfn)

    ## convert book number to book name
    bcv = [[books[x[0]],x[1],x[2]] for x in bcv];

    ## convert to human readable book:chapter:verse format
    bcvh = [x[0] + ' ' + ':'.join([str(s) for s in x[1:]]) for x in bcv];
    return bcvh

def motet_astxt(listdata):
  return '\n' . join(listdata) + '\n'

def motet_get_data_aslist(filename):
  with open(filename) as f:
    return f.read().strip().split('\n')

def motet_put_data(fn, data):
  with open(fn, 'w') as f:
    f.write(data)

## this is the project gutenberg KJV bible
infile = 'src/pg10.txt'
# old testament book titles
p1books = 'src/books1.txt'
# new testament book titles
p2books = 'src/books2.txt'

## outfiles
outfile1 = 'bcvh1.txt'
outfile2 = 'bcvh2.txt'

## the delimiter between sections
stars = '***'
# regex chapter-verse markers
rcv = r'\d{1,3}:\d{1,4}'

s = ''
with open(infile) as f:
  s = f.read()

  ## splits the front matter and back matter
  ## from the bible texts
  a = s.split(stars)

  # old testament
  p1 = a[2]

  # new testament
  p2 = a[3]

  ## extracts all chapter-verse markers [c:v] lists
  cv1 = motet_kjv_getcv(p1)
  cv2 = motet_kjv_getcv(p2)
 # print(cv1, cv2)

  ## transforms to book-chapter-verse [b:c:v] lists
  bcv1 = motet_kjv_getbcv(cv1)
  bcv2 = motet_kjv_getbcv(cv2)

  ## transforms to human-readable book-chapter-verse [Book c:v] lists
  bcvh1 = motet_kjv_getbcvh(bcv1, p1books)
  bcvh2 = motet_kjv_getbcvh(bcv2, p2books)
#  print(bcvh1, bcvh2)

  ## saves output to flat files
  motet_put_data(outfile1, motet_astxt(bcvh1))
  motet_put_data(outfile2, motet_astxt(bcvh2))
