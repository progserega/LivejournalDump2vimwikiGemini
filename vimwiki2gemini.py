#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import xmltodict
import sys
import re
import time
from datetime import datetime

def get_info(text):
    result={}
    ret=re.search(r'%title (.*)',text)
    if ret is None:
        result["title"]="без имени"
        print("error get title")
    else:
        result["title"]=ret.group(1)
    date=re.search(r'\n%date (.*)\n',text)
    if date is not None:
        print(date.group(1))
        result["timestamp"]=time.mktime(datetime.strptime(date.group(1), "%Y-%m-%d %H:%M").timetuple())
    else:
        print("error get date - set current date")
        result["timestamp"]=time.time()
    return result

def format_text(text):
    text=text.replace('%date','Дата записи:',-1)
    text=re.sub(r'^%title ',r'# ',text)
    text=re.sub(r'\[\[(.*)\]\]',r'\n=> \1\n',text)
    return text

def vimwiki2gemini(in_data, path):
    info=get_info(in_data)
    text=format_text(in_data)
#    print(text)
#    print(info)
    file_name=path+'/'+"%s.gmi"%(datetime.fromtimestamp(info["timestamp"]).strftime('%Y.%m.%d-%H%M'))
    print("save to file: %s"%file_name)
    f = open(file_name, mode="w+", encoding="utf-8")
    f.write(text)
    f.write("\n=> ../index.gmi 🔙 вернуться к началу... ")
    f.close()

if len(sys.argv) < 3:
	print("Необходимо два параметра: имя входного файла, путь, куда сохранять получаемые файлы")
	print("Выход")
	raise SystemExit(1)

#print(sys.argv)

print("load source from file: %s"%sys.argv[1])
f=open(sys.argv[1],"r")
in_data = f.read()
out_data=vimwiki2gemini(in_data,sys.argv[2])
