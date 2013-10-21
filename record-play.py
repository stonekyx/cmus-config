#!/usr/bin/python2

import os
import subprocess

def get_file_info():
    cmus=subprocess.Popen(["cmus-remote", "-Q"], stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    uncooked=cmus.stdout.read().split('\n')
    cmus.stdout.close()
    ans = ""
    status = ""
    position = ""
    for s in uncooked:
        if s.split(' ', 1)[0]=="file":
            ans = s.split(' ', 1)[1]
        elif s.split(' ', 1)[0]=="status":
            status = s.split(' ', 1)[1]
        elif s.split(' ', 1)[0]=="position":
            position = s.split(' ', 1)[1]
    if status=="playing" and position=="0":
        return ans
    else:
        return ""

rec = get_file_info()
if rec!="":
    fp = open("/home/stone/.cmus/play-record", "a")
    if fp.tell()!=0:
        fp.write('\0')
    fp.write(rec)
    fp.close()
