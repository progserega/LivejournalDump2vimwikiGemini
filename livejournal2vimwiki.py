#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import xmltodict
import sys
import re
from datetime import datetime

def format_tags(str_tags):
    custom_tag="несвязанное_из_livejournal:livejournal"
    result=":%s:"%custom_tag
    if str_tags is None or str_tags.strip() == "":
        return result
    tags_list=str_tags.split(',')
    for tag in tags_list:
        result+=tag.strip().replace(' ','_',-1)
        result+=':'
    return result

def format_text(text):
    text=text.replace('<p>','',-1).replace('</p>','',-1)
    text=text.replace('<blockquote>','_',-1)
    text=text.replace('</blockquote>','_',-1)
    text=text.replace('<br>','\n',-1)
    text=text.replace('&lt;br /&gt;','\n',-1)
    text=text.replace('<br />','\n',-1)
    text=text.replace('&quot;','"',-1)
    text=text.replace('&nbsp;',' ',-1)
    
    text=re.sub(r'<img alt=".*" src="(.*)" />',r'[[\1]]',text)
    text=re.sub(r'<img src="(.*)" alt=".*" */>',r'[[\1]]',text)
    #text=re.sub(r'<img (alt=".*")* *src="(.*)" *(alt=".*")* */>',r'[[\2]]',text)
    text=re.sub(r'<span style="font-size:[0-9]*\.*[0-9]*em;">(.*)</span>',r'\1',text)
    text=re.sub(r'<b>(.*)</b>',r'*\1*',text)
    #text=re.sub(r'<blockquote>(.*)</blockquote>',r'_\1_',text)
    #text=re.sub(r'<blockquote>(.*)</blockquote>',r'_\1_',text)
    return text

def create_vimwiki(in_data, path):
    event=in_data["event"]
    text=format_text(event["event"])
    timestamp=int(event["event_timestamp"])
    #date_str=event["eventtime"]
    if "taglist" in event["props"]:
        tags=format_tags(event["props"]["taglist"])
    else:
        tags=format_tags("")
    if "subject" in event:
        title=event["subject"]
    else:
        title="без_имени"
    url=event["url"]
    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    #date=datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    date=datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

    data = """%%title %(title)s
%%date %(date)s
%(text)s

----
Ссылки на связанные идеи:
* [[%(url)s]] - исходная ссылка на livejournal.com

Теги:
%(tags)s"""%{\
    "title":title,\
    "date":date,\
    "text":text,\
    "url":url,\
    "tags":tags\
    }
    
    file_name=path+'/'+"%s-%s.wiki"%(datetime.utcfromtimestamp(timestamp).strftime('%Y.%m.%d-%H%M'),title)
    print("save to file: %s"%file_name)
    f = open(file_name, mode="w+", encoding="utf-8")
    f.write(data)
    f.close()

if len(sys.argv) < 3:
	print("Необходимо два параметра: имя входного файла, путь, куда сохранять получаемые файлы")
	print("Выход")
	raise SystemExit(1)

#print(sys.argv)

print("load source from file: %s"%sys.argv[1])
f=open(sys.argv[1],"r")
in_data = xmltodict.parse(f.read())
#print(json.dumps(in_data, sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False))
out_data=create_vimwiki(in_data,sys.argv[2])
#print(out_data)
