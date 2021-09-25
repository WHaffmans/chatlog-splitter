# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 00:27:20 2021

usage: discordlog.py [-h] [-n N] [-z Z] Input_File Output_Name

Split a chatlog in mutiple files

positional arguments:
  Input_File   the path to input file
  Output_Name  the output name

optional arguments:
  -h, --help   show this help message and exit
  -n N         number of msgs on page
  -z Z         number of digits in filename

@author: Willem Haffmans
"""
 
from bs4 import BeautifulSoup, Tag
import argparse
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
 
def list_split(listA, n):
    """Split a list in chunks of size n"""
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk
        

def add_nav():
    """add navigation to the body"""
    if prevpage:
        a_prev = Tag(new_soup,name='a', attrs={'href': args.output + prevpage + '.html'})
        a_prev.string = 'Previous'
        body.append(a_prev)
    if nextpage:
        a_next = Tag(new_soup,name='a', attrs={'href': args.output + nextpage + '.html'})
        a_next.string = 'Next'
        body.append(a_next)


# Create the parser
my_parser = argparse.ArgumentParser(description='Split a chatlog in mutiple files')

# Add the arguments
my_parser.add_argument('-n', action='store', default=5, type=int, help='number of msgs on page')
my_parser.add_argument('-z', action='store', default=4, type=int, help= 'number of digits in filename')

my_parser.add_argument('input',
                       metavar='Input_File',
                       type=str,
                       help='the path to input file')

my_parser.add_argument('output',
                       metavar='Output_Name',
                       type=str,
                       help='the output name')

# Execute the parse_args() method
args = my_parser.parse_args()

logging.debug('opening the input file')

# Open the input file and parse the html 
with open(args.input,encoding="utf8") as f:
    soup = BeautifulSoup(f, "html.parser")

# find the different sections
logging.debug('find head')
head = soup.find("head")
logging.debug('find preamble')
header = soup.find("div", class_="preamble")
logging.debug('find chatlog')
msgs = soup.find_all("div", class_="chatlog__message-group")
logging.debug('find postamble')
footer = soup.find("div", class_= "postamble")

# split the list of messages in chunks and create a htmlpage for every chunck
for n, page in enumerate(list_split(msgs,args.n),1):
    
    logging.debug('create new soup for page' + str(n))
    new_soup = BeautifulSoup()
    logging.debug('creating tags')
    html = Tag(new_soup,name='html')
    body = Tag(new_soup,name='body')
    chatlog = Tag(new_soup,name="div",attrs={'class':'chatlog'})
    
    nextpage = str(n + 1).zfill(args.z) if args.n * n < len(msgs) else None
    prevpage = str(n - 1).zfill(args.z) if n > 1 else None
   
    new_soup.append(html)
    html.append(head)
    html.append(body)
    body.append(header)
    
    add_nav()
        
    for msg in page:
        if msg:
            chatlog.append(msg)
    body.append(chatlog)
    
    add_nav()
    html.append(footer)
    
# write the output    
    logging.debug('writing file')
    with open(args.output+str(n).zfill(args.z)+'.html','wb') as f:
        f.write(new_soup.prettify(encoding='utf-8'))
    logging.debug('done with page' + str(n))

