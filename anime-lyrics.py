#!/usr/bin/python2

from __future__ import print_function
from bs4 import BeautifulSoup
import sys
import os
import urllib2
import subprocess

if len(sys.argv)<3:
    print("Argument Error", file=sys.stderr)
    sys.exit(1)

if os.path.dirname(sys.argv[0]) != '':
    os.chdir(os.path.dirname(sys.argv[0]))

def get_user_idea(fd_read, argv):
    child = subprocess.Popen(["urxvt", "-e", "./urwid-list.py"]+argv)
    idea=int(os.read(fd_read, 10));
    if idea<0:
        sys.exit(1)
    return idea

def get_lyric(url):
    lyric_page=BeautifulSoup(urllib2.urlopen(url))
    print(u''.join(lyric_page.find('p', id='lyricBody').strings)
            .replace('\r', '')
            .encode('utf8'))

def query_lyric():
    artist=sys.argv[1]
    title=sys.argv[2]
    query_url="http://search.j-lyric.net/index.php?kt=%s&ka=%s" % \
            (urllib2.quote(title), urllib2.quote(artist))
    query_page=BeautifulSoup(urllib2.urlopen(query_url))
    res_list=query_page.find('div', id='lyricList')\
            .find_all('div', class_='body', recursive=False)[0:]
    res_list_str=[
            [x.find(class_='title').a.string,
                ''.join(x.find(class_='status').strings),
                x.find(class_='lyric').string]
            for x in res_list]
    res_list_str=[item.replace('\r','')
            for sublist in res_list_str for item in sublist]
    if len(res_list)<=0:
        sys.exit(2)
    elif len(res_list)==1:
        get_lyric(res_list[0].find(class_='title').a['href'])
        sys.exit(0)
    else:
        fd_pair=os.pipe()
        get_lyric(
                res_list[get_user_idea(
                    fd_pair[0],
                    res_list_str+[str(fd_pair[1]), str(os.getpid())]
                    )].find(class_='title').a['href']
                )
        sys.exit(0)

query_lyric()
